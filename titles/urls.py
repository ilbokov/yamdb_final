from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, GenreViewSet, TitleViewSet

router_v1 = DefaultRouter()
router_v1.register(r'categories', CategoryViewSet, 'categories')
router_v1.register(r'genres', GenreViewSet, 'genres')
router_v1.register(r'titles', TitleViewSet, 'titles')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
