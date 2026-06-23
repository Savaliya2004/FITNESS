from django.urls import path
from . import views

urlpatterns = [
    path('', views.store_home, name='store'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart/<int:product_id>/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('apply-coupon/', views.apply_coupon, name='apply_coupon'),
    path('coupons/', views.coupons_list, name='coupons_list'),
    path('place-order/', views.place_order, name='place_order'),
    path('order-success/', views.order_success, name='order_success'),
    path('my-orders/', views.my_orders, name='my_orders'),

    # Wishlist
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),

    # Membership & Razorpay Payments
    path('buy-membership/<int:pk>/', views.buy_membership, name='buy_membership'),
    path('membership/', views.membership_page, name='membership'),
    path('payment/create-order/', views.create_razorpay_order, name='create_razorpay_order'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/complete/', views.payment_complete, name='payment_complete'),
    path('payment/failed/', views.payment_failed, name='payment_failed'),
]
