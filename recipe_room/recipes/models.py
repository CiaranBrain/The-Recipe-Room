from django.db import models


class Recipe(models.Model):
    """Represents a recipe with detailed information and an image."""

    title = models.CharField(max_length=255)
    description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title