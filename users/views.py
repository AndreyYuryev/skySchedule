from rest_framework import viewsets, generics
from users.serializer import UserSerializer, PaymentSerializer, UserPaymentSerializer
from users.models import User, Payment
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from users.permissions import IsCurrentUser
from users.services import (create_stripe_product, create_stripe_price,
                            create_stripe_session, get_stripe_session_status)
from lms.models import Lesson, Course


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsAuthenticated, ]
        elif self.action == 'create':
            permission_classes = [AllowAny, ]
        else:
            permission_classes = [IsAuthenticated, IsCurrentUser | IsAdminUser]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()

    def perform_update(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()


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


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        payment = serializer.save()
        if payment.paid_lesson:
            lesson = Lesson.objects.get(pk=payment.paid_lesson.pk)
            name = lesson.title
            description = lesson.description
        elif payment.paid_course:
            course = Course.objects.get(pk=payment.paid_course.pk)
            name = course.title
            description = course.description
        product_id = create_stripe_product(name=name, description=description)
        payment_price_id = create_stripe_price(payment.amount, product_id)
        payment.payment_link, payment.payment_id, payment.payment_status = create_stripe_session(payment_price_id)
        payment.save()


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        payment_id = kwargs.get('pk')
        payment = Payment.objects.get(pk=payment_id)
        if payment:
            payment.payment_status = get_stripe_session_status(payment.payment_id)
            payment.save()
        return self.retrieve(request, *args, **kwargs)
