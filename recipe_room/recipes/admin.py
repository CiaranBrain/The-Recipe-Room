from django.contrib import admin
from .models import Recipe, Comment, Rating


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'image')


admin.site.register(Recipe, RecipeAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user', 'text', 'created_on')


admin.site.register(Comment, CommentAdmin)


class RatingAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user', 'value', 'created_on')


admin.site.register(Rating, RatingAdmin)
