from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from rest_framework import status, views, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from .models import Burger, Ingredient
from .serializers import BurgerSerializer, IngredientSerializer


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
      return Response({'status': 404, 'message': 'hamburguesa inexistente'}, status=status.HTTP_404_NOT_FOUND)

    except ValueError:
      return Response({'status':400, 'message':'id invalido'}, status=status.HTTP_400_BAD_REQUEST)
    

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
      return Response({'status': 400, 'message': 'input invalido'}, status=status.HTTP_400_BAD_REQUEST)


  def destroy(self, request, *args, **kwargs):
    # delete hamburguesa/pk
    try:
      burger = Burger.objects.get(id=(int(kwargs['pk'])))
      burger.delete()
      return Response({'status': 200, 'message': 'hamburguesa eliminada'}, status=status.HTTP_200_OK)

    except Burger.DoesNotExist:
      return Response({'status': 404, 'message': 'hamburguesa inexistente'}, status=status.HTTP_404_NOT_FOUND)


  def update(self, request, *args, **kwargs):
    # path hamburguesa/pk
    if 'id' in request.data.keys() or 'ingredientes' in request.data.keys():
      return Response({'status': 400, 'message': 'parámetros invalidos'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
      burger = Burger.objects.get(id=(int(kwargs['pk'])))
      serializer = self.get_serializer(burger, data=request.data, partial=True)
      serializer.is_valid(raise_exception=True)
      serializer.save()
      return Response({'status': 200, 'message': 'operación exitosa', 'body': serializer.data}, status=status.HTTP_200_OK)
    
    except Burger.DoesNotExist:
      return Response({'status': 404, 'message': 'hamburguesa inexistente'}, status=status.HTTP_404_NOT_FOUND)


  @action(methods=['PUT'], detail=True)
  def add_ingredient(self, request, *args, **kwargs):
    # put hamburguesa/pk/ingrediente/id
    try: 
      burger = Burger.objects.get(id=(int(kwargs['pk'])))
      ingredient = Ingredient.objects.get(id=(int(kwargs['id'])))

    except Burger.DoesNotExist:
      return Response({'status': 400, 'message': 'id de hamburguesa inválido'}, status=status.HTTP_400_BAD_REQUEST)
    
    except Ingredient.DoesNotExist: 
      return Response({'status': 404, 'message': 'ingrediente inexistente'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
      burger.ingredientes.add(ingredient)
      serializer = BurgerSerializer
      return Response({'status': 201, 'message': 'ingrediente agregado'}, status=status.HTTP_201_CREATED)


  @action(methods=['DELETE'], detail=True)
  def delete_ingredient(self, request, *args, **kwargs):
    # delete hamburguesa/pk/ingrediente/id
    try: 
      burger = Burger.objects.get(id=(int(kwargs['pk'])))
      ingredient = burger.ingredientes.get(id=(int(kwargs['id'])))

    except Burger.DoesNotExist:
      return Response({'status': 400, 'message': 'id de hamburguesa inválido'}, status=status.HTTP_400_BAD_REQUEST)
    
    except Ingredient.DoesNotExist:
      return Response({'status': 404, 'message': 'ingrediente inexistente en la hamburguesa'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'DELETE':
      burger.ingredientes.remove(ingredient)
      return Response({'status': 200, 'message': 'ingrediente retirado'}, status=status.HTTP_200_OK)
      

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
        return Response({'status': 400, 'message': 'input invalido'}, status=status.HTTP_400_BAD_REQUEST)
    

    def retrieve(self, request, *args, **kwargs):
    # get ingrediente/pk
      try:
        ingredient = Ingredient.objects.get(id=(int(kwargs['pk'])))
        serializer = self.get_serializer(ingredient)
        return Response({'status':200, 'message': 'operación exitosa',
            'body': serializer.data}, status=status.HTTP_200_OK)

      except Ingredient.DoesNotExist:
        return Response({'status': 404, 'message': 'ingrediente inexistente'}, status=status.HTTP_404_NOT_FOUND)

      except ValueError:
        return Response({'status':400, 'message':'id invalido'}, status=status.HTTP_400_BAD_REQUEST)
    

    def destroy(self, request, *args, **kwargs):
    # delete ingrediente/pk
      try:
        ingredient = Ingredient.objects.get(id=(int(kwargs['pk'])))

        if Burger.objects.filter(ingredientes__id=(int(kwargs['pk']))).exists():
          return Response({'status': 409,
            'message':'ingrediente no se puede borrar, se encuentra presente en una hamburguesa'}, status=status.HTTP_409_CONFLICT)
        else:
          ingredient.delete()
          return Response({'status': 200, 'message': 'ingrediente eliminado'}, status=status.HTTP_200_OK)

      except Ingredient.DoesNotExist:
        return Response({'status': 404, 'message': 'ingrediente inexistente'}, status=status.HTTP_404_NOT_FOUND)
