from rest_framework.serializers import Serializer,ModelSerializer
from django.contrib.auth.models import User
from .models import UploadedFile




class UserSerializer(ModelSerializer):
    class meta:
        model = User
        fields = ['id','email','username','password','first_name','last_name']
        extra_kwargs = {
                'password': {'write_only': True}
            }
        

class UploadedFileSerializer(ModelSerializer):
    class meta:
        model = UploadedFile
        fields = ['id','name','owner','uploaded_at','file','last_visited','auto_delete','url']
        extra_kwargs = {
                'uploaded_at': {'read_only': True},
                'last_visited' : {'read_only': True},
                'url' : {'read_only': True},
            }