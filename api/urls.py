from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BookViewSet, AuthorViewSet

app_name = 'api'

router = DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'books', BookViewSet)

urlpatterns = [
    path('', include(router.urls))
]
