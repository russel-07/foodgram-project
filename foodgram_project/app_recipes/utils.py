from django.core.paginator import Paginator

from .models import Recipe, Tag


def get_favorites(request):
    favorites = []
    if request.user.is_authenticated:
        user = request.user
        favorites = user.favorites.all().values_list('recipe', flat=True)

    return favorites


def get_shop_list(request):
    shop_list = []
    if request.user.is_authenticated:
        user = request.user
        shop_list = user.shoplist.all().values_list('recipe', flat=True)

    return shop_list


def get_follows(request):
    follows = []
    if request.user.is_authenticated:
        user = request.user
        follows = user.follower.all().values_list('author', flat=True)

    return follows


def get_checked_tags(request):
    tags = Tag.objects.all()
    get_tags = request.GET.getlist('tag', tags.values_list('name', flat=True))

    return tags, get_tags


def get_pagination(request, objects, obj_per_page):
    paginator = Paginator(objects, obj_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return page, paginator


def get_selected_ingredients(form):
    selected_ingredients = None
    for key in form.data.keys():
        if key[:14] == 'nameIngredient':
            selected_ingredients = form.cleaned_data['ingredients']
            break

    return selected_ingredients
