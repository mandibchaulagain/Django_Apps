from django.urls import path
from . import views

urlpatterns = [
    path('',views.recipe_list,name = 'recipe_list'),
    path('add/',views.add_recipe, name = 'add_recipe'),
    path('edit/<int:pk>',views.edit_recipe, name = 'edit_recipe'),
]