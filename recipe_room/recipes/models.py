from django.db import models
from django.contrib.auth.models import User

class Recipe(models.Model):
    """Represents a recipe with detailed information and an image."""

    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='recipe_images/', blank=True, null=True)
    description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_image_url(self):
        if self.image:
            return self.image.url
        return '/static/images/no_image.png'

    def average_rating(self):
        """Calculate the average rating for the recipe."""
        ratings = self.ratings.all()  # Access all related ratings
        if ratings.exists():
            return sum(rating.value for rating in ratings) / ratings.count()
        return 0  # Return 0 if no ratings are available


class Comment(models.Model):
    """Represents a comment on a recipe."""
    recipe = models.ForeignKey(Recipe, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username if self.user else 'Anonymous'} on {self.recipe}"


class Rating(models.Model):
    """Represents a rating for a recipe."""
    recipe = models.ForeignKey(Recipe, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    value = models.IntegerField()  # Rating value, 1-5
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(value__gte=1, value__lte=5), name='rating_range'),
            models.UniqueConstraint(fields=['user', 'recipe'], name='unique_user_recipe_rating')
        ]

    def __str__(self):
        return f"Rating of {self.value} for {self.recipe} by {self.user.username if self.user else 'Anonymous'}"