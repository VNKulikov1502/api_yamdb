from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import AuthTokenView, SignUpView, UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('auth/signup/', SignUpView.as_view(), name='signup'),
    path('auth/token/', AuthTokenView.as_view(), name='token_obtain_pair'),
]

urlpatterns += router.urls
