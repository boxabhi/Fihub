from rest_framework import serializers
from .models import Order, Product, Customer, Delivery, Category,Platform


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"

class CategorySerialier(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = '__all__'