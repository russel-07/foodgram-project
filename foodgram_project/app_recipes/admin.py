from django.contrib import admin

from .models import Unit, Ingredient


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'unit')
    list_filter = ('name',)
    empty_value_display = '-пусто-'

