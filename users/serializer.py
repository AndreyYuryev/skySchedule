from rest_framework import serializers
from users.models import User, Payment
from django.db import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        # fields = ['id', 'email', 'first_name', 'last_name', 'password', ]
        # fields = ['id', 'email', 'first_name', 'last_name',]
        # extra_kwargs = {
        #     'password': {
        #         'write_only': True,
        #         'style': {'input_type': 'password'}
        #     }
        # }

    # def create(self, validated_data):
    #     pswd = validated_data.pop('password')
    #     user = User.objects.create(**validated_data)
    #     user.set_password(pswd)
    #     user.save()
    #     return user

    # def list(self, validated_data):
    #     pass
    #
    # def retrieve(self, validated_data, pk=None):
    #     pass
    #
    # def update(self, validated_data, pk=None):
    #     user = User.objects.get(pk=pk)
    #     if user:
    #         print("user")
    #         user.update(**validated_data)
    #         user.save()
    #     return user
    #
    # def partial_update(self, validated_data, pk=None):
    #     user = User.objects.get(pk=pk)
    #     if user:
    #         print("user upd")
    #         user.update(**validated_data)
    #         user.save()
    #     return user
    #
    # def destroy(self, validated_data, pk=None):
    #     pass


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'password', ]


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
        return PaymentSerializer(Payment.objects.filter(user=instance), many=True).data
