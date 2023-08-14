from django_filters.rest_framework import FilterSet, filters
from rest_framework.filters import SearchFilter

from foodgram.models import Recipe


class RecipeFilter(FilterSet):
    """Фильтр рецептов по тегам, избранному, корзине."""
    is_fovorited = filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )
    tags = filters.AllValuesMultipleFilter(field_name='tags_slug')

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_fovorited', 'is_in_shopping_cart')

    def filter_is_favorited(self, queriset, name, value):
        if value:
            return queriset.filter(favorites__user=self.request.user)
        return queriset

    def filter_is_in_shopping_cart(self, queriset, name, value):
        if value:
            return queriset.filter(carts__user=self.request.user)
        return queriset


class IngredientFilter(SearchFilter):
    """Фильтр ингредиентов по названию."""
    search_param = 'name'
