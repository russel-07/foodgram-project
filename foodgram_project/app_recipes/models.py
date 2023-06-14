from django.db import models


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
                             related_name="units",
                             verbose_name='единицы измерения')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'
        ordering = ['name']
