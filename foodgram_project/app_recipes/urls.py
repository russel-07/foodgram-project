from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_recipe/', views.create_recipe, name='create_recipe'),
]
