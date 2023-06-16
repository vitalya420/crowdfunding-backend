from django.urls import path

from store.views import (
    UserGoodsView,
    GoodsView,
    CartView,
    OrderListView,
    DestinationAddressView,
    CartDetailView,
    OrderCompleteView
)

urlpatterns = [
    path('<int:user_id>/', UserGoodsView.as_view()),
    path('item/<item_id>/', GoodsView.as_view()),
    path('carts/', CartView.as_view(), name='cart-list'),
    path('carts/<int:orderline_id>', CartDetailView.as_view(), name='cart-detail'),
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('complete/', OrderCompleteView.as_view(), name='order-complete'),
    path('addresses/', DestinationAddressView.as_view(), name='address-create'),
]

