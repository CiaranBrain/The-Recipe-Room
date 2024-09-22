from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Recipe

def home(request):
    return render(request, 'recipes/home.html')

def recipe_list(request):
    recipe_list = Recipe.objects.all()
    paginator = Paginator(recipe_list, 4)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'recipes/recipe_list.html', {'page_obj': page_obj})

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})