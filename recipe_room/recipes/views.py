from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe, Comment, Rating
from .forms import RecipeForm, CommentForm, RatingForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def recipe_list(request):
    # Fetch all recipes and order them by a specific field, e.g., 'created_on'
    recipe_list = Recipe.objects.all().order_by('created_on')

    # Set up pagination
    paginator = Paginator(recipe_list, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }

    return render(request, 'recipes/recipe_list.html', context)

def recipe_detail(request, recipe_id):
    """View to display recipe details along with comments and ratings."""
    recipe = get_object_or_404(Recipe, id=recipe_id)
    comments = recipe.comments.all()
    ratings = recipe.ratings.all()
    average_rating = recipe.average_rating()

    # Handle Comment Form
    comment_form = CommentForm(request.POST or None)
    if request.method == 'POST' and 'comment_submit' in request.POST:
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.recipe = recipe
            if request.user.is_authenticated:
                comment.user = request.user
            comment.save()
            return redirect('recipe_detail', recipe_id=recipe.id)

    # Check if the user has already rated this recipe
    user_rating = None
    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(recipe=recipe, user=request.user).first()

    # Handle Rating Form
    rating_form = RatingForm(request.POST or None)
    if request.method == 'POST' and 'rating_submit' in request.POST:
        if user_rating is None:
            if rating_form.is_valid():
                rating = rating_form.save(commit=False)
                rating.recipe = recipe
                if request.user.is_authenticated:
                    rating.user = request.user
                rating.save()
                return redirect('recipe_detail', recipe_id=recipe.id)
        else:
            return render(request, 'recipes/recipe_detail.html', {
                'recipe': recipe,
                'comments': comments,
                'ratings': ratings,
                'average_rating': average_rating,
                'comment_form': comment_form,
                'rating_form': rating_form,
                'error_message': 'You have already rated this recipe.',
                'user_rating': user_rating
            })

    context = {
        'recipe': recipe,
        'comments': comments,
        'ratings': ratings,
        'average_rating': average_rating,
        'comment_form': comment_form,
        'rating_form': rating_form,
        'user_rating': user_rating
    }
    return render(request, 'recipes/recipe_detail.html', context)

@login_required
def publish_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('recipe_list')
    else:
        form = RecipeForm()

    context = {
        'form': form,
    }

    return render(request, 'recipes/publish_recipe.html', context)

@login_required
def recipe_edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        ingredients = request.POST.get('ingredients')
        instructions = request.POST.get('instructions')

        # Update recipe
        recipe.title = title
        recipe.description = description
        recipe.ingredients = ingredients
        recipe.instructions = instructions

        # Handle image upload
        if 'image' in request.FILES:
            recipe.image = request.FILES['image']

        try:
            recipe.save()
            messages.success(request, 'Recipe updated successfully')
            return JsonResponse({'success': True})
        except:
            messages.error(request, 'Error updating your recipe')
            return JsonResponse({'success': False})

    return JsonResponse({'success': False})


@login_required
def recipe_delete(request, recipe_id):
    if request.method == 'POST':
        recipe = get_object_or_404(Recipe, id=recipe_id)
        recipe.delete()
        messages.success(request, 'Recipe deleted successfully')
        return JsonResponse({'success': True})
    else:
        messages.error(request, 'Error deleting your recipe')
        return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)