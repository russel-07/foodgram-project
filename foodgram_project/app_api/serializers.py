from rest_framework import serializers

from app_recipes.models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    unit = serializers.ReadOnlyField(source='unit.name', read_only=True)

    class Meta:
        fields = ['name', 'unit']
        model = Ingredient
