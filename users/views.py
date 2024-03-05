from django.shortcuts import render
from rest_framework import viewsets, generics, status
from users.serializer import UserSerializer, PaymentSerializer, UserPaymentSerializer
from users.models import User, Payment
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from lms.permissions import IsOwner


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsAuthenticated, ]
        elif self.action == 'create':
            permission_classes = [AllowAny, ]
        else:
            permission_classes = [IsAuthenticated, IsAdminUser ]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()

    def perform_update(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()

    # def create(self, request, *args, **kwargs):
    #     serializer = UserSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     password = serializer.data["password"]
    #     user = User.objects.get(pk=serializer.data["id"])
    #     if user:
    #         user.set_password(password)
    #         user.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     user = User.objects.get(pk=kwargs.get('pk'))
    #     user.set_password(request.data.get('password'))
    #     request.data['password'] = user.password
    #     serializer = self.serializer_class(instance=instance,
    #                                        data=request.data,
    #                                        partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['paid_course', 'paid_lesson', 'payment_type', ]
    # search_fields = ['field1', 'field2']
    ordering_fields = ['payment_date']
    permission_classes = [IsAuthenticated, ]


class UserPaymentRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserPaymentSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, ]
