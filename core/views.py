from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import Product, Order, OrderItem, Customer
from .serializers import ProductSerializer, UserRegisterSerializer, OrderSerializer
from .permissions import IsOwnerOrStaffForWrite
from rest_framework_simplejwt.views import TokenObtainPairView
from .auth_serializers import MyTokenObtainPairSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    s = UserRegisterSerializer(data=request.data)
    if s.is_valid():
        s.save()
        return Response(s.data, status=status.HTTP_201_CREATED)
    return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated & IsOwnerOrStaffForWrite]

    def get_queryset(self):
        tenant = getattr(self.request, 'tenant', None)
        if tenant:
            return Product.objects.filter(vendor=tenant)
        return Product.objects.none()

    def perform_create(self, serializer):
        serializer.save(vendor=self.request.tenant)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def place_order(request):
    tenant = request.tenant
    if not tenant:
        return Response({'detail':'Tenant not resolved'}, status=status.HTTP_400_BAD_REQUEST)
    items = request.data.get('items', [])
    if not items:
        return Response({'detail':'Provide items'}, status=status.HTTP_400_BAD_REQUEST)
    # get or create customer record for this user
    customer = None
    if request.user.role == 'customer':
        customer = getattr(request.user, 'customer_profile', None)
        if not customer:
            customer = Customer.objects.create(vendor=tenant, user=request.user)
    order = Order.objects.create(vendor=tenant, created_by=request.user, customer=customer)
    total = 0
    for it in items:
        pid = it.get('product_id')
        qty = int(it.get('qty', 1))
        try:
            prod = Product.objects.get(id=pid, vendor=tenant)
        except Product.DoesNotExist:
            order.delete()
            return Response({'detail':f'Product {pid} not found for this tenant'}, status=status.HTTP_400_BAD_REQUEST)
        OrderItem.objects.create(order=order, product=prod, quantity=qty, price=prod.price)
        total += prod.price * qty
    order.total = total
    order.save()
    return Response({'order_id': order.id, 'total': str(order.total)}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_orders(request):
    tenant = request.tenant
    if not tenant:
        return Response({'detail':'Tenant not resolved'}, status=status.HTTP_400_BAD_REQUEST)
    # owner and staff see all; customers — show their orders
    if request.user.role in ['owner','staff']:
        qs = Order.objects.filter(vendor=tenant)
    else:
        cust = getattr(request.user, 'customer_profile', None)
        qs = Order.objects.filter(vendor=tenant, customer=cust) if cust else Order.objects.none()
    serializer = OrderSerializer(qs, many=True)
    return Response(serializer.data)
