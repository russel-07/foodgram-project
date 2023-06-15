from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'tag', 'cook_time', 'description', 'image']
        widgets = {'tag': forms.CheckboxSelectMultiple()}
