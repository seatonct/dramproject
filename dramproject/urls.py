from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from dramapi.views import UserViewSet, TypeViewSet, ColorViewSet, RatingViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'types', TypeViewSet, 'type')
router.register(r'colors', ColorViewSet, 'color')
router.register(r'ratings', RatingViewSet, 'rating')

urlpatterns = [
    path('', include(router.urls)),
    path('register', UserViewSet.as_view(
        {'post': 'register_account'}), name='register'),
    path('login', UserViewSet.as_view({'post': 'user_login'}), name='login'),
]
