from rest_framework import serializers
from apps.account.models import Account

class AccountRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = ('phone_number', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('Passwords do not match')
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        account = Account.objects.create(**validated_data)
        return account