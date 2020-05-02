from django.urls import path, include
from rest_framework import routers
from . import views 

router = routers.DefaultRouter()
router.register(r'hamburguesa', views.BurgerViewSet)
router.register(r'ingrediente', views.IngredientViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api/', include('rest_framework.urls', namespace='rest_framework')),
    path('hamburguesa', views.BurgerViewSet.as_view({'post':'create'})),
    path('hamburguesa/<pk>/ingrediente/<id>', 
        views.BurgerViewSet.as_view({'put': 'add_ingredient', 'delete': 'delete_ingredient'})),
    path('hamburguesa/<pk>',
        views.BurgerViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'patch': 'update'})),
    path('ingrediente', views.IngredientViewSet.as_view({'post':'create'})),
    path('ingrediente/<pk>',
        views.IngredientViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'}))
]