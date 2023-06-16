from rest_framework import status, viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView

from store.models import Goods, Cart, DestinationAddress, OrderLine
from store.serializers import GoodsSerializer

from .serializers import (
    CartSerializer,
    OrderSerializer,
    DestinationAddressSerializer,
    OrderLineSerializer
)


class UserGoodsView(ListAPIView):
    queryset = Goods.objects.all()

    def get(self, request, user_id):
        queryset = Goods.objects.all().filter(created_by=int(user_id))
        serializer = GoodsSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)


class UserGoodsCreateDeleteView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        serializer = GoodsSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        return Response(serializer.data)

    def delete(self, request, goods_id):
        goods = Goods.objects.get(pk=int(goods_id))
        goods.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DestinationAddressViewSet(viewsets.ModelViewSet):
    queryset = DestinationAddress.objects.all()
    serializer_class = DestinationAddressSerializer


class GoodsView(APIView):
    queryset = Goods.objects.all()

    def get(self, request, item_id):
        queryset = Goods.objects.get(pk=item_id)
        serializer = GoodsSerializer(queryset, context={'request': request})
        return Response(serializer.data)


class DestinationAddressView(CreateAPIView):
    serializer_class = DestinationAddressSerializer


class OrderView(CreateAPIView):
    serializer_class = OrderSerializer


class CartView(APIView):
    def get(self, request):
        user = request.user
        cart = Cart.objects.filter(user=user).first()

        if not cart:
            return Response({'error': 'User does not have a cart.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CartSerializer(cart, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, ):
        # book_id = request.qe.get('book_id')
        item_id = self.request.query_params.get('item_id')
        if not item_id:
            return Response({'error': 'Item ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        good = Goods.objects.get(id=item_id)

        # Check if the user has a cart
        user = request.user
        cart = Cart.objects.filter(user=user).first()

        if not cart:
            return Response({'error': 'User does not have a cart.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the book is in the cart and remove the order line
        order_line = cart.order_lines.filter(book=book).first()

        if order_line:
            cart.order_lines.remove(order_line)
            order_line.delete()

        serializer = CartSerializer(cart, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        item_id = request.data.get('item_id')
        if not item_id:
            return Response({'error': 'Item ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        item = Goods.objects.get(id=item_id)

        # Check if the user already has a cart
        user = request.user
        cart = Cart.objects.filter(user=user).first()

        if not cart:
            # Create a new cart if the user doesn't have one
            cart = Cart.objects.create(user=user)

        # Check if the book is already in the cart
        order_line = cart.order_lines.filter(good=item).first()

        if order_line:
            # If the book is already in the cart, update the order line's amount
            order_line.amount += 1
            order_line.save()
        else:
            # If the book is not in the cart, create a new order line and add it to the cart
            order_line = OrderLine.objects.create(good=item, amount=1)
            cart.order_lines.add(order_line)

        serializer = CartSerializer(cart, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartDetailView(APIView):
    def get(self, request):
        user = request.user
        cart = Cart.objects.filter(user=user).first()

        if not cart:
            return Response({'error': 'User does not have a cart.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CartSerializer(cart, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, orderline_id):
        user = request.user
        cart = Cart.objects.filter(user=user).first()

        if not cart:
            return Response({'error': 'User does not have a cart.'}, status=status.HTTP_400_BAD_REQUEST)

        order_line = cart.order_lines.filter(id=orderline_id).first()

        if not order_line:
            return Response({'error': 'Order line does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = OrderLineSerializer(order_line, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderCompleteView(APIView):
    def post(self, request):
        user = request.user
        cart = Cart.objects.filter(user=user).first()

        if not cart or not cart.order_lines.exists():
            return Response({'error': 'Cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)

        address_data = request.data.get('address')

        # Create the destination address
        destination_address = DestinationAddress.objects.create(
            user=user,
            address_line_1=address_data.get('address_line_1'),
            address_line_2=address_data.get('address_line_2', ''),
            city=address_data.get('city'),
            state=address_data.get('state'),
            postal_code=address_data.get('postal_code')
        )

        # Create the order
        order = Order.objects.create(
            user=user,
            address=destination_address,
        )

        order.order_lines.set(cart.order_lines.all())

        # Clear the cart
        cart.order_lines.clear()

        return Response({'message': 'Order completed successfully.'}, status=status.HTTP_200_OK)


class OrderListView(APIView):
    def get(self, request):
        user = request.user
        orders = Order.objects.filter(user=user)
        serializer = OrderSerializer(orders, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
