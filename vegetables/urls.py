from django.urls import path
from . import views

app_name = 'vegetables'

urlpatterns = [
    path('', views.home, name='home'),
    path('vegetables/', views.vegetable_list, name='vegetable_list'),
    path('vegetable/<slug:slug>/', views.vegetable_detail, name='vegetable_detail'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('add-to-cart/<int:vegetable_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart-item/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
]