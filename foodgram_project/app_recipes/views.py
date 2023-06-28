from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from .forms import RecipeForm
from .models import Recipe, RecipeIngredient
from .utils import (get_follows, get_shop_list, get_selected_ingredients,
                    get_favorites, get_checked_tags, get_pagination,
                    get_check_tags)


User = get_user_model()


def index(request):
    tags, get_tags = get_check_tags(request)
    recipes = Recipe.objects.filter(tags__name__in=get_tags).distinct()
    page, paginator = get_pagination(request, recipes, 3)
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
    checked_tags = get_checked_tags(form)########################
    selected_ingredients = get_selected_ingredients(form)################
    context = {
        'form': form,
        'checked_tags': checked_tags,
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
    page, paginator = get_pagination(request, authors, 3)
    context = {
        'page': page,
        'paginator': paginator,
    }

    return render(request, 'follows_view.html', context)


@login_required
def favorites_view(request):
    tags, get_tags = get_check_tags(request)
    favorites = get_favorites(request)
    recipes = Recipe.objects.filter(
        tags__name__in=get_tags, favorites__recipe__in=favorites).distinct()
    page, paginator = get_pagination(request, recipes, 3)
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
    ingredients = (
        RecipeIngredient.objects.values('ingredient__name',
                                        'ingredient__unit__name').
                                        filter(recipe__id__in=shop_list).
                                        annotate(total_amount=Sum('amount')).
                                        order_by('ingredient')
                                        )
    output_text = ('Данный список автоматически сгенерирован'
                   ' сервисом Foodgram.\n\nСписок покупок:\n')
    
    for i, ingredient in enumerate(ingredients, 1):
        output_text += (f'{i}. {ingredient["ingredient__name"]} - '
                        f'{ingredient["total_amount"]} '
                        f'{ingredient["ingredient__unit__name"]}\n')
    if shop_list:
        response = HttpResponse(content_type='text/plain')  
        response['Content-Disposition']= 'attachment; filename="shoplist.txt"'
        response.write(output_text)
        return response
    else:
        return redirect('shoplist_view')


def profile_view(request, username):
    profile = get_object_or_404(User, username=username)
    tags, get_tags = get_check_tags(request)
    recipes = Recipe.objects.filter(author=profile,
                                    tags__name__in=get_tags).distinct()
    page, paginator = get_pagination(request, recipes, 3)
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
