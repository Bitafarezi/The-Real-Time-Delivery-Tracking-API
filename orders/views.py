from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Order
from .serializers import OrderSerializer


# With ModelViewSet you get GET, POST, PUT/PATCH, DELETE ready to use
class OrderViewSet(ModelViewSet):
    # queryset = Order.objects.all()
    
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    
    # filter orders based on the role a user has
    def get_queryset(self):
        user = self.request.user
        
        profile = getattr(user, 'profile', None)
        
        if profile:
            if profile.role == "customer":
                return Order.objects.filter(customer=user)
            elif profile.role == "driver":
                return Order.objects.filter(driver=user)
            
        if user.is_staff or user.is_superuser:
            return Order.objects.all()
        
        return Order.objects.none()