from rest_framework import viewsets, mixins

from app_recipes.models import Recipe, Ingredient
from .serializers import IngredientSerializer


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
