from django.contrib.auth import get_user_model
from rest_framework.fields import SerializerMethodField, ImageField
from rest_framework.serializers import ModelSerializer, CharField

from .models import (
    Account,
    Links,
    SubTier,
    SubInfo,
    Transaction,
    CustomizationSettings,
    CustomizationData,
)

User = get_user_model()


class CustomizationDataSerializer(ModelSerializer):
    class Meta:
        model = CustomizationData
        fields = '__all__'


class CustomizationSettingsSerializer(ModelSerializer):
    banner = CustomizationDataSerializer()
    background = CustomizationDataSerializer()

    class Meta:
        model = CustomizationSettings
        fields = '__all__'


class MinimalUserSerializer(ModelSerializer):
    profile_picture = ImageField(required=False)

    class Meta:
        model = User
        fields = (
            'id',
            'profile_picture',
            'username',
            'first_name',
            'last_name'
        )


class TransactionSerializer(ModelSerializer):
    from_user = MinimalUserSerializer()

    class Meta:
        model = Transaction
        fields = '__all__'


class AccountSerializer(ModelSerializer):
    history = SerializerMethodField()

    class Meta:
        model = Account
        fields = '__all__'

    def get_history(self, instance):
        return TransactionSerializer(instance.history.all()[:5], many=True).data


class LinksSerializer(ModelSerializer):
    class Meta:
        model = Links
        fields = (
            "youtube",
            "twitch",
            "website",
        )


class SubTierSerializer(ModelSerializer):
    class Meta:
        model = SubTier
        fields = (
            'uuid',
            'price',
            'currency',
            'title',
            'description'
        )


class SubInfoSerializer(ModelSerializer):
    tier = SubTierSerializer()
    subscriber = MinimalUserSerializer()
    target_user = MinimalUserSerializer()

    class Meta:
        model = SubInfo
        fields = '__all__'


class UserSerializer(MinimalUserSerializer):
    subscribers = SerializerMethodField()
    supporting = SerializerMethodField()
    password = CharField(write_only=True)
    email = CharField(write_only=True)
    customizing = CustomizationSettingsSerializer(required=False)
    sub_tiers = SerializerMethodField()
    links = LinksSerializer(required=False)
    active_subscription = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'about',
            'active_subscription',
            'username',
            'first_name',
            'last_name',
            'date_joined',
            'activity',
            'email',
            'verified',
            'links',
            'sub_tiers',
            'subscribers',
            'supporting',
            'password',
            'profile_picture',
            'customizing'
        )

    def create(self, validated_data):
        password = validated_data.pop('password')
        instance = self.Meta.model(**validated_data)
        instance.is_active = True
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def get_sub_tiers(self, instance):
        sub_tiers = instance.sub_tiers.all().order_by('price')
        return SubTierSerializer(sub_tiers, many=True).data

    def get_subscribers(self, instance):
        return len(instance.subscribers)

    def get_supporting(self, instance):
        try:
            return self.context['request'].user.is_supporting(instance)
        except KeyError:
            return False

    def get_active_subscription(self, instance):
        try:
            user = self.context['request'].user
            data = user.sub_info.filter(subscriber=user, target_user=instance).first()
            if data:
                return SubInfoSerializer(data).data
            return None
        except KeyError:
            return None


class AuthorizedUserSerializer(UserSerializer):
    accounts = AccountSerializer(many=True)
    history = SerializerMethodField()
    email = CharField()
    sub_info = SubInfoSerializer(many=True)

    class Meta:
        model = User
        fields = (
            'id',
            'about',
            'username',
            'accounts',
            'email',
            'first_name',
            'last_name',
            'date_joined',
            'activity',
            'about',
            'verified',
            'links',
            'sub_tiers',
            'sub_info',
            'supporting',
            'subscribers',
            'profile_picture',
            'history',
            'customizing'
        )

    def get_history(self, instance):
        total = []
        for account in instance.accounts.all():
            total += TransactionSerializer(account.history.all().order_by('-id')[:5], many=True).data
        return total


