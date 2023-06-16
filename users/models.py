import uuid as uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)


class CustomizationData(models.Model):
    type = models.IntegerField(choices=[
        (0, 'Color'), (1, 'Gradient'), (2, 'Image'),
    ])
    data = models.CharField(max_length=255, null=True, default=True)
    image = models.ImageField(upload_to=upload_to, null=True, default=None)
    mask = models.CharField(max_length=255)
    mask_opacity = models.FloatField(null=True, default=0)


class CustomizationSettings(models.Model):
    banner_enabled = models.BooleanField(default=False)
    banner_width_mode = models.IntegerField(choices=[
        (0, 'Full'), (1, 'Container'),
    ], default=1)
    banner = models.ForeignKey(CustomizationData, on_delete=models.CASCADE, related_name='banner',
                               null=True, default=None)
    background_enabled = models.BooleanField(default=False)
    background = models.ForeignKey(CustomizationData, on_delete=models.CASCADE, related_name='background',
                                   null=True, default=None)


class Transaction(models.Model):
    transaction_type = models.IntegerField([
        (0, "Subscription"),
        (1, 'One time payment')
    ])
    from_user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, default=None)
    amount = models.FloatField()
    currency = models.CharField(max_length=5)


class Account(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, max_length=36)
    balance = models.FloatField(default=0.0)
    currency = models.CharField(null=True, max_length=5, default='USD')
    history = models.ManyToManyField(Transaction)
    # TODO: transactions, saved info


class Links(models.Model):
    youtube = models.CharField(max_length=128, default=None, null=True)
    twitch = models.CharField(max_length=128, default=None, null=True)
    website = models.CharField(max_length=128, default=None, null=True)


class SubTier(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, max_length=36)
    price = models.FloatField(null=True, default=True)
    currency = models.CharField(null=True, max_length=5, default='USD')
    title = models.CharField(max_length=32, default='Subscription')
    description = models.TextField(max_length=1000, null=True, default=None)


class SubInfo(models.Model):
    date = models.DateField(auto_now=True)
    subscriber = models.ForeignKey('User', on_delete=models.CASCADE, null=True, default=True, related_name='subscriber')
    target_user = models.ForeignKey("User", on_delete=models.CASCADE)
    tier = models.ForeignKey(SubTier, on_delete=models.CASCADE, default=None, null=True)


class User(AbstractUser):
    accounts = models.ManyToManyField(Account)
    activity = models.CharField(default='Good person', max_length=300)
    about = models.TextField(default=None, null=True)
    verified = models.BooleanField(default=False)
    links = models.ForeignKey(Links, on_delete=models.CASCADE, null=True, default=None)
    sub_tiers = models.ManyToManyField(SubTier)
    sub_info = models.ManyToManyField('SubInfo')
    profile_picture = models.ImageField(upload_to=upload_to, blank=True, null=True)
    customizing = models.ForeignKey(CustomizationSettings, on_delete=models.CASCADE, default=None, null=True)

    @property
    def subscribers(self):
        return SubInfo.objects.all().filter(target_user=self)

    def create_new_sub_tier(self, *, price, currency, title, description):
        if not self.has_account_in_this_currency(currency):
            self.create_account(currency)
        if len(self.sub_tiers.all()) >= 3:
            return self
        sub_tier = SubTier.objects.create(price=price, currency=currency, title=title, description=description)
        self.sub_tiers.add(sub_tier)
        self.save()
        return self

    def has_account_in_this_currency(self, currency):
        if self.accounts.all().filter(currency=currency):
            return True

    def create_account(self, currency):
        account = Account.objects.create(currency=currency)
        self.accounts.add(account)
        self.save()
        return self

    def add_link(self, **kwargs):
        if not self.links:
            self.links = Links.objects.create(**kwargs)
        for kwarg in kwargs:
            if hasattr(self.links, kwarg):
                setattr(self.links, kwarg, kwargs[kwarg])
        self.save()
        return self

    def delete_sub_tier(self, _uuid):
        subs = self.sub_tiers.all().filter(uuid=_uuid).all()
        for sub in subs:
            sub.delete()
        self.save()
        return self

    def is_subscribed(self, target_user):
        return not not self.sub_info.all().filter(target_user=target_user)

    def sub_to_user(self, target_user, tier: SubTier):
        if self.is_subscribed(target_user):
            return
        sub_info = SubInfo.objects.create(target_user=target_user, tier=tier, subscriber=self)
        target_user.add_transaction(self, tier.price, tier.currency)
        self.sub_info.add(sub_info)
        self.save()

    def add_transaction(self, from_user, amount, currency):
        transaction = Transaction.objects.create(
            transaction_type=0,
            from_user=from_user,
            amount=amount,
            currency=currency
        )
        account = self.accounts.all().filter(currency=currency).first()
        account.balance += amount
        account.history.add(transaction)
        account.save()

    def cancel_sub(self, sub_id):

        sub = self.sub_info.get(pk=sub_id)
        sub.delete()
        self.save()
        return self

    def is_supporting(self, target_user):
        return not not self.sub_info.all().filter(target_user=target_user)
