from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import serializers
from app_recipes.models import Recipe, Ingredient, Favorite, Follow, Shoplist


User = get_user_model()


class IngredientViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.IngredientSerializer

    def get_queryset(self):
        query = self.request.query_params.get("query").lower()
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
        if author != user:
            serializer.save(user=user, author=author)

    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        author = kwargs['pk']
        follow = get_object_or_404(Follow, user=user, author=author)
        follow.delete()
        return Response(data={'success': True}, status=status.HTTP_200_OK)


class ShoplistViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Shoplist.objects.all()
    serializer_class = serializers.ShoplistSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Shoplist.objects.filter(user=user)
        return queryset

    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipe, id=self.request.data['id'])
        if self.request.user.is_authenticated:
            user = self.request.user
            serializer.save(user=user, recipe=recipe)
        elif 'recipes' not in self.request.session:
            self.request.session.set_expiry(0)
            self.request.session['recipes'] = [recipe.id]
        else:
            recipes = self.request.session['recipes']
            if recipe.id not in recipes:
                recipes.append(recipe.id)
                self.request.session['recipes'] = recipes

    def destroy(self, request, *args, **kwargs):
        recipe = kwargs['pk']
        if self.request.user.is_authenticated:
            user = self.request.user
            shoplist = get_object_or_404(Shoplist, user=user, recipe=recipe)
            shoplist.delete()
        else:
            recipes = self.request.session['recipes']
            recipes.remove(int(recipe))
            self.request.session['recipes'] = recipes

        return Response(data={'success': True}, status=status.HTTP_200_OK)
