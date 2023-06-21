from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('ingredients', views.IngredientViewSet, basename='Ingredient')
router.register('favorites', views.FavoriteViewSet, basename='Favorite')
router.register('follows', views.FollowViewSet, basename='Follow')
router.register('shoplist', views.ShoplistViewSet, basename='Shoplist')


urlpatterns = [
    path('', include(router.urls)),
]
