from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated, AllowAny

from app_recipes.models import Recipe, Ingredient, Favorite
from .serializers import IngredientSerializer, FavoriteSerializer


class CreateRecipeIngredient(mixins.CreateModelMixin):
    def perform_create(self, serializer):
        recipe = Recipe.objects.get(id=self.request.data["id"])
        user = self.request.user
        serializer.save(user=user, recipes=recipe)
        return super().perform_create(serializer)


class IngredientViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = IngredientSerializer

    def get_queryset(self):
        query = self.request.query_params.get("query")
        queryset = Ingredient.objects.filter(name__startswith=query)
        return queryset


class FavoriteViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    lookup_field = 'id'

    def perform_create(self, serializer):
        recipe = Recipe.objects.get(id=self.request.data["id"])
        user = self.request.user
        serializer.save(user=user, recipe=recipe)
        return super().perform_create(serializer)
