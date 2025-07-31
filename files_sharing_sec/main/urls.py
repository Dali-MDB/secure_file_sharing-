from django.urls import path,include
from . import authentication

urlpatterns = [
    path('auth/register/',view=authentication.register),
    path('auth/login/',view=authentication.login),
    path('auth/access_token/',view=authentication.get_access_token),

]