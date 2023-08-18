from django.contrib import admin
from django.contrib.auth import get_user_model

from foodgram.models import (Ingredient, Recipe, Tag, IngredientRecipe,
                             Favorite, ShoppingCart)
from users.models import Follow

User = get_user_model()


class RecipeIngredientsInline(admin.TabularInline):
    """Добавление ингредиента для рецепта в панели администратора."""
    model = IngredientRecipe
    extra = 0


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Модель Recipe для представления в панели администратора."""
    list_display = ('name', 'author', 'get_tags', 'count_in_is_favorite')
    empty_value_display = '-пусто-'
    list_filter = ('tags', )
    inlines = (RecipeIngredientsInline, )

    def count_in_is_favorite(self, obj):
        return obj.favorites.count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Модель Ingredient для представления в панели администратора."""
    list_display = ('name', 'measurement_unit')
    list_filter = ('measurement_unit',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """Модель ShoppingCart для представления в панели администратора."""
    list_display = ('user', 'recipe')
    empty_value_display = '-пусто-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Модель Favorite для представления в панели администратора."""
    list_display = ('user', 'recipe')
    empty_value_display = '-пусто-'


admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Follow)
