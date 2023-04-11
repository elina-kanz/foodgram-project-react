from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (RecipeViewSet, TagViewSet, IngredientViewSet,
                       UserModelViewSet, RegistrationAPIView, UserTokenView)

router = DefaultRouter()

router.register('recipes', RecipeViewSet)
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('users', UserModelViewSet, basename='User')

app_name = 'api'

auth_urlpatterns = [
    path('signup/', RegistrationAPIView.as_view()),
    path('token/', UserTokenView.as_view()),
]

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include(auth_urlpatterns)),
]
