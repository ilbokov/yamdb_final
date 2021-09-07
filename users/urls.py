from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import LoginView, RegistrationViewSet, UsersViewSet

router = DefaultRouter()
router.register(r'users', UsersViewSet, 'users')
router.register(r'auth/email', RegistrationViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path(
        'v1/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'v1/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path('v1/auth/token/', LoginView.as_view(), name='token_obtain_pair')
]
