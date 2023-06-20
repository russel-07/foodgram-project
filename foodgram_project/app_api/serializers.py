from rest_framework import serializers

from app_recipes.models import Ingredient, Favorite, Follow


class IngredientSerializer(serializers.ModelSerializer):
    unit = serializers.ReadOnlyField(source='unit.name', read_only=True)

    class Meta:
        fields = ['name', 'unit']
        model = Ingredient


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['user', 'recipe']
        model = Favorite
        read_only_fields = ['user', 'recipe']


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['user', 'author']
        model = Follow
        read_only_fields = ['user', 'author']
