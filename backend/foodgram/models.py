from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator

User = get_user_model()


class Tag(models.Model):
    """Модель тега."""
    name = models.CharField('Название', max_length=200)
    slug = models.SlugField('Краткое название(англ)',
                            unique=True,
                            max_length=200)
    color = models.CharField('Цвет(HEX-CODE)', max_length=7)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Теги'


class Ingredient(models.Model):
    """Модель ингредиента."""
    name = models.CharField('Название', max_length=200)
    measurement_unit = models.CharField('Единицы измерения', max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        constraints = [
            models.UniqueConstraint(fields=['name', 'measurement_unit'],
                                    name='unique ingredient')
        ]


class Recipe(models.Model):
    """Модель рецепта."""
    author = models.ForeignKey(User,
                               verbose_name='Автор',
                               related_name='author_recipies',
                               on_delete=models.CASCADE)
    name = models.CharField('Название',
                            max_length=200)
    image = models.ImageField('Изображение',
                              upload_to='images/',
                              null=True,
                              default='recipe_default.png')
    text = models.TextField('Текст рецепта',
                            max_length=5000)
    cooking_time = models.IntegerField('Время приготовления(минуты)',
                                       validators=[MinValueValidator(1)])
    pub_date = models.TimeField('Дата пупликации',
                                auto_now_add=True)
    tags = models.ManyToManyField(Tag,
                                  verbose_name='Теги',
                                  related_name='recipies',
                                  blank=True)
    ingredients = models.ManyToManyField(Ingredient,
                                         verbose_name='Ингридиенты',
                                         related_name='recipies',
                                         through='IngredientRecipe',
                                         through_fields=('recipe',
                                                         'ingredient'))
    faworite = models.ManyToManyField(User,
                                      verbose_name='Избранное',
                                      related_name='favorite_recipies')

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name

    def get_tags(self):
        return ','.join([str(p) for p in self.tags.all()])


class IngredientRecipe(models.Model):
    """Модель связи ингредиента с рецептом."""
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE,
                                   verbose_name='Ингредидиент',
                                   related_name='amounts',
                                   null=True)
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               verbose_name='Рецепт',
                               related_name='amounts',
                               null=True)
    amount = models.IntegerField('Количество',
                                 validators=[MinValueValidator(1)])

    def __str__(self):
        return f'{self.ingredient} {self.recipe}'


class ShoppingCart(models.Model):
    """Модель корзины покупок."""
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name='Пользователь',
                             related_name='carts')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               verbose_name='Рецепт',
                               related_name='carts')

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'


class Favorite(models.Model):
    """Модель избранных рецептов."""
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name='Пользователь',
                             related_name='favorites_user')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               verbose_name='Рецепт',
                               related_name='favorites')

    def __str__(self):
        return self.recipe.name

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique favorite')
        ]
