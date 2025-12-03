from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, register, MyTokenObtainPairView, place_order, list_orders
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('auth/register/', register, name='register'),
    path('auth/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('', include(router.urls)),
    path('orders/place/', place_order, name='place_order'),
    path('orders/', list_orders, name='list_orders'),
]
