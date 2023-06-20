from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, FavoriteViewSet


router = DefaultRouter()
router.register('ingredients', IngredientViewSet, basename='Ingredient')
router.register('favorites', FavoriteViewSet, basename='Favorite')


urlpatterns = [
    path('', include(router.urls)),
]
