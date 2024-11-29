

from django.contrib import admin
from .models import Order, Delivery  


# Custom admin for Order model
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_id",
        "product",
        "customer",
        "quantity_sold",
        "selling_price",
        "total_sale_value",
        "date_of_sale",
        "prime_delivery",
        "warehouse_location",
        "reseller_name",
        "commission_percentage",
        "coupon_used",
        "return_window",

    )

    ordering = ('date_of_sale',)  
    list_per_page = 25  


# Custom admin for Delivery model
class DeliveryAdmin(admin.ModelAdmin):
    list_display = (
        'order', 'delivery_address', 'delivery_date', 'delivery_status'
    )
    search_fields = ('order__order_id', 'order__product_name', 'delivery_address')
    list_filter = ('delivery_status',)
    list_per_page = 25

# Registering the models with the custom admin classes






admin.site.register(Order, OrderAdmin)
admin.site.register(Delivery)
