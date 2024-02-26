from django.shortcuts import render
from rest_framework import viewsets, generics
from users.serializer import UserSerializer, PaymentSerializer, UserPaymentSerializer
from users.models import User, Payment
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['paid_course', 'paid_lesson', 'payment_type', ]
    # search_fields = ['field1', 'field2']
    ordering_fields = ['payment_date']


class UserPaymentRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserPaymentSerializer
    queryset = User.objects.all()
