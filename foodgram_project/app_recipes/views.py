from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import json

from .forms import RecipeForm
from .models import Recipe, RecipeIngredient, Tag


def index(request):
    return render(request, 'base.html')


@login_required
def recipe_create(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        form.save(author = request.user)
        return redirect('index')

    checked_tags = None
    if form['tags'].value():
        checked_tags = [int(val) for val in form['tags'].value()]

    selected_ingredients = None
    for key in form.data.keys():
        if key[:14] == 'nameIngredient':
            selected_ingredients = form.cleaned_data['ingredients']
            break

    context = {
        'page_title': 'Создание рецепта',
        'button': 'Создать рецепт',
        'form': form,
        'checked_tags': checked_tags,
        'selected_ingredients': selected_ingredients
    }

    return render(request, 'recipe_form.html', context)


@login_required
def recipe_edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user != recipe.author:
        return redirect("/")
    form = RecipeForm(request.POST or None, files=request.FILES or None,
                      instance=recipe)
    if form.is_valid():
        recipe.recipe_ingredients.all().delete()
        form.save(author=request.user)
        return redirect('recipe_view', recipe_id=recipe.id)
    form = RecipeForm(instance=recipe)
    context = {
        "page_title": "Редактирование рецепта",
        "button": "Сохранить",
        "form": form,
        "recipe": recipe,
        "edit": True,
    }

    return render(request, "recipe_form.html", context)


def recipe_view(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, 'recipe_view.html', {'recipe': recipe})

