from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,
         name='index'),
    path('recipe/create/', views.recipe_create,
         name='recipe_create'),
    path('recipe/<int:recipe_id>/', views.recipe_view,
         name='recipe_view'),
    path('recipe/<int:recipe_id>/edit/', views.recipe_edit,
         name='recipe_edit'),
    path('recipe/<int:recipe_id>/delete/', views.recipe_delete,
         name='recipe_delete'),
    path('favorites/', views.favorites_view,
         name='favorites_view'),
    path('shoplist/', views.shoplist_view,
         name='shoplist_view'),
    path('shoplist/save/', views.shoplist_save,
         name='shoplist_save'),

]
