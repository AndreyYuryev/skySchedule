from django.shortcuts import render
from rest_framework import viewsets, generics
from users.serializer import UserSerializer
from users.models import User


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
