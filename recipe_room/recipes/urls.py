from django.urls import path
from .views import recipe_list, recipe_detail
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('recipes/', recipe_list, name='recipe_list'),
    path('recipe/<int:recipe_id>/', recipe_detail, name='recipe_detail'),
    path('publish/', views.publish_recipe, name='publish_recipe'),
    path('recipe/<int:recipe_id>/edit/', views.recipe_edit, name='recipe_edit'),
    path('recipe/<int:recipe_id>/delete/', views.recipe_delete, name='recipe_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)