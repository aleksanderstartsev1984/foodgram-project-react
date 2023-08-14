from django.urls import include, path
from rest_framework import routers

from foodgram.views import RecipeViewSet, IngredientViewSet, TagViewSet
from users.views import CustomUserViewSet, FollowListView, FollowViewSet


router = routers.DefaultRouter()

router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('tags', TagViewSet, basename='tags')
router.register('users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('users/subscriptions/',
         FollowListView.as_view(),
         name='subscriptions'),
    path('users/<int:user_id>/subscribe/',
         FollowViewSet.as_view(),
         name='subscribe'),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
