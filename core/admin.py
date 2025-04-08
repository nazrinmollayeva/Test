from django.contrib import admin
from .models import Products, Brands, ContactUs, Subscriber, HomeSlider\
    ,Review, Category

admin.site.register(HomeSlider)
admin.site.register(Products)
admin.site.register(Brands)
admin.site.register(ContactUs)
admin.site.register(Review)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'created_at')
    prepopulated_fields = {"slug": ("name",)}  #ad daxil olunduqda avtomatik slug yaranir
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')



class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'email', 'created_at')  # Custom user adı göstər
    search_fields = ('user__username', 'email')  # Axtarış üçün user adı və email

    def get_username(self, obj):
        return obj.user.username if obj.user else "Anonymous"
    get_username.short_description = "User"

admin.site.register(Subscriber, SubscriberAdmin)

