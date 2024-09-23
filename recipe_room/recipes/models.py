from django.db import models


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
        return '\static\images\no_image.png'