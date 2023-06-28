from django.core.paginator import Paginator

from .models import Recipe, Tag


def get_favorite_list(request):
    favorite_list = []
    if request.user.is_authenticated:
        user = request.user
        favorites = user.favorites.all().values_list('recipe', flat=True)
        #favorite_list = Recipe.objects.filter(favorites__in=favorites)

    #return favorite_list
    return favorites


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

    return follow_list


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


def get_check_tags(request):
    tags = Tag.objects.all()
    get_tags = request.GET.getlist('tag', tags.values_list('name', flat=True))

    return tags, get_tags


def get_pagination(request, objects, obj_per_page):
    paginator = Paginator(objects, obj_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return page, paginator
