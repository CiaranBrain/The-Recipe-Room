from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Recipe

def recipe_list(request):
    # Fetch all recipes and order them by a specific field, e.g., 'title'
    recipe_list = Recipe.objects.all().order_by('created_on')

    # Set up pagination
    paginator = Paginator(recipe_list, 4)
    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }

    return render(request, 'recipes/recipe_list.html', context)


def recipe_detail(request, recipe_id):
    # Fetch the recipe or return a 404 if it doesn't exist
    recipe = get_object_or_404(Recipe, id=recipe_id)

    # Set up the context dictionary to pass to the template
    context = {
        'recipe': recipe,
    }

    return render(request, 'recipes/recipe_detail.html', context)