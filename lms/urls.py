from django.urls import path
from lms.apps import LmsConfig
from rest_framework.routers import DefaultRouter
from lms.views import (CourseViewSet, LessonListAPIView,
                       LessonCreateAPIView, LessonUpdateAPIView,
                       LessonDestroyAPIView, LessonRetriveAPIView,
                       SubscriptionListAPIView, SubscriptionCreateAPIView,
                       SubscriptionDestroyAPIView)

app_name = LmsConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
                  path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
                  path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson_delete'),
                  path('lesson/', LessonListAPIView.as_view(), name='lesson_list'),
                  path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson_update'),
                  path('lesson/<int:pk>/', LessonRetriveAPIView.as_view(), name='lesson_retrive'),
                  path('subscription/', SubscriptionListAPIView.as_view(), name='subscription_list'),
                  path('subscription/create/', SubscriptionCreateAPIView.as_view(), name='subscription_create'),
                  path('subscription/delete/<int:pk>/', SubscriptionDestroyAPIView.as_view(),
                       name='subscription_delete'),
              ] + router.urls
