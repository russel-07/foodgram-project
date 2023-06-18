from django.contrib import admin

from . import models


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'pub_date',)
    search_fields = ('name',) 
    list_filter = ('author', 'pub_date')
    empty_value_display = '-пусто-'


@admin.register(models.RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient', 'amount')
    list_filter = ('recipe',)
    empty_value_display = '-пусто-'


@admin.register(models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'unit')
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(models.Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color')
