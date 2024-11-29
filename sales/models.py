from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    product_id = models.CharField(unique=True,max_length=255)
    product_name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Customer(models.Model):
    customer_id = models.CharField(unique=True,max_length=255)
    customer_name = models.CharField(max_length=255)
    contact_email = models.EmailField()
    phone_number = models.CharField(max_length=15)


class Platform(models.Model):
    platform_id = models.AutoField(primary_key=True)
    platform_name = models.CharField(max_length=100)
    seller_id = models.CharField(max_length=100)


class Order(models.Model):
    order_id = models.CharField(unique=True,max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity_sold = models.PositiveIntegerField()
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_sale_value = models.DecimalField(max_digits=15, decimal_places=2)
    date_of_sale = models.DateField()
    prime_delivery = models.CharField(max_length=100, null=True , blank=True)
    warehouse_location = models.CharField(max_length=100, null=True , blank=True)
    reseller_name = models.CharField(max_length=100, null=True , blank=True)
    commission_percentage = models.CharField(max_length=100, null=True , blank=True)
    coupon_used = models.CharField(max_length=100, null=True , blank=True)
    return_window = models.CharField(max_length=100, null=True , blank=True)
    platform = models.ForeignKey(Platform, on_delete=models.SET_NULL, null=True , blank=True)



class Delivery(models.Model):
    order = models.ForeignKey(Order, related_name="order_delivery", on_delete=models.CASCADE)
    delivery_address = models.TextField()
    delivery_date = models.DateField()
    delivery_status = models.CharField(max_length=50, choices=[
        ('Delivered', 'Delivered'),
        ('In Transit', 'In Transit'),
        ('Cancelled', 'Canceled')
    ])
    delivery_partner = models.CharField(max_length=100)

