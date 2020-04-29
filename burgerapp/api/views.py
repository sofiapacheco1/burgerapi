from django.shortcuts import render
from rest_framework import viewsets, views, status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view, action
from .serializers import BurgerSerializer, IngredientSerializer
from .models import Burger, Ingredient


class BurgerViewSet(viewsets.ModelViewSet):
  queryset = Burger.objects.all()
  serializer_class = BurgerSerializer

  def retrieve(self, request, *args, **kwargs):
    # get hamburguesa/pk
    try:
      burger = Burger.objects.get(id=(int(kwargs['pk'])))
      serializer = self.get_serializer(burger)
      return Response({'status':200, 'message': 'operación exitosa',
          'body': serializer.data}, status=status.HTTP_200_OK)

    except Burger.DoesNotExist:
      return Response({'status': 404, 'message': 'hamburguesa inexistente'})

    except ValueError:
      return Response({'status':400, 'message':'id invalido'})
    

  def create(self, request):
    # post hamburguesa
    try:
      serializer = self.get_serializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      serializer.save()
      headers = self.get_success_headers(serializer.data)
      return Response({'status':201, 'message': 'hamburguesa creada',
        'body': serializer.data}, status=status.HTTP_201_CREATED, headers=headers)

    except: 
      return Response({'status': 400, 'message': 'input invalido'})


  def destroy(self, request, *args, **kwargs):
    # delete hamburguesa/pk
    try:
      burger = Burger.objects.get(id=(int(kwargs['pk'])))
      burger.delete()
      return Response({'status': 200, 'message': 'hamburguesa eliminada'})

    except Burger.DoesNotExist:
      return Response({'status': 404, 'message': 'hamburguesa inexistente'})


  def update(self, request, *args, **kwargs):
    # path hamburguesa/pk
    if 'id' in request.data.keys() or 'ingredientes' in request.data.keys():
      return Response({'status': 400, 'message': 'parámetros invalidos'})
    
    try:
      burger = Burger.objects.get(id=(int(kwargs['pk'])))
      serializer = self.get_serializer(burger, data=request.data, partial=True)
      serializer.is_valid(raise_exception=True)
      serializer.save()
      return Response({'status': 200, 'message': 'operación exitosa', 'body': serializer.data})
    
    except Burger.DoesNotExist:
      return Response({'status': 404, 'message': 'hamburguesa inexistente'})


  @action(methods=['PUT'], detail=True)
  def add_ingredient(self, request, *args, **kwargs):
    # put hamburguesa/pk/ingrediente/id
    try: 
      burger = Burger.objects.get(id=(int(kwargs['pk'])))
      ingredient = Ingredient.objects.get(id=(int(kwargs['id'])))

    except Burger.DoesNotExist:
      return Response({'status': 400, 'message': 'id de hamburguesa inválido'})
    
    except Ingredient.DoesNotExist: 
      return Response({'status': 404, 'message': 'ingrediente inexistente'})
    
    if request.method == 'PUT':
      burger.ingredientes.add(ingredient)
      serializer = BurgerSerializer
      return Response({'status': 201, 'message': 'ingrediente agregado'})


  @action(methods=['DELETE'], detail=True)
  def delete_ingredient(self, request, *args, **kwargs):
    # delete hamburguesa/pk/ingrediente/id
    try: 
      burger = Burger.objects.get(id=(int(kwargs['pk'])))
      ingredient = burger.ingredientes.get(id=(int(kwargs['id'])))

    except Burger.DoesNotExist:
      return Response({'status': 400, 'message': 'id de hamburguesa inválido'})
    
    except Ingredient.DoesNotExist:
      return Response({'status': 404, 'message': 'ingrediente inexistente en la hamburguesa'})
    
    if request.method == 'DELETE':
      burger.ingredientes.remove(ingredient)
      return Response({'status': 200, 'message': 'ingrediente retirado'})
      

class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    
    def create(self, request):
    # post ingrediente 
      try:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response({'status':201, 'message': 'ingrediente creado',
          'body': serializer.data}, status=status.HTTP_201_CREATED, headers=headers)

      except: 
        return Response({'status': 400, 'message': 'input invalido'})
    

    def retrieve(self, request, *args, **kwargs):
    # get ingrediente/pk
      try:
        ingredient = Ingredient.objects.get(id=(int(kwargs['pk'])))
        serializer = self.get_serializer(ingredient)
        return Response({'status':200, 'message': 'operación exitosa',
            'body': serializer.data}, status=status.HTTP_200_OK)

      except Ingredient.DoesNotExist:
        return Response({'status': 404, 'message': 'ingrediente inexistente'})

      except ValueError:
        return Response({'status':400, 'message':'id invalido'})
    

    def destroy(self, request, *args, **kwargs):
    # delete ingrediente/pk
      try:
        ingredient = Ingredient.objects.get(id=(int(kwargs['pk'])))

        if Burger.objects.filter(ingredientes__id=(int(kwargs['pk']))).exists():
          return Response({'status': 409,
            'message':'ingrediente no se puede borrar, se encuentra presente en una hamburguesa'})
        else:
          ingredient.delete()
          return Response({'status': 200, 'message': 'ingrediente eliminado'})

      except Ingredient.DoesNotExist:
        return Response({'status': 404, 'message': 'ingrediente inexistente'})
