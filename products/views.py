from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer


class ListProductAPI(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer



class CreateProductAPI(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer