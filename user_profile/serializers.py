from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer): 

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 
                  'first_name', 'last_name', 'password', 
                  'phone_number', 'is_email_verified', 
                  'is_superuser', 'is_staff', 
                  'created_at']
        extra_kwargs = {
            'password': {'write_only': True},
        } 


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
        }

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializer(self.user).data
        for k, v in serializer.items():
            data[k] = v
        return data


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'token']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)
    

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
