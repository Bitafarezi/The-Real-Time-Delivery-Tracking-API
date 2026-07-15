from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import UserProfile, Order

User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']
        
        
class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)   # Shows users's info instead of numeric ID
    class Meta:
        model = UserProfile
        fields = ['user', 'role', 'phone_number', 'address']


class OrderSerializer(serializers.ModelSerializer):
    
    # we dont have this feild in database but we want to show to user
    delivery_duration = serializers.SerializerMethodField()
    
    customer_profile = UserProfileSerializer(source='customer.profile', read_only=True)
    driver_profile = UserProfileSerializer(source='driver.profile', read_only=True)
    
    def get_delivery_duration(self, obj):
        if obj.status == 'Pending':
            return "45-60 minutes"
        
        elif obj.status == 'Preparing':
            return "30-45 minutes"
        
        elif obj.status == 'Out for Delivery':
            return "10-20 minutes"
        
        return "Delivered"
    
    class Meta:
        model = Order
        fields = [
            'id', 'restaurant_name', 'address', 'status',
            'created_at', 'updated_at', 'delivery_duration',
            'customer', 'driver', 'customer_profile', 'driver_profile'
        ]
        
        read_only_fields = ['customer', 'driver', 'status']