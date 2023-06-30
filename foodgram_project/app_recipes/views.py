from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import RecipeForm
from .models import Recipe
from .utils import (get_follows, get_shop_list, get_selected_ingredients,
                    get_favorites, get_pagination, get_checked_tags,
                    get_shoplist_file)


User = get_user_model()


def index(request):
    tags, get_tags = get_checked_tags(request)
    recipes = Recipe.objects.filter(tags__name__in=get_tags).distinct()
    page, paginator = get_pagination(request, recipes)
    favorites = get_favorites(request)
    shop_list = get_shop_list(request)
    context = {
        'page': page,
        'paginator': paginator,
        'tags': tags,
        'get_tags': get_tags,
        'favorites': favorites,
        'shop_list': shop_list
    }

    return render(request, 'index.html', context)


def recipe_view(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    favorites = get_favorites(request)
    shop_list = get_shop_list(request)
    follows = get_follows(request)
    context = {
        'recipe': recipe,
        'favorites': favorites,
        'shop_list': shop_list,
        'follows': follows
    }

    return render(request, 'recipe_view.html', context)


@login_required
def recipe_create(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        recipe = form.save(author = request.user)
        return redirect('recipe_view', recipe_id=recipe.id)
    selected_ingredients = get_selected_ingredients(form)################
    context = {
        'form': form,
        'selected_ingredients': selected_ingredients,
    }

    return render(request, 'recipe_form.html', context)


@login_required
def recipe_edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user != recipe.author:
        return redirect('index')
    form = RecipeForm(request.POST or None, files=request.FILES or None,
                      instance=recipe)
    if form.is_valid():
        recipe.recipe_ingredients.all().delete()
        form.save(author=request.user)
        return redirect('recipe_view', recipe_id=recipe.id)
    form = RecipeForm(instance=recipe)
    context = {
        'form': form,
        'recipe': recipe,
        'edit': True,
    }

    return render(request, 'recipe_form.html', context)


@login_required
def recipe_delete(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user != recipe.author:
        return redirect('index')
    recipe.delete()

    return redirect('index')


@login_required
def follows_view(request):
    follows = get_follows(request)
    authors = User.objects.filter(id__in=follows)
    page, paginator = get_pagination(request, authors)
    context = {
        'page': page,
        'paginator': paginator,
    }

    return render(request, 'follows_view.html', context)


@login_required
def favorites_view(request):
    tags, get_tags = get_checked_tags(request)
    favorites = get_favorites(request)
    recipes = Recipe.objects.filter(
        tags__name__in=get_tags, favorites__recipe__in=favorites).distinct()
    page, paginator = get_pagination(request, recipes)
    shop_list = get_shop_list(request)
    context = {
        'page': page,
        'paginator': paginator,
        'tags': tags,
        'get_tags': get_tags,
        'favorites': favorites,
        'shop_list': shop_list
    }

    return render(request, 'favorites_view.html', context)


def shoplist_view(request):
    shop_list = get_shop_list(request)
    recipes = Recipe.objects.filter(id__in=shop_list)

    return render(request, 'shoplist_view.html', {'recipes': recipes})


def shoplist_save(request):
    shop_list = get_shop_list(request)
    if shop_list:
        return get_shoplist_file(shop_list)
    else:
        return redirect('shoplist_view')


def profile_view(request, username):
    profile = get_object_or_404(User, username=username)
    tags, get_tags = get_checked_tags(request)
    recipes = Recipe.objects.filter(author=profile,
                                    tags__name__in=get_tags).distinct()
    page, paginator = get_pagination(request, recipes)
    follows = get_follows(request)
    favorites = get_favorites(request)
    context = {
        'page': page,
        'paginator': paginator,
        'tags': tags,
        'get_tags': get_tags,
        'profile': profile,
        'follows': follows,
        'favorites': favorites,
    }

    return render(request, 'profile_view.html', context)
