from django.shortcuts import render
from .models import CustomUser
from .serializers import UserSerializers,LoginSerializer
from rest_framework import viewsets
from django.contrib.auth import login ,logout
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .serializers import LoginSerializer

# Create your views here.

# class UserViewSet(viewsets.ModelViewSet):
#     queryset=CustomUser.objects.all()
#     serializer_class=UserSerializers



class RegisterView(APIView):
    serializer_class = UserSerializers

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user_data = serializer.validated_data
            email=user_data.pop('email')
            password = user_data.pop('password')
            confirm_password = user_data.pop('confirm_password')
            if password != confirm_password:
                return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Ensure 'email' is passed only once when creating the user
            user = CustomUser.objects.create_user(email, password, **user_data)
            
            # Generate token for the user
            token, created = Token.objects.get_or_create(user=user)
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    serializer_class=LoginSerializer
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            if(token):
                login(request,user)
            return Response({'message':"User logged in successfull",'token': token.key, 'user_id': user.id}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# from rest_framework.authtoken.views import AuthTokenViewSet
class UserLogoutViewSet(APIView):
    # def post(self, request, *args, **kwargs):
    #     if request.user:
    #         # Delete user's token
    #         Token.objects.filter(user=request.user).delete()
    #         # Logout the user
    #         logout(request)
    #         return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
    #     else:
    #         return Response({'message': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
     def post(self, request, *args, **kwargs):
        # Get and validate the token
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        if not token:
            return Response({'message': 'Missing token in authorization header'}, status=status.HTTP_401_UNAUTHORIZED)

        # Check if token is valid (use appropriate logic based on your authentication setup)
        if not self.token_validator(token):
            return Response({'message': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

        # Proceed with logout if token is valid
        logout(request)

        return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
    