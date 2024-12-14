from rest_framework import serializers
from .models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, get_user_model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'profile_picture', 'followers']

class UserRegistrationSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'bio', 'profile_picture', 'first_name', 'last_name', 'token']

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username = validated_data['username'],
            email = validated_data.get('email', ''),
            password=validated_data['password'],
            bio=validated_data.get('bio', ''),
            profile_picture=validated_data.get('profile_picture', None),
            first_name = validated_data.get('first_name'), 
            last_name = validated_data.get('last_name')
        )
        Token.objects.create(user=user)
        return user
    
    def get_token(self, obj):
        token, _ = Token.objects.get_or_create(user=obj)
        return token.key
    
class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()
    token = serializers.SerializerMethodField()

    class Meta:
        model = User 
        fields = ['username', 'password', 'token']
        
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Invalid username or password")
        else:
            raise serializers.ValidationError("Both username and password are required")
        return data
    
    def get_token(self, obj):
        token, _ = Token.objects.get_or_create(user=self.user)
        return token.key
        