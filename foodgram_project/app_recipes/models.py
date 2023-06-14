from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Unit(models.Model):
    name = models.CharField(max_length=20, unique=True,
                            verbose_name='название')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'единица измерения'
        verbose_name_plural = 'единицы измерения'
        ordering = ['name']


class Ingredient(models.Model):
    name = models.CharField(max_length=50, unique=True,
                            verbose_name='название')
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE,
                             related_name="ingredients",
                             verbose_name='единицы измерения')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'
        ordering = ['name']


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True,
                            verbose_name='тег')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'
        ordering = ['name']


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes')
    name = models.CharField(max_length=50, unique=True,
                            verbose_name='название')
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    description = models.TextField(verbose_name='описание')
    ingredients = models.ManyToManyField(Ingredient, through='Recipe'
                                         'Ingredient', related_name='recipes')
    tag = models.ManyToManyField(Tag, related_name='recipes')
    cook_time = models.PositiveSmallIntegerField(verbose_name='время '
                                                 'приготовления')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'
        ordering = ['-pub_date']


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='recipe_ingredients',
                               verbose_name='рецепт')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   related_name='recipe_ingredients',
                                   verbose_name='ингредиент')
    amount = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ("recipe", "ingredient")
