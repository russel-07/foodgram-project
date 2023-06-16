from django import forms
from .models import Recipe, Tag

class RecipeForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "tags__checkbox"}),
        to_field_name="pk", required=True,)

    class Meta:
        model = Recipe
        fields = ['name', 'tags', 'cook_time', 'description', 'image']
        #widgets = {'tags': forms.CheckboxSelectMultiple()}

    def save(self, author=None):
        recipe = super().save(commit=False)
        recipe.author = author
        recipe = super().save()
        return recipe
