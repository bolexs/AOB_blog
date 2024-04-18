from rest_framework import serializers
from .models import User, UserProfile, Profile
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=60, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'password': {'required': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class GetUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['profile_name']


class GetUserProfileSerializer(serializers.ModelSerializer):
    user = GetUserSerializer(read_only=True)
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'profile']

    def to_representation(self, value):

        if isinstance(value, User):
            serializer = GetUserSerializer(value)
        elif isinstance(value, Profile):
            serializer = ProfileSerializer(value)
        elif isinstance(value, UserProfile):
            serializer = super().to_representation(value)
            serializer['user'] = GetUserSerializer(value.user)
            serializer['profile'] = ProfileSerializer(value.profile)
        else:
            raise Exception('Unexpected type of tagged object')

        return serializer.data


class ActivateAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
    activation_code = serializers.IntegerField(min_value=1000, max_value=9999)

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token' : ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()
        
        except TokenError:
            return self.default_error_messages