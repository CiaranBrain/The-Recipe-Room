from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe
from .forms import RecipeForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST

def recipe_list(request):
    # Fetch all recipes and order them by a specific field, e.g., 'title'
    recipe_list = Recipe.objects.all().order_by('created_on')

    # Set up pagination
    paginator = Paginator(recipe_list, 3)
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

def publish_recipe(request):
    if request.method == 'POST':
        # If the form has been submitted, process the data
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the new recipe to the database
            form.save()
            return redirect('recipe_list')  # Redirect to the recipe list after publishing
    else:
        # If the form hasn't been submitted, render an empty form
        form = RecipeForm()

    context = {
        'form': form,
    }

    return render(request, 'recipes/publish_recipe.html', context)

def recipe_edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        ingredients = request.POST.get('ingredients')
        instructions = request.POST.get('instructions')

        # Update recipe
        recipe.title = title
        recipe.ingredients = ingredients
        recipe.instructions = instructions

        # Handle image upload
        if 'image' in request.FILES:
            recipe.image = request.FILES['image']

        recipe.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def recipe_delete(request, recipe_id):
    if request.method == 'POST':
        recipe = get_object_or_404(Recipe, id=recipe_id)
        recipe.delete()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)