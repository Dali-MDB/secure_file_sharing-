from rest_framework.serializers import Serializer,ModelSerializer
from django.contrib.auth.models import User
from .models import UploadedFile,DownloadLink




class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','username','password','first_name','last_name']
        extra_kwargs = {
                'password': {'write_only': True}
            }
        

class UploadedFileSerializer(ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ['id','name','owner','uploaded_at','file','last_visited','auto_delete','url']
        extra_kwargs = {
                'uploaded_at': {'read_only': True},
                'last_visited' : {'read_only': True},
                'url' : {'read_only': True},
            }
        

class DownloadLinkSerializer(ModelSerializer):
    class Meta:
        model = DownloadLink
        fields = ['id','token', 'file', 'created_at', 'expires_at', 'max_uses', 'current_uses' ]
        extra_kwargs = {
            'current_uses' : {'read_only':True},
            'token' : {'read_only':True},
            'created_at' : {'read_only':True},
        }