from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from foodgram.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                             ShoppingCart, Tag)
from foodgram.paginations import CustomPageNumberPagination
from foodgram.permissions import IsAuthorOrReadOnly
from foodgram.serializers import (IngredientSerializer, RecipeGetSelializer,
                                  RecipePostSelializer, TagSerializer,
                                  FavoriteSerializer, ShoppingCartSerializer)
from foodgram.filters import IngredientFilter, RecipeFilter


class RecipeViewSet(viewsets.ModelViewSet):
    """Представление модели Recipe."""
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def get_queryset(self):
        return Recipe.objects.prefetch_related(
            'amounts__ingredient', 'tags'
        ).all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeGetSelializer
        return RecipePostSelializer

    @staticmethod
    def post_method_for_actions(request, pk, serializers):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = serializers(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def delete_method_for_actions(request, pk, model):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        instance = get_object_or_404(model, user=user, recipe=recipe)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["POST"],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        return self.post_method_for_actions(
            request=request, pk=pk, serializers=FavoriteSerializer)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        return self.delete_method_for_actions(
            request=request, pk=pk, model=Favorite)

    @action(detail=True, methods=["POST"],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        return self.post_method_for_actions(
            request=request, pk=pk, serializers=ShoppingCartSerializer)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        return self.delete_method_for_actions(
            request=request, pk=pk, model=ShoppingCart)

    @action(detail=False, methods=['GET'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        ingredients = IngredientRecipe.objects.filter(
            recipe__carts__user=request.user).values_list(
            'ingredient__name', 'ingredient__measurement_unit',
            'amount'
        )
        cart_list = {}
        for item in ingredients:
            name = item[0]
            if name not in cart_list:
                cart_list[name] = {
                    'measurement_unit': item[1],
                    'amount': item[2]
                }
            else:
                cart_list[name]['amount'] += item[2]

        pdfmetrics.registerFont(
            TTFont('ofont', 'data/ofont.ttf', 'UTF-8'))
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = ('attachment; '
                                           'filename="shopping_cart.pdf"')
        page = canvas.Canvas(response)
        page.setFont('ofont', size=26)
        page.drawString(50, 800, 'Список покупок')
        page.setFont('ofont', size=14)
        height = 750
        for i, (name, data) in enumerate(cart_list.items(), 1):
            page.drawString(50, height, (f'{i}. {name} - {data["amount"]} '
                                         f'{data["measurement_unit"]}'))
            height -= 30
        page.showPage()
        page.save()
        return response


class IngredientViewSet(viewsets.ModelViewSet):
    """Представление модели Ingredient."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = [IngredientFilter]
    search_fields = ('^name', )


class TagViewSet(viewsets.ModelViewSet):
    """Представление модели Tag."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
