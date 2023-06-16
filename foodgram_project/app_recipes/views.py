from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import RecipeForm
from .models import Tag


def index(request):
    return render(request, 'base.html')


@login_required
def create_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        form.save(author = request.user)
        return redirect('/')
    return render(request, 'formRecipe.html', {'form': form})
