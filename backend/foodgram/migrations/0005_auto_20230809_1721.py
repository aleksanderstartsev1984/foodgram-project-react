# Generated by Django 3.2.3 on 2023-08-09 10:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodgram', '0004_auto_20230808_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='ingredient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='amounts', to='foodgram.ingredient', verbose_name='Ингредидиент'),
        ),
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='recipe',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='amounts', to='foodgram.recipe', verbose_name='Рецепт'),
        ),
    ]
