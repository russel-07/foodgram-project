from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, FavoriteViewSet, FollowViewSet


router = DefaultRouter()
router.register('ingredients', IngredientViewSet, basename='Ingredient')
router.register('favorites', FavoriteViewSet, basename='Favorite')
router.register('follows', FollowViewSet, basename='Follow')


urlpatterns = [
    path('', include(router.urls)),
]
