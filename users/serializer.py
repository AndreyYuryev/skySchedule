from rest_framework import serializers
from users.models import User, Payment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            'password': {'write_only': True}
        }
        read_only_fields = [
            'is_staff', 'is_superuser', 'is_active', 'date_joined',
            'last_login', 'groups', 'user_permissions',
        ]


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class UserPaymentSerializer(serializers.ModelSerializer):
    payment = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'payment']

    def get_payment(self, instance):
        return PaymentSerializer(Payment.objects.filter(user=instance.pk), many=True).data
