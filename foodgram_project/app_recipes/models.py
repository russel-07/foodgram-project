from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Unit(models.Model):
    name = models.CharField('Название', max_length=20, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'
        ordering = ['name']


class Ingredient(models.Model):
    name = models.CharField('Название', max_length=50, unique=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE,
                             related_name="ingredients",
                             verbose_name='Единицы измерения')

    def __str__(self):
        return f'{self.name}, {self.unit}'

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']


class Tag(models.Model):
    name = models.CharField('Название', max_length=50, unique=True)
    color = models.CharField('Цветовой код', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['name']


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes',
                               verbose_name='Автор')
    name = models.CharField('Название', max_length=50)
    image = models.ImageField('Картинка', upload_to='recipes/',
                              blank=True, null=True)
    description = models.TextField('Описание')
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient',
                                         related_name='recipes')
    tags = models.ManyToManyField(Tag, related_name='recipes',
                                  verbose_name='Теги')
    cook_time = models.PositiveSmallIntegerField('Время приготовления')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='recipe_ingredients',
                               verbose_name='Рецепт')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   related_name='recipe_ingredients',
                                   verbose_name='Ингредиент')
    amount = models.DecimalField('Количество', max_digits=6, decimal_places=2)

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецептов'
        unique_together = ('recipe', 'ingredient')
