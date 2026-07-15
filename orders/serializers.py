from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import UserProfile, Order

User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']
        
        
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    
    # we dont have this feild in database but we want to show to user
    delivery_duration = serializers.SerializerMethodField()
    
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
        fields = '__all__'