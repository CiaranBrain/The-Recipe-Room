from django import forms
from .models import Recipe, Comment, Rating

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients', 'instructions', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Recipe Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'ingredients': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingredients'}),
            'instructions': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Instructions'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class':"form-control", 'placeholder': 'Comment'})
        }


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['value']