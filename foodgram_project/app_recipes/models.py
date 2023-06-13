from django.db import models

class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='название')
    unit = models.CharField(max_length=100, verbose_name='единицы измерения')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'
        ordering = ['name']
