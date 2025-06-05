from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal

class HomeSlider(models.Model):
    slider = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Products(models.Model):
    product_name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='products/')
    ex_price = models.CharField(max_length=200, blank=True, null=True)
    brand = models.CharField(max_length=200, blank=True, null=True)
    price = models.CharField(max_length=200)
    score = models.FloatField(default=0)
    details = models.TextField()
    description = models.TextField()
    specification = models.TextField()
    is_active = models.BooleanField(default=True)

    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.product_name


class Review(models.Model):
    product = models.ForeignKey(Products, related_name='reviews', on_delete=models.CASCADE)
    reviewer_name = models.CharField(max_length=100)
    reviewer_email = models.EmailField()
    content = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=5.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reviewer_name} - {self.product.product_name}"


class Brands(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ContactUs(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.name


class Subscriber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscribe')
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.email}"



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Cart"

    def get_subtotal(self):
        subtotal = Decimal('0')
        for item in self.items.all():
            if item.product.ex_price:  # Endirimli məhsul
                price_str = item.product.ex_price.replace('$', '')
            else:  # Endirimsiz məhsul
                price_str = item.product.price.replace('$', '')

            try:
                price = Decimal(price_str)
            except:
                price = Decimal('0')

            subtotal += price * item.quantity
        return subtotal

    def get_shipping_cost(self):
        shipping_cost = Decimal('0')
        for item in self.items.all():
            if item.product.ex_price:
                original_price = Decimal(item.product.price.replace('$', ''))
                discount_price = Decimal(item.product.ex_price.replace('$', ''))
                shipping_cost += (original_price - discount_price) * item.quantity
        return shipping_cost

    def get_total(self):
        total = sum(item.get_total_price() for item in self.items.all())
        return total

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Products', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.product.product_name} ({self.quantity})"

    def get_total_price(self):
        price_str = self.product.price.replace('$', '')
        try:
            price = Decimal(price_str)
        except Exception:
            price = Decimal('0')
        return price * self.quantity



class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wishlist')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Wishlist"

    def get_total_items(self):
        total = sum(item.quantity for item in self.items.all())
        return total

class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Products', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.product.product_name} ({self.quantity})"

