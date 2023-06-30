from django.core.paginator import Paginator
from django.http import HttpResponse
from django.db.models import Sum

from .models import RecipeIngredient, Tag


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


def get_pagination(request, objects):
    paginator = Paginator(objects, 6)
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


def get_shoplist_file(shop_list):
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

    response = HttpResponse(content_type='text/plain')  
    response['Content-Disposition']= 'attachment; filename="shoplist.txt"'
    response.write(output_text)

    return response
