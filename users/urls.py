from django.urls import path
from users.apps import UsersConfig
from rest_framework.routers import SimpleRouter
from users.views import (UserViewSet, PaymentListAPIView, UserPaymentRetrieveAPIView,
                         PaymentCreateAPIView, PaymentRetrieveAPIView)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = UsersConfig.name

router = SimpleRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
                  path('payment/', PaymentListAPIView.as_view(), name='payment_list'),
                  path('payment/user/<int:pk>/', UserPaymentRetrieveAPIView.as_view(), name='user_payment'),
                  path('payment/create/', PaymentCreateAPIView.as_view(), name='payment_create'),
                  path('payment/detail/<int:pk>/', PaymentRetrieveAPIView.as_view(), name='payment_detail'),
                  path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
              ] + router.urls
