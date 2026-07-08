from rest_framework.viewsets import ModelViewSet

from .models import Order
from .serializers import OrderSerializer


# With ModelViewSet you get GET, POST, PUT/PATCH, DELETE ready to use
class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

