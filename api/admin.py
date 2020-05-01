from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Burger)
admin.site.register(models.Ingredient)
