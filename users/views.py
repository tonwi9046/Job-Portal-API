from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Profile
from .serializers import ProfileSerializer, RegisterSerializer

from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class ProfileListCreateView(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            return Response({
                'message': 'Login successful',
                'username': user.username
            })

        return Response({
            'message': 'Invalid username or password'
        }, status=status.HTTP_400_BAD_REQUEST)
