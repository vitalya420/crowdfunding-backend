from rest_framework import serializers

from users.serializers import MinimalUserSerializer
from .models import Cart, DestinationAddress, Goods, Order, OrderLine


class GoodsSerializer(serializers.ModelSerializer):
    created_by = MinimalUserSerializer()

    class Meta:
        model = Goods
        fields = '__all__'


class DestinationAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = DestinationAddress
        fields = '__all__'


class CartCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class OrderLineSerializer(serializers.ModelSerializer):
    good = GoodsSerializer()

    class Meta:
        model = OrderLine
        fields = ['id', 'good', 'amount']
        read_only_fields = ['id', 'good']


class OrderSerializer(serializers.ModelSerializer):
    order_lines = OrderLineSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    order_lines = OrderLineSerializer(many=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = '__all__'

    def get_total(self, cart):
        return cart.calculate_total_price()
