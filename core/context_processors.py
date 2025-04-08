from django.conf import settings
from django.urls import reverse

def social_media_links(request):
    return {
        'twitter': getattr(settings, 'TWITTER', '#' ),
        'facebook': getattr(settings, 'FACEBOOK', '#'),
        'linkedin': getattr(settings, 'LINKEDIN', '#'),
        'youtube': getattr(settings, 'YOUTUBE', '#'),
        'instagram': getattr(settings, 'INSTAGRAM', '#'),
}

def common_links(request):
    return {
        'home_url': reverse('shopping:home'),
        'products_url': reverse('shopping:products'),
        'cart_url': reverse('shopping:cart'),
        'checkout_url': reverse('shopping:checkout'),
        'login_url': reverse('shopping:login'),
        'register_url': reverse('shopping:register'),
        'account_url': reverse('shopping:account'),
        'wishlist_url': reverse('shopping:wishlist'),
        'contact_url': reverse('shopping:contact'),
    }
