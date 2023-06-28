from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from .forms import RecipeForm
from .models import Recipe, Tag, Follow, RecipeIngredient
from .utils import (get_follow_list, get_shop_list, get_selected_ingredients,
                    get_favorite_list, get_checked_tags, get_pagination, get_check_tags)


User = get_user_model()


def index(request):
    tags, get_tags = get_check_tags(request)
    recipes = Recipe.objects.filter(tags__name__in=get_tags).distinct()
    page, paginator = get_pagination(request, recipes, 3)
    favorites = get_favorite_list(request)
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
    favorites = get_favorite_list(request)
    shop_list = get_shop_list(request)
    follow = Follow.objects.filter(user=request.user,
                                   author=recipe.author).first()
    follow_list = get_follow_list(request)
    context = {
        'recipe': recipe,
        'favorites': favorites,
        'shop_list': shop_list,
        'follow': follow,
        'follow_list': follow_list
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


def follows_view(request):
    follow_list = get_follow_list(request)
    page, paginator = get_pagination(request, follow_list, 3)
    context = {
        'page': page,
        'paginator': paginator,
    }

    return render(request, 'follows_view.html', context)


def favorites_view(request):
    tags, get_tags = get_check_tags(request)
    favorites = get_favorite_list(request)
    recipes = Recipe.objects.filter(tags__name__in=get_tags, favorites__recipe__in=favorites).distinct()
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
    shoplist = get_shop_list(request)
    return render(request, 'shoplist_view.html', {'shoplist': shoplist})


def shoplist_save(request):
    shoplist = get_shop_list(request)
    shoplist_ingr = (
        RecipeIngredient.objects.values('ingredient__name',
                                        'ingredient__unit__name').
                                        filter(recipe__in=shoplist).
                                        annotate(total_amount=Sum('amount')).
                                        order_by('ingredient')
                                        )
    output_text = ('Данный список автоматически сгенерирован'
                   ' сервисом Foodgram.\n\nСписок покупок:\n')
    for i, ingredient in enumerate(shoplist_ingr, 1):
        output_text += (f'{i}. {ingredient["ingredient__name"]} - '
                        f'{ingredient["total_amount"]} '
                        f'{ingredient["ingredient__unit__name"]}\n')
    if shoplist:
        response = HttpResponse(content_type='text/plain')  
        response['Content-Disposition'] = 'attachment; filename="shoplist.txt"'
        response.write(output_text)
        return response
    else:
        return redirect('shoplist_view')


def profile_view(request, username):
    profile = get_object_or_404(User, username=username)
    tags, get_tags = get_check_tags(request)
    recipes = Recipe.objects.filter(author=profile, tags__name__in=get_tags).distinct()
    page, paginator = get_pagination(request, recipes, 3)
    follow = Follow.objects.filter(user=request.user,
                                   author=profile).first()
    follow_list = get_follow_list(request)
    favorites = get_favorite_list(request)
    context = {
        'page': page,
        'paginator': paginator,
        'tags': tags,
        'get_tags': get_tags,
        'profile': profile,
        'follow': follow,
        'follow_list': follow_list,
        'favorites': favorites,
    }

    return render(request, 'profile_view.html', context)
