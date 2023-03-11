from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import Subscribe, User
from .models import (Favorites, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Tag)


class IngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    min_num = 1


class UsersAdmin(UserAdmin):
    list_filter = ('username', 'email', )
    list_display = ('pk', 'username', 'email', 'first_name', 'last_name', )


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'name', 'get_favorites')
    search_fields = ('name', 'author', 'tags', )
    list_filter = ('name', 'author', 'tags', )
    inlines = (IngredientInline, )
    empty_value_display = '-пусто-'

    def get_favorites(self, instance):
        return instance.fav_recipe.count()
    get_favorites.short_description = 'Избранное'


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'ingredient')
    search_fields = ('recipe',)
    list_filter = ('recipe',)
    empty_value_display = '-пусто-'


class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
    search_fields = ('author',)
    list_filter = ('author',)
    empty_value_display = '-пусто-'


class FavoritesAndShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'user')
    search_fields = ('recipe',)
    list_filter = ('recipe',)
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Subscribe, SubscribeAdmin)
admin.site.register(Favorites, FavoritesAndShoppingCartAdmin)
admin.site.register(ShoppingCart, FavoritesAndShoppingCartAdmin)
