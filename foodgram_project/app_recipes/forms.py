from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'tags', 'cook_time', 'description', 'image']
        widgets = {'tags': forms.CheckboxSelectMultiple()}
