from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_recipe/', views.recipe_create, name='recipe_create'),
    path('recipe/<int:recipe_id>/', views.recipe_view, name='recipe_view'),
    path('recipe/<int:recipe_id>/edit/', views.recipe_edit, name='recipe_edit'),
]
