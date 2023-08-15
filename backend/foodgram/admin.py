from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from foodgram.models import (Ingredient, Recipe, Tag, IngredientRecipe,
                             Favorite, ShoppingCart)
from users.models import Follow

User = get_user_model()


class RecipeIngredientsInline(admin.TabularInline):
    model = IngredientRecipe
    extra = 0


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Модель Recipe для представления в панели администратора."""
    list_display = ('name', 'author', 'get_tags')
    empty_value_display = '-пусто-'
    list_filter = ('name', 'author__email', 'tags')
    inlines = (RecipeIngredientsInline, )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Модель Ingredient для представления в панели администратора."""
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


@admin.register(User)
class UserAdmin(UserAdmin):
    """Модель User для представления в панели администратора."""
    list_filter = ('email', 'username')


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


admin.site.register(Tag)
admin.site.register(Follow)
