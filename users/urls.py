from django.urls import path
from users.apps import UsersConfig
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, PaymentListAPIView, UserPaymentRetrieveAPIView

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
                  path('payment/', PaymentListAPIView.as_view(), name='payment_list'),
                  path('user/<int:pk>/payment', UserPaymentRetrieveAPIView.as_view(), name='user_payment')
              ] + router.urls
