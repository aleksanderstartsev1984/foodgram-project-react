from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter

from foodgram.models import Recipe, Tag

User = get_user_model()


class RecipeFilter(filters.FilterSet):
    """Фильтр рецептов по тегам, избранному, корзине."""
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    is_favorited = filters.BooleanFilter(field_name='is_favorited',
                                         method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        field_name='is_in_shopping_cart',
        method='filter_is_in_shopping_cart'
    )
    tags = filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all(),
                                             field_name='tags__slug',
                                             to_field_name='slug')

    class Meta:
        model = Recipe
        fields = ('author',
                  'is_favorited',
                  'is_in_shopping_cart',
                  'tags')

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if not user or user.is_anonymous:
            return queryset
        if value:
            return queryset.filter(favorites__user=user)
        if not value:
            return queryset.excluse(favorites__user=user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if not user or user.is_anonymous:
            return queryset
        if value:
            return queryset.filter(carts__user=user)
        if not value:
            return queryset.excluse(carts__user=user)
        return queryset


class IngredientFilter(SearchFilter):
    """Фильтр ингредиентов по названию."""
    search_param = 'name'
