from django.urls import path
from .views import home_view, product_view, product_detail_view,\
    contact_view, login_view, register_view, logout_view,account_view,\
    cart_view, add_to_cart, update_cart_item, remove_cart_item,\
     wishlist_view, add_to_wishlist, update_wishlist_item, remove_wishlist_item,\
    move_to_cart, checkout_view

app_name = 'shopping'


urlpatterns = [
    path('', home_view, name='home'),
    path('products/', product_view, name='products'),
    path('product/<int:post_id>/', product_detail_view, name='product_detail'),
    path('contact/', contact_view, name='contact'),

    path('register/', register_view, name='register'),
    path("login/", login_view, name="login"),
    path('accounts/login/', login_view, name='login'),
    path("logout/", logout_view, name="logout"),
    path('my-account/', account_view, name='account'),

    path('cart/', cart_view, name='cart'),
    path('ajax/add_to_cart/', add_to_cart, name='add_to_cart'),
    path('ajax/update_cart_item/', update_cart_item, name='update_cart_item'),
    path('ajax/remove_cart_item/', remove_cart_item, name='remove_cart_item'),

    path('wishlist/', wishlist_view, name='wishlist'),
    path('ajax/add_to_wishlist/', add_to_wishlist, name='add_to_wishlist'),
    path('ajax/update_wishlist_item/', update_wishlist_item, name='update_wishlist_item'),
    path('ajax/remove_wishlist_item/', remove_wishlist_item, name='remove_wishlist_item'),

    path('ajax/move_to_cart/', move_to_cart, name='move_to_cart'),

    path('checkout/', checkout_view, name='checkout'),
]

