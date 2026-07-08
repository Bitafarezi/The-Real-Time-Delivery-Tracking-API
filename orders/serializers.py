from rest_framework import serializers

from .models import UserProfile, Order

class UserProfileSerializer(serializers.ModelSerializer):
    
    model = UserProfile
    fields = '__all__'
