from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.SimpleRouter()

router.register('tags', views.TagView, basename='tags')
router.register('ingredients', views.IngredientView, basename='ingredients')
router.register('recipes', views.RecipeView, basename='recipes')
router.register('users', views.UserViewSet, basename='users')
urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
