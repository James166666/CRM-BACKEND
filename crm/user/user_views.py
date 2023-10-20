from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .models import User
from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from datetime import datetime

from .serializers import UserSerializer

    
class CreateUser(APIView):

    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserSerializer(data=data)

        if serializer.is_valid():
            email = data.get('email')
            user_password = data.get('user_password')
            # Ensure to remove the email and password from the data to prevent duplication
            data.pop('email', None)
            data.pop('user_password', None)
            # Ensure to remove the password from the data to prevent it from being saved in plain text
            if 'user_password' in data:
                del data['user_password']
            user = User.objects.create_user(email=email, user_password=user_password, **data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # get all users' information
    def get(self, request, *args, **kwargs):
        userprofile = User.objects.all()
        serializer = UserSerializer(userprofile, many=True)
        return Response(serializer.data)
    


class RetrieveUserByPK(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        return Response(serializer.data)
    

class RetrieveLoggedInUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Access the user directly from the request
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    
    
class UserProfileUpdate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        data = request.data

        if data.get('email'):
            return Response({"detail": "Email cannot be modified."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(request.user, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        request.user.delete()
        return Response({'message': 'User was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    
    

class ResetPassword(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        if user.check_password(old_password):
            new_password = request.data.get('new_password')
            user.set_password(new_password)
            user.save()
            return Response({'message': "Password has been changed!"}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
    
class ResetPasswordWithoutOld(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    
    def put(self, request):
        new_password = request.data.get('new_password')
        email = request.data.get('email')
        user = User.objects.get(email = email)
        if user :
            user.set_password(new_password)
            user.save()
            return Response({'message': "Password has been changed!"}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)    
    

class Login(APIView):
    ###### DELETE and LOGOUT - did not achieve
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "message": 'Logged in successfully!'}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED) 

class Logout(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # simply delete the token to force a login
        request.auth.delete()
        return Response({"message": 'Logged out successfully!'}, status=status.HTTP_200_OK)   