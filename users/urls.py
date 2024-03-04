from django.urls import path, include
from users.apps import UsersConfig
from rest_framework.routers import DefaultRouter, SimpleRouter
from users.views import UserViewSet, PaymentListAPIView, UserPaymentRetrieveAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = UsersConfig.name

router = SimpleRouter()
router.register(r'users', UserViewSet, basename='users')
print(router.urls)
urlpatterns = [
                  path('payment/', PaymentListAPIView.as_view(), name='payment_list'),
                  path('user/<int:pk>/payment', UserPaymentRetrieveAPIView.as_view(), name='user_payment'),
                  path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                  # path('api', include(router.urls)),
              ] + router.urls
