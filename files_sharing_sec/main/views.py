from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UploadedFileSerializer,DownloadLinkSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import UploadedFile,DownloadLink
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import get_object_or_404
from django.http import FileResponse

@permission_classes([IsAuthenticated])
@api_view(['POST'])
def upload_file(request):
    data = request.data.copy()
    data.update({
        'owner' : request.user.id,
        'last_visited' : timezone.now(),
    })

    file_ser = UploadedFileSerializer(data=data)
    if file_ser.is_valid():
        file = file_ser.save()
        return Response(file_ser.data,status=status.HTTP_201_CREATED)
    return Response(file_ser.errors,400)




@api_view(['delete'])
@permission_classes([IsAuthenticated])
def delete_file(request,file_id:int):
    #we fetch the file
    file = get_object_or_404(UploadedFile,id=file_id)
    #check permission
    if not file.owner.id == request.user.id:
        return Response('access denied, you are not the owner of this file',status=status.HTTP_401_UNAUTHORIZED)
    file.file.delete(save=False)
    file.delete()
    return Response({'detail':'the file has been deleted successfully'},200)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_download_token(request,file_id:int):
    #we fetch the file
    file = get_object_or_404(UploadedFile,id=file_id)
    #check permission
    if not file.owner.id == request.user.id:
        return Response('access denied, you are not the owner of this file',status=status.HTTP_401_UNAUTHORIZED)
    data = request.data.copy()
    expires_at =  timezone.now() +  timedelta(minutes=int(data.get('duration',60*24)))   #1 day if duration is not provided
    data['expires_at'] = expires_at
    data['file'] = file.id
    
    down_ser = DownloadLinkSerializer(data=data)
    if down_ser.is_valid():
        download_link = down_ser.save()
        return Response(
            {'token' : download_link.token},
            status=201
        )
    return Response(down_ser.errors,400)

    
@api_view(['GET'])
def download_file(request):
    token = request.GET.get('token',None)
    if not token:
        return Response({'detail':'No token was provided'},400)
    #we fetch the download link
    link = DownloadLink.objects.filter(token=token).first()
    #validation
    if not link or link.is_expired:
        return Response({'detail':'this token has expired, ask the owner for a new one'},status.HTTP_410_GONE)
    #at this level the token is valid
    link.current_uses += 1
    link.save()
    file = link.file
    file.last_visited = timezone.now()   #mark the last time visited
    file.save()
    return FileResponse(open(file.file.path,'rb'),as_attachment=True,filename=file.file.name)
