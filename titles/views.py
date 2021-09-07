from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import PageNumberPagination

from users.permissions import IsAdminOrReadOnly

from .filters import TitleFilter
from .models import Category, Genre, Title
from .serializers import (
    CategorySerializer, GenreSerializer, TitleListSerializer,
    TitlePostSerializer,
)


class CustomViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return TitleListSerializer
        return TitlePostSerializer


class CategoryViewSet(CustomViewSet):
    queryset = Category.objects.all()
    lookup_field = "slug"
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class GenreViewSet(CustomViewSet):
    queryset = Genre.objects.all()
    lookup_field = "slug"
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
