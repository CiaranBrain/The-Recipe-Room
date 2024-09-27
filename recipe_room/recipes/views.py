from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe, Comment, Rating
from .forms import RecipeForm, CommentForm, RatingForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

def recipe_list(request):
    # Fetch all recipes and order them by a specific field, e.g., 'title'
    recipe_list = Recipe.objects.all().order_by('created_on')

    # Set up pagination
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }

    return render(request, 'recipes/recipe_list.html', context)

from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe, Comment, Rating
from .forms import CommentForm, RatingForm
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

def recipe_detail(request, recipe_id):
    """View to display recipe details along with comments and ratings."""

    recipe = get_object_or_404(Recipe, id=recipe_id)
    comments = recipe.comments.all()  # Get all comments related to the recipe
    ratings = recipe.ratings.all()  # Get all ratings related to the recipe
    average_rating = recipe.average_rating()  # Calculate average rating

    # Handle Comment Form
    if request.method == 'POST' and 'comment_submit' in request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.recipe = recipe
            if request.user.is_authenticated:
                comment.user = request.user
            comment.save()
            return redirect('recipe_detail', recipe_id=recipe.id)
    else:
        comment_form = CommentForm()

    # Check if the user has already rated this recipe
    user_rating = None
    if request.user.is_authenticated:
        try:
            user_rating = Rating.objects.get(recipe=recipe, user=request.user)
        except Rating.DoesNotExist:
            user_rating = None

    # Handle Rating Form (Only allow rating if the user hasn't rated yet)
    if request.method == 'POST' and 'rating_submit' in request.POST:
        if not user_rating:
            rating_form = RatingForm(request.POST)
            if rating_form.is_valid():
                rating = rating_form.save(commit=False)
                rating.recipe = recipe
                if request.user.is_authenticated:
                    rating.user = request.user
                rating.save()
                return redirect('recipe_detail', recipe_id=recipe.id)
        else:
            # If the user has already rated, display a message or handle this case
            return render(request, 'recipe_detail.html', {
                'recipe': recipe,
                'comments': comments,
                'ratings': ratings,
                'average_rating': average_rating,
                'comment_form': comment_form,
                'rating_form': RatingForm(),
                'error_message': 'You have already rated this recipe.'
            })
    else:
        rating_form = RatingForm()

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