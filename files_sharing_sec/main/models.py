from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone


# Create your models here.
def user_directory_path(instance, filename):
        today = timezone.now()
        return f"{instance.owner.id}/{today.year}_{today.month:02}_{today.day:02}_{filename}"

class UploadedFile(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name='files')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to=user_directory_path)
    last_visited = models.DateTimeField(null=True,blank=True)
    auto_delete = models.BooleanField(default=False)   #indicate if te file should be auto deleted if it has been so long since it was last opened

    @property
    def url(self):
        return self.file.url

    def __str__(self):
        return f'file: {self.name} - {self.owner.email} - {self.uploaded_at}'
    

class DownloadLink(models.Model):
    token = models.UUIDField(default=uuid.uuid4,unique=True)
    file = models.ForeignKey(UploadedFile,related_name='download_links',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    max_uses = models.IntegerField()
    current_uses = models.IntegerField(default=0)



    @property
    def is_expired(self):
        return ( timezone.now() > self.expires_at ) or ( self.current_uses >= self.max_uses )

    def __str__(self):
        return f'download_link: {self.token} - ({self.created_at}/{self.max_uses}) - {self.file} '
    

    
