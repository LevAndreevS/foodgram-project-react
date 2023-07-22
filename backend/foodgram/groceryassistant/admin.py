
from django.contrib import admin

from foodgram import settings
from groceryassistant.models import (Favoritelist, Ingredient,
                                     IngredientInRecipe, RecipeList,
                                     Shoppinglist, Tag)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = settings.EMPTY


class IngredientInRecipeInline(admin.TabularInline):
    model = IngredientInRecipe
    extra = 2
    min_num = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('name', 'color', 'slug')
    empty_value_display = settings.EMPTY


@admin.register(IngredientInRecipe)
class IngredientInRecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'ingredient', 'amount')
    empty_value_display = settings.EMPTY


@admin.register(RecipeList)
class RecipeListAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'author', 'favorites_quantity')
    search_fields = ('name', 'author', 'tags')
    list_filter = ('name', 'author', 'tags')
    inlines = [
        IngredientInRecipeInline,
    ]
    empty_value_display = settings.EMPTY

    def favorites_quantity(self, obj):
        return obj.favorites.count()


@admin.register(Favoritelist)
class FavoritelistAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    search_fields = ('user', 'recipe')
    empty_value_display = settings.EMPTY


@admin.register(Shoppinglist)
class ShoppinglistAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    search_fields = ('user', 'recipe')
    empty_value_display = settings.EMPTY
