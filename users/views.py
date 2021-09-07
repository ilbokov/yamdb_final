from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .permissions import IsAdministrator
from .serializers import (LoginSerializer, RegistrationSerializer,
                          UserSerializer)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdministrator)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        methods=['GET', 'PATCH'],
        permission_classes=[permissions.IsAuthenticated],
        detail=False)
    def me(self, request):
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=True)
            serializer.is_valid()
            self.perform_create(serializer)
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class RegistrationViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer


class LoginView(TokenObtainPairView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer
