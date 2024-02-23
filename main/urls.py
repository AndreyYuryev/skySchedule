from django.urls import path
from main.apps import MainConfig
from rest_framework.routers import DefaultRouter
from main.views import (LessonViewSet, CourseCreateAPIView, CourseDestroyAPIView,
                        CourseListAPIView, CourseUpdateAPIView, CourseRetriveAPIView)

app_name = MainConfig.name

router = DefaultRouter()
router.register(r'lessons', LessonViewSet, basename='lessons')

urlpatterns = [
                  path('course/create/', CourseCreateAPIView.as_view(), name='course_create'),
                  path('course/delete/<int:pk>/', CourseDestroyAPIView.as_view(), name='course_delete'),
                  path('course/', CourseListAPIView.as_view(), name='course_list'),
                  path('course/update/<int:pk>/', CourseUpdateAPIView.as_view(), name='course_update'),
                  path('course/<int:pk>/', CourseRetriveAPIView.as_view(), name='course_retrive'),
              ] + router.urls
