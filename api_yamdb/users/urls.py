from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('users', views.UserViewSet)

urlpatterns = [
    path('auth/signup/', views.SignUpView.as_view(), name='user-signup'),
    path('auth/token/', views.AuthTokenView.as_view(), name='user-token'),
    path('', include(router.urls)),
]
