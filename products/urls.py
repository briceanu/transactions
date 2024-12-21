from django.urls import path, include
from . import views

extra_patterns=[
    path('create',views.CreateProductAPI.as_view(),name='create_product'),
    path('list',views.ListProductAPI.as_view(),name='list_products')
    ]



urlpatterns = [
    path('product/',include(extra_patterns))
    ]