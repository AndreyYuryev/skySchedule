from django.shortcuts import render
from rest_framework import viewsets, generics
from main.serializer import LessonSerializer, CourseSerializer
from main.models import Lesson, Course


class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class CourseCreateAPIView(generics.CreateAPIView):
    serializer_class = CourseSerializer


class CourseDestroyAPIView(generics.DestroyAPIView):
    queryset = Course.objects.all()


class CourseRetriveAPIView(generics.RetrieveAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class CourseListAPIView(generics.ListAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class CourseUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
