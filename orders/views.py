from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status as http_status

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
                return Order.objects.filter(driver=user) | Order.objects.filter(
                    driver__isnull=True, 
                    status__in=['Pending', 'Preparing']
                )
            
        if user.is_staff or user.is_superuser:
            return Order.objects.all()
        
        return Order.objects.none()
    
    # accept action by driver
    # (detail=True) -> address: /api/order/<id>/accept/
    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        order = self.get_object()
        user = request.user
        profile = getattr(user, 'profile', None)
        
        # check if user has logged in and role == driver
        if not profile or profile.role != 'driver':
            return Response({'error': 'Only drivers can accept orders.'}, status=http_status.HTTP_403_FORBIDDEN)
        
        # check if the order has not been taken by another driver
        if order.driver is not None:
            return Response({'error': 'This order has already been accepted by another driver.'}, status=http_status.HTTP_400_BAD_REQUEST)
        
        
        order.driver = user
        order.status = 'Out for Delivery' 
        order.save()
        
        serializer = self.get_serializer(order)
        return Response({'message': 'Order accepted successfully.', 'order': serializer.data})