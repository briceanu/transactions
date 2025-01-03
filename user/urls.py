from django.urls import path, include
from . import views


extra_patterns=[
    path('create',views.CreateUserAPI.as_view(),name='create_user'),
    path('list_users',views.ListUserAPI.as_view(),name='list_users'),
    path('update_user/<str:username>',views.UpdateUserAPIView.as_view(),name='update_user')
    ]


urlpatterns=[
    path('user/',include(extra_patterns))
    ]

