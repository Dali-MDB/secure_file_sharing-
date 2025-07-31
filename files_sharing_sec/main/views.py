from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UploadedFileSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import UploadedFile



# @permission_classes([IsAuthenticated])
# @api_view(['POST'])
# def upload_file(request):
#     uploaded_file = request.FILES.get('file')
#     file_name = request.data.get('name',uploaded_file.name)
#     auto_delete = request.data.get('auto_delete')
#     data = {
#         'name' : uploaded_file.name,
#         'file' : file_name,
#         'owner' : request.user.id,
#         'auto_delete' : 

#     }
#     file_ser = UploadedFileSerializer()


