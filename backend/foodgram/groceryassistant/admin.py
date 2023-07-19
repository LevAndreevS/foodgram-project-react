from django.contrib import admin
from .models import (
    Ingredient,
    IngredientInRecipe,
    RecipeList,
    Tag,
    Favoritelist,
    Shoppinglist,
)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class IngredientInRecipeInline(admin.TabularInline):
    model = IngredientInRecipe
    extra = 2
    min_num = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('name', 'color', 'slug')
    empty_value_display = '-пусто-'


@admin.register(IngredientInRecipe)
class IngredientInRecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'ingredient', 'amount')
    empty_value_display = '-пусто-'


@admin.register(RecipeList)
class RecipeListAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'author', 'favorites_quantity')
    search_fields = ('name', 'author', 'tags')
    list_filter = ('name', 'author', 'tags')
    inlines = [
        IngredientInRecipeInline,
    ]
    empty_value_display = '-пусто-'

    def favorites_quantity(self, obj):
        return obj.favorites.count()


@admin.register(Favoritelist)
class FavoritelistAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    search_fields = ('user', 'recipe')
    empty_value_display = '-пусто-'


@admin.register(Shoppinglist)
class ShoppinglistAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    search_fields = ('user', 'recipe')
    empty_value_display = '-пусто-'
