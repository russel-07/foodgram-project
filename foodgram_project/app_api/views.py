from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import serializers
from app_recipes.models import Recipe, Ingredient, Favorite, Follow


User = get_user_model()


class CreateRecipeIngredient(mixins.CreateModelMixin):
    def perform_create(self, serializer):
        recipe = Recipe.objects.get(id=self.request.data["id"])
        user = self.request.user
        serializer.save(user=user, recipes=recipe)
        return super().perform_create(serializer)


class IngredientViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.IngredientSerializer

    def get_queryset(self):
        query = self.request.query_params.get("query")
        queryset = Ingredient.objects.filter(name__startswith=query)
        return queryset


class FavoriteViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Favorite.objects.all()
    serializer_class = serializers.FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=self.request.data['id'])
        serializer.save(user=user, recipe=recipe)

    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        recipe = kwargs['pk']
        favorite = get_object_or_404(Favorite, user=user, recipe=recipe)
        favorite.delete()
        return Response(data={'success': True}, status=status.HTTP_200_OK)


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    queryset = Follow.objects.all()
    serializer_class = serializers.FollowSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        author = get_object_or_404(User, id=self.request.data['id'])
        serializer.save(user=user, author=author)

    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        author = kwargs['pk']
        follow = get_object_or_404(Follow, user=user, author=author)
        follow.delete()
        return Response(data={'success': True}, status=status.HTTP_200_OK)
