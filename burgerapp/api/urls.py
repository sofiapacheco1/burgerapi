from django.urls import path, include
from rest_framework import routers
from . import views 

router = routers.DefaultRouter()
router.register(r'hamburguesa', views.BurgerViewSet)
router.register(r'ingrediente', views.IngredientViewSet)


urlpatterns = [
    path('', include(router.urls)),
    #path('hamburguesa/', views.BurgerAPIView.as_view())
    path('api/', include('rest_framework.urls', namespace='rest_framework')),
    path('hamburguesa/<int:pk>/ingrediente/<int:id>', 
        views.BurgerViewSet.as_view({'put': 'add_ingredient', 'delete': 'delete_ingredient'})),
    path('hamburguesa/<int:pk>',
        views.BurgerViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'patch': 'update'})),
    path('ingrediente/<int:pk>',
        views.IngredientViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'}))
]