from rest_framework import generics
from .models import User
from .serializers import UserSerializer


class CreateUserAPI(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ListUserAPI(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UpdateUserAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field='username'