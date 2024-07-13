from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UsersListView.as_view(), name='users-list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='users-detail'),
]