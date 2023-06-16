from rest_framework import viewsets, mixins

from app_recipes.models import Ingredient
from .serializers import IngredientSerializer


class IngredientViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = IngredientSerializer

    def get_queryset(self):
        query = self.request.query_params.get("query")
        queryset = Ingredient.objects.filter(name__startswith=query).values('name', 'unit')
        print(queryset)
        return queryset
