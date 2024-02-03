from django.contrib import admin
from . models import Product,UserProfile,Cart
from .models import Order, OrderItem
# Register your models here.
admin.site.register(Product)
admin.site.register(UserProfile)
admin.site.register(Cart)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'shipping_address', 'name', 'phone', 'pincode', 'total_price', 'created_at']
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)

