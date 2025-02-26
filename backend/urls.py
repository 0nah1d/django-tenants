from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from authentication.views import GoogleLogin,GithubLogin
from authentication.viewset import AuthenticationViewSet

router = DefaultRouter()
router.register(r'auth', AuthenticationViewSet, basename='auth')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('accounts/', include('allauth.urls')),

    path('auth/social-login/google/', GoogleLogin.as_view(), name='google-auth'),
    path('auth/social-login/github/', GithubLogin.as_view(), name='github-auth'),
]
