from rest_framework import serializers
from .models import Product, Order, OrderItem, Customer, User, Vendor
from django.contrib.auth import get_user_model

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id','name','contact_email','domain']

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    vendor_id = serializers.IntegerField(write_only=True, required=False)
    class Meta:
        model = get_user_model()
        fields = ['id','username','password','email','role','vendor_id']
    def create(self, validated_data):
        vendor_id = validated_data.pop('vendor_id', None)
        password = validated_data.pop('password')
        user = get_user_model().objects.create(**validated_data)
        user.set_password(password)
        if vendor_id:
            from .models import Vendor
            user.vendor = Vendor.objects.filter(id=vendor_id).first()
        user.save()
        # if role == customer create Customer entry
        if user.role == 'customer' and user.vendor:
            Customer.objects.create(vendor=user.vendor, user=user)
        return user

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name','price','stock']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id','product','quantity','price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id','vendor','customer','created_by','total','status','items','created_at']
        read_only_fields = ['vendor','created_by','total','status','created_at']
