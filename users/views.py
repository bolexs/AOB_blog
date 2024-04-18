from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics, permissions, views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import RegistrationSerializer, LogoutSerializer, ActivateAccountSerializer, GetUserSerializer, GetUserProfileSerializer
from drf_yasg.utils import swagger_auto_schema
from .models import User, UserProfile
from common.utils import get_last_serializer_error

class RegistrationAPIView(generics.GenericAPIView):
    """create a user account"""
    serializer_class = RegistrationSerializer
    permission_classes = []
    @swagger_auto_schema(tags=['Users'])
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(TokenObtainPairView):
    @swagger_auto_schema(tags=['Users'])
    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)


class ActivateAccountAPIView(views.APIView):
    @swagger_auto_schema(tags=['Users'])
    def post(self, request, *args, **kwargs):
        serializer = ActivateAccountSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            activation_code = serializer.validated_data['activation_code']
            # validate email and activation code

            try:
                user = User.objects.get(email=email)
                profile = UserProfile.objects.get(user=user)
                if user.is_active:
                    return Response({
                        "message": "Account is already activated",
                        "data": {},
                        "status": False,
                        "status_code": 400
                    }, status=status.HTTP_400_BAD_REQUEST)

                if profile.activation_code == activation_code:
                    # activate account
                    profile.is_active = True
                    profile.activation_code = None
                    user.is_active = True
                    user.save()
                    profile.save()
                    return Response({
                        "message": "Account activated successfully",
                        "data": {},
                        "status": True,
                        "status_code": 200
                    }, status=status.HTTP_200_OK)

                else: 
                    return Response({
                        "message": "Invalid activation code",
                        "data": {},
                        "status": False,
                        "status_code": 400
                    }, status=status.HTTP_400_BAD_REQUEST)
                
            except User.DoesNotExist:
                return Response({
                    "message": "Invalid email address",
                    "data": {},
                    "status": False,
                    "status_code": 400
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "message": get_last_serializer_error(serializer.errors),
                "data": {},
                "status": False,
                "status_code": 400
            }, status=status.HTTP_400_BAD_REQUEST)