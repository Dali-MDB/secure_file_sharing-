from django.urls import path,include
from . import authentication
from . import views

urlpatterns = [
    path('auth/register/',view=authentication.register),
    path('auth/login/',view=authentication.login),
    path('auth/access_token/',view=authentication.get_access_token),

    path('files/upload/',view=views.upload_file),
    path('files/generate_token/<int:file_id>',view=views.generate_download_token),
    path('files/download',view=views.download_file),
    path('files/delete/<int:file_id>',view=views.delete_file),

]