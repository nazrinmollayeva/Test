from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect

from .models import HomeSlider, Products, Brands, Profile, Subscriber,\
    Cart, CartItem, Wishlist, WishlistItem, Category
from .forms import ContactForm, SubscribeForm, RegistrationForm, LoginForm,\
    ReviewForm
from django.core.paginator import Paginator
import random
from django.http import JsonResponse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
import os


def home_view(request):
    sliders = HomeSlider.objects.filter(is_active=True)

    featured_products = Products.objects.filter(ex_price__isnull=False).exclude(ex_price="")
    recent_products = Products.objects.filter(ex_price__isnull=True) | Products.objects.filter(ex_price="")
    brands = Brands.objects.all()

    subscriber_exists = False
    if request.user.is_authenticated:
        subscriber_exists = Subscriber.objects.filter(user=request.user).exists()

    subscribe_form = SubscribeForm()
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "Please login to subscribe.")
            return redirect('shopping:login')  # next nedir

        if not subscriber_exists:
            subscribe_form = SubscribeForm(request.POST)
            if subscribe_form.is_valid():
                subscriber = subscribe_form.save(commit=False)
                subscriber.user = request.user
                subscriber.save()

                template_path = os.path.join(settings.BASE_DIR, 'templates/subscribe_mail.html')
                html_message = render_to_string(template_path)
                plain_text = strip_tags(html_message)

                subject = "Subscription Successful"
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [subscriber.email]
                send_mail(
                    subject,
                    plain_text,
                    email_from,
                    recipient_list,
                    html_message=html_message
                )

                return redirect('shopping:home')

    return render(request, 'home.html', {
        'sliders': sliders,
        'featured_products': featured_products,
        'recent_products': recent_products,
        'brands': brands,
        'subscribe_form': subscribe_form,
        'subscriber_exists': subscriber_exists,
    })

# def product_view(request):
#     products_list = Products.objects.all()
#     featured_products = Products.objects.filter(ex_price__isnull=False).exclude(ex_price="")
#     brands = Brands.objects.all()
#
#     paginator = Paginator(products_list, 9)
#     page_number = request.GET.get('page', 1)
#     page_obj = paginator.get_page(page_number)
#
#     featured_product = random.choice(featured_products) if featured_products.exists() else None
#
#     return render(request, 'products.html', {
#         'page_obj':page_obj,
#         'featured_product': featured_product,
#         'brands': brands,
#         # 'page_obj': page_obj,
#     })

def product_view(request):
    category_id = request.GET.get('category')

    if category_id:
        if category_id == "all":
            products_list = Products.objects.all()
        else:
            products_list = Products.objects.filter(category__id=category_id)
    else:
        products_list = Products.objects.all()

    # if category_id is None:
    #     products_list = Products.objects.none()
    # else:
    #     if category_id == "all":
    #         products_list = Products.objects.all()
    #     else:
    #         products_list = Products.objects.filter(category__id=category_id)

    paginator = Paginator(products_list, 9)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    featured_products = Products.objects.filter(ex_price__isnull=False).exclude(ex_price="")
    featured_product = random.choice(featured_products) if featured_products.exists() else None
    brands = Brands.objects.all()
    categories = Category.objects.filter(is_active=True)

    return render(request, 'products.html', {
        'page_obj': page_obj,
        'featured_product': featured_product,
        'brands': brands,
        'categories': categories,
    })


def product_detail_view(request, post_id):
    products = Products.objects.all()
    product = get_object_or_404(Products, id=post_id)

    featured_products = Products.objects.filter(ex_price__isnull=False).exclude(ex_price="")
    featured_product = random.choice(featured_products) if featured_products.exists() else None
    categories = Category.objects.filter(is_active=True)

    brands = Brands.objects.all()

    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(request, 'Please login to submit a review.')
            return redirect('shopping:login')


        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.product = product
            review.save()
            return redirect('shopping:product_detail', post_id=product.id)
    else:
        review_form = ReviewForm()

    reviews = product.reviews.all().order_by('-created_at')

    return render(request, 'product-detail.html', {
        'products': products,
        'product':product,
        'featured_product': featured_product,
        'brands': brands,
        'reviews': reviews,
        'review_form': review_form,
        'categories': categories,
    })



@login_required
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()
            form = ContactForm()

            return render(request, 'contact.html', {'form': form})
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()

            Profile.objects.create(
                user=user,
                mobile=form.cleaned_data['mobile'],
            )

            login(request, user)

            return redirect('shopping:home')
    else:
        form=RegistrationForm()

    return render(request, 'login.html', {'form': form, 'register': True})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            return redirect('shopping:home')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form, 'register': False})

def logout_view(request):
    logout(request)
    return redirect('shopping:home')


def account_view(request):
    return render(request, 'my-account.html')


@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart.html', {'cart': cart})

@login_required
def add_to_cart(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Products, id=product_id)

        # İstifadəçinin cart-i yoxdursa, yaradırıq
        cart, created = Cart.objects.get_or_create(user=request.user)

        # Əgər məhsul artıq varsa, sadəcə miqdarı artırırıq
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

        data = {
            'status': 'ok',
            'message': f"{product.product_name} səbətə əlavə edildi.",
            'cart_total': cart.get_total(),
        }
        return JsonResponse(data)
    return JsonResponse({'status': 'fail', 'message': 'Invalid request'}, status=400)

@login_required
def update_cart_item(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        item_id = request.POST.get('item_id')
        action = request.POST.get('action')
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

        if action == 'increment':
            cart_item.quantity += 1
        elif action == 'decrement':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
        cart_item.save()

        data = {
            'status': 'ok',
            'quantity': cart_item.quantity,
            'item_total': cart_item.get_total_price(),
            'cart_total': cart_item.cart.get_total(),
        }
        return JsonResponse(data)
    return JsonResponse({'status': 'fail', 'message': 'Invalid request'}, status=400)

@login_required
def remove_cart_item(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        item_id = request.POST.get('item_id')
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        cart_item.delete()

        # Əlavə olaraq, istifadəçinin cart ümumi məbləğini hesablamaq üçün
        cart = get_object_or_404(Cart, user=request.user)
        data = {
            'status': 'ok',
            'message': f"Item silindi",
            'cart_total': cart.get_total() if cart.items.exists() else 0,
        }
        return JsonResponse(data)
    return JsonResponse({'status': 'fail', 'message': 'Invalid request'}, status=400)



@login_required
def wishlist_view(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    return render(request, 'wishlist.html', {'wishlist': wishlist})

@login_required
def add_to_wishlist(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Products, id=product_id)

        # İstifadəçinin wishlist-i yoxdursa, yaradırıq
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        # Əgər məhsul artıq varsa, miqdarı artırırıq
        wishlist_item, item_created = WishlistItem.objects.get_or_create(wishlist=wishlist, product=product)
        if not item_created:
            wishlist_item.quantity += quantity
        else:
            wishlist_item.quantity = quantity
        wishlist_item.save()

        data = {
            'status': 'ok',
            'message': f"{product.product_name} wishlist-ə əlavə edildi.",
            'total_items': wishlist.get_total_items(),
        }
        return JsonResponse(data)
    return JsonResponse({'status': 'fail', 'message': 'Invalid request'}, status=400)

@login_required
def update_wishlist_item(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        item_id = request.POST.get('item_id')
        action = request.POST.get('action')
        wishlist_item = get_object_or_404(WishlistItem, id=item_id, wishlist__user=request.user)

        if action == 'increment':
            wishlist_item.quantity += 1
        elif action == 'decrement':
            if wishlist_item.quantity > 1:
                wishlist_item.quantity -= 1
        wishlist_item.save()

        data = {
            'status': 'ok',
            'quantity': wishlist_item.quantity,
            'total_items': wishlist_item.wishlist.get_total_items()
        }
        return JsonResponse(data)
    return JsonResponse({'status': 'fail', 'message': 'Invalid request'}, status=400)

@login_required
def remove_wishlist_item(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        item_id = request.POST.get('item_id')
        wishlist_item = get_object_or_404(WishlistItem, id=item_id, wishlist__user=request.user)
        wishlist_item.delete()

        wishlist = get_object_or_404(Wishlist, user=request.user)
        data = {
            'status': 'ok',
            'message': "Item silindi",
            'total_items': wishlist.get_total_items() if wishlist.items.exists() else 0,
        }
        return JsonResponse(data)
    return JsonResponse({'status': 'fail', 'message': 'Invalid request'}, status=400)


@login_required
def move_to_cart(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        item_id = request.POST.get('item_id')
        wishlist_item = get_object_or_404(WishlistItem, id=item_id, wishlist__user=request.user)
        product = wishlist_item.product

        # İstifadəçinin cart‑ini əldə edirik (və ya yaratmaq)
        cart, created = Cart.objects.get_or_create(user=request.user)
        # Əgər məhsul artıq cart‑də varsa, miqdarı artırırıq, yoxsa yeni element yaradırıq
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += wishlist_item.quantity
        else:
            cart_item.quantity = wishlist_item.quantity
        cart_item.save()

        # İndi həmin wishlist elementini silirik
        wishlist_item.delete()

        data = {
            'status': 'ok',
            'message': f"{product.product_name} cart‑ə köçürüldü.",
            'cart_total': cart.get_total(),
        }
        return JsonResponse(data)
    return JsonResponse({'status': 'fail', 'message': 'Invalid request'}, status=400)


def checkout_view(request):
    return render(request, 'checkout.html')




