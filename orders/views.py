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
                # Drivers see their own assigned deliveries OR pending/preparing orders that don't have a driver yet
                return Order.objects.filter(driver=user) | Order.objects.filter(
                    driver__isnull=True, 
                    status__in=['Pending', 'Preparing']
                )
        
        # Admins and superusers can see all orders
        if user.is_staff or user.is_superuser:
            return Order.objects.all()
        
        return Order.objects.none()
    
    
    # 1. Driver Accepts an Order
    # Endpoint: POST /api/order/<id>/accept/
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
        return Response({'message': 'Order successfully assigned to you and updated to "Out for Delivery".', 'order': serializer.data})
    
    
    # 2. Driver Marks Order as Delivered
    # Endpoint: POST /api/order/<id>/deliver/
    @action(detail=True, methods=['post'])
    def deliver(self, request, pk=None):
        order = self.get_object()
        user = request.user

        # Ensure only the assigned driver can mark it as delivered
        if order.driver != user:
            return Response(
                {'error': 'You are not the assigned driver for this order.'}, 
                status=http_status.HTTP_403_FORBIDDEN
            )

        # Ensure the order is currently out for delivery
        if order.status != 'Out for Delivery':
            return Response(
                {'error': 'Only orders with "Out for Delivery" status can be marked as delivered.'}, 
                status=http_status.HTTP_400_BAD_REQUEST
            )

        # Complete the delivery
        order.status = 'Delivered'  # Matching STATUS_CHOICES
        order.save()

        serializer = self.get_serializer(order)
        return Response({
            'message': 'Order successfully marked as Delivered.', 
            'order': serializer.data
        })