from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from dramapi.views import CurrentUserView, UserViewSet, TypeViewSet, ColorViewSet, RatingViewSet, EntryViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'types', TypeViewSet, 'type')
router.register(r'colors', ColorViewSet, 'color')
router.register(r'ratings', RatingViewSet, 'rating')
router.register(r'entries', EntryViewSet, 'entry')

urlpatterns = [
    path('', include(router.urls)),
    path('register', UserViewSet.as_view(
        {'post': 'register_account'}), name='register'),
    path('login', UserViewSet.as_view({'post': 'user_login'}), name='login'),
    path('admin/', admin.site.urls),
    path('dramapi/token/', include('rest_framework.urls')),
    path('dramapi/current_user/', CurrentUserView.as_view(), name='current_user')
]
