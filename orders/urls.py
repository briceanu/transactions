from django.urls import path
from . import views


urlpatterns = [
    path('order',views.PlaceOrderAPI.as_view(),name='place_order'),
    path('place_orders',views.PlaceOrderProductsAPI.as_view(),name='place_orders'),
    path('learn',views.LearnAPI.as_view(),name='learn'),
    path('list_orders',views.ListOrdersAPIView.as_view(),name='list_orders')


    ]

