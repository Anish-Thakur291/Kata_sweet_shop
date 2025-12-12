from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Sweet


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password_confirm']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({'password_confirm': 'Passwords do not match'})
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff']


class SweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sweet
        fields = ['id', 'name', 'description', 'category', 'price', 'quantity', 'image', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class PurchaseSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1, default=1)


class RestockSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)
