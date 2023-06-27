from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from .forms import RecipeForm
from .models import Recipe, Tag, Follow, RecipeIngredient


User = get_user_model()


def index(request):
    get_tags = request.GET.getlist('get_tags', (1, 2, 3))
    print('>>>>>>>>>>>>>>>>>>>>>>')
    print(get_tags)

    recipes = Recipe.objects.filter(tags__in=get_tags).distinct()

    tags = Tag.objects.all
    favorite_list = get_favorite_list(request)
    shop_list = get_shop_list(request)
    get_tags = [int(v) for v in get_tags]
    context = {
        'recipes': recipes,
        'tags': tags,
        'get_tags': get_tags,
        'favorite_list': favorite_list,
        'shop_list': shop_list
    }

    return render(request, 'index.html', context)


def index2(request):
    recipes = Recipe.objects.all
    favorite_list = get_favorite_list(request)
    shop_list = get_shop_list(request)
    context = {
        'recipes': recipes,
        'favorite_list': favorite_list,
        'shop_list': shop_list
    }

    return render(request, 'index.html', context)


def recipe_view(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    favorite_list = get_favorite_list(request)
    shop_list = get_shop_list(request)
    follow = Follow.objects.filter(user=request.user,
                                   author=recipe.author).first()
    follow_list = get_follow_list(request)
    context = {
        'recipe': recipe,
        'favorite_list': favorite_list,
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
    checked_tags = get_checked_tags(form)
    selected_ingredients = get_selected_ingredients(form)
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
    context = {
        'follow_list': follow_list,
    }

    return render(request, 'follows_view.html', context)


def favorites_view(request):
    favorite_list = get_favorite_list(request)
    shop_list = get_shop_list(request)
    context = {
        'recipes': favorite_list,
        'favorite_list': favorite_list,
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
    recipes = Recipe.objects.filter(author=profile)
    follow = Follow.objects.filter(user=request.user,
                                   author=profile).first()
    follow_list = get_follow_list(request)
    context = {
        'profile': profile,
        'recipes': recipes,
        'follow': follow,
        'follow_list': follow_list
    }

    return render(request, 'profile_view.html', context)





def get_favorite_list(request):
    favorite_list = []
    if request.user.is_authenticated:
        user = request.user
        favorites = user.favorites.all()
        favorite_list = Recipe.objects.filter(favorites__in=favorites)

    return favorite_list


def get_shop_list(request):
    shop_list = []
    if request.user.is_authenticated:
        user = request.user
        list = user.shoplist.all()
        shop_list = Recipe.objects.filter(shoplist__in=list)

    return shop_list


def get_follow_list(request):
    follow_list = []
    if request.user.is_authenticated:
        user = request.user
        follow_list = user.follower.all()
        #following = user.following.all()
        #print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        #print(following)
        #follow_list = Recipe.objects.filter(following__in=following)
        #print(follow_list)

    return follow_list


def get_is_follow(request, author):
    is_follow = None
    if request.user.is_authenticated:
        user = request.user
        is_follow = Follow.objects.filter(user=user, author=author).exists()

    return is_follow


def get_checked_tags(form):
    checked_tags = None
    if form['tags'].value():
        checked_tags = [int(val) for val in form['tags'].value()]

    return checked_tags


def get_selected_ingredients(form):
    selected_ingredients = None
    for key in form.data.keys():
        if key[:14] == 'nameIngredient':
            selected_ingredients = form.cleaned_data['ingredients']
            break

    return selected_ingredients
