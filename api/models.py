from django.db import models

# Create your models here.
class Ingredient(models.Model):
  nombre = models.CharField(max_length=100)
  descripcion = models.TextField(max_length=100)

 
class Burger(models.Model):
  nombre = models.CharField(max_length=100)
  precio = models.IntegerField()
  descripcion = models.TextField(max_length=100)
  imagen = models.URLField(max_length=100)
  
  ingredientes = models.ManyToManyField('Ingredient', related_name='burgers', blank=True)
