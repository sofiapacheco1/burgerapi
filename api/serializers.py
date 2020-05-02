from rest_framework import serializers
from .models import Burger, Ingredient

url = 'https://burgerawesomeapi.herokuapp.com'

"""
[
  {
    "id": 1,
    "nombre": "De la casa",
    "precio": 5990,
    "descripcion": "Exquisita hamburguesa con queso y salsa BBQ, la especialidad de la casa",
    "imagen": "https://cdn.hswstatic.com/gif/cheeseburger-1.jpg",
    "ingredientes": [
      {
        "path": "https://hamburgueseria.com/ingrediente/1"
      }
    ]
  }
]
"""

class BurgerSerializer(serializers.HyperlinkedModelSerializer):
  ingredientes = serializers.SerializerMethodField()
  
  class Meta:
    model = Burger 
    fields = ('id','nombre', 'precio', 'descripcion', 'imagen', 'ingredientes')
    extra_kwargs = {'ingredientes': {'required': False}}
  
  def get_ingredientes(self, obj):
    path_ingredients = []
    ingredients = obj.ingredientes.all()
    for i in ingredients:
      path = url + 'ingrediente/' + str(i.id)
      path_dict = { 'path': path }
      path_ingredients.append(path_dict)
    return path_ingredients 
  

class IngredientSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Ingredient
    fields = ('id', 'nombre', 'descripcion')