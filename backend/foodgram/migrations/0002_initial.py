# Generated by Django 3.2.3 on 2023-08-19 11:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('foodgram', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppingcart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='carts', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_recipies', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='faworite',
            field=models.ManyToManyField(related_name='favorite_recipies', to=settings.AUTH_USER_MODEL, verbose_name='Избранное'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(related_name='recipies', through='foodgram.IngredientRecipe', to='foodgram.Ingredient', verbose_name='Ингридиенты'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='recipies', to='foodgram.Tag', verbose_name='Теги'),
        ),
        migrations.AddField(
            model_name='ingredientrecipe',
            name='ingredient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='amounts', to='foodgram.ingredient', verbose_name='Ингредидиент'),
        ),
        migrations.AddField(
            model_name='ingredientrecipe',
            name='recipe',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='amounts', to='foodgram.recipe', verbose_name='Рецепт'),
        ),
        migrations.AddConstraint(
            model_name='ingredient',
            constraint=models.UniqueConstraint(fields=('name', 'measurement_unit'), name='unique ingredient'),
        ),
        migrations.AddField(
            model_name='favorite',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='foodgram.recipe', verbose_name='Рецепт'),
        ),
        migrations.AddField(
            model_name='favorite',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites_user', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique favorite'),
        ),
    ]
