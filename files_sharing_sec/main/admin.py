from django.contrib import admin
from django.contrib.auth.models import User
from .models import UploadedFile,DownloadLink
# Register your models here.

admin.site.register(UploadedFile)
admin.site.register(DownloadLink)
