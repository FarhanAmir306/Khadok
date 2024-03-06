from django.urls import path, include
from rest_framework.routers import DefaultRouter

from accounts  import views

# Create a router and register our ViewSets with it.
router = DefaultRouter()


# router.register('', views.UserViewSet,basename='custom_user')

urlpatterns = [
    path('', include(router.urls)),
    path('login/',views.LoginView.as_view(),name='login'),
    path('register/',views.RegisterView.as_view(),name='register'),
    path('logout/',views.UserLogoutViewSet.as_view(),name='logout'),
]