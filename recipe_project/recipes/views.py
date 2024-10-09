from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe
from .forms import RecipeForm

def recipe_list(request):
    recipes = Recipe.objects.all()
    context = {'recipes':recipes}
    return render(request, 'recipe_list.html',context)
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('recipe_list')
    else:
        form = RecipeForm()
    context = {'form':form}
    return render(request,'add_recipe.html',context)
def edit_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        form = RecipeForm(request.POST, instance = recipe)
        if form.is_valid():
            form.save()
            return redirect('recipe_list')
    else:
        form = RecipeForm(instance = recipe)
    context = {'form':form, 'recipe': recipe}
    return render(request, 'edit_recipe.html', context)