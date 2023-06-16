from django import forms
from .models import Recipe, Ingredient, Tag, RecipeIngredient


def get_form_ingredients(ingredients, recipe):
    result = list()
    for ingr in ingredients:
        ingredient = Ingredient.objects.get(name=ingr["name"],
                                            unit=ingr["unit"])
        result.append(RecipeIngredient(recipe=recipe, ingredient=ingredient,
                                       amount=ingr["amount"]))
    return result


class RecipeForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "tags__checkbox"}),
        to_field_name="pk", required=True,)

    class Meta:
        model = Recipe
        fields = ['name', 'tags','cook_time',
                  'description','image']
        #widgets = {'tags': forms.CheckboxSelectMultiple()}
    
    def clean_ingredients(self):
        ingredient_names = [self.data[key] for key in self.data
                            if key.startswith("nameIngredient_")]
        ingredient_units = [self.data[key] for key in self.data
                            if key.startswith("unitsIngredient_")]
        ingredient_quantities = [self.data[key] for key in self.data
                                 if key.startswith("valueIngredient_")]
        ingredients_clean = []

        for ingredient in zip(ingredient_names, ingredient_units,
                              ingredient_quantities):
            if not int(ingredient[2]) > 0:
                raise forms.ValidationError("Количество ингредиентов должно"
                                            " быть больше нуля.")
            elif not Ingredient.objects.filter(name=ingredient[0]).exists():
                raise forms.ValidationError("Ингредиенты должны"
                                            " быть из списка")
            else:
                ingredients_clean.append({"name": ingredient[0],
                                          "unit": ingredient[1],
                                          "amount": ingredient[2]})
        if len(ingredients_clean) == 0:
            raise forms.ValidationError("Добавьте ингредиент")
        return ingredients_clean

    def save(self, author=None):
        recipe = super().save(commit=False)
        recipe.author = author
        #ingredients = self.cleaned_data["ingredients"]
        #print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        #print(get_form_ingredients(ingredients, recipe))
        #print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        #self.cleaned_data["ingredients"] = []
        recipe = super().save()

        #RecipeIngredient.objects.bulk_create(get_form_ingredients
        #                                     (ingredients, recipe))
        return recipe
