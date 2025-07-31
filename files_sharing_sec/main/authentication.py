from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


def generate_tokens(user):
    token = RefreshToken.for_user(user)
    access_token = str(token.access_token)
    refresh_token = str(token)
    return refresh_token,access_token


@api_view(['POST'])
def register(request):
    user_ser = UserSerializer(data=request.data)
    if user_ser.is_valid():
        user = user_ser.save()
        #we generate the refresh and access token
        refresh_token,access_token = generate_tokens(user)
        return Response(
            {       
                'detail':'the user has been registered successfully',
                'refresh_token' : refresh_token,
                'access_token' : access_token,
            },
            status=status.HTTP_200_OK
        )
    return Response(user_ser.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    email = request.data.get('email',None)
    password = request.data.get('password',None)
    if not email or not password:
        raise ValidationError(detail='the email and password fields are required')
    #get the user with this email
    user = User.objects.filter(email=email).first()
    if not user:
        return Response(
            {'detail':'no user with the provided credentials was found'},
            status=status.HTTP_404_NOT_FOUND
        )
    #we authenticated the user
    user = authenticate(username=user.username,password=password)
    if not user:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    #generate tokens for the user
    #we generate the refresh and access token
    refresh_token,access_token = generate_tokens(user)
    return Response(
            {       
                'refresh_token' : refresh_token,
                'access_token' : access_token,
            },
            status=status.HTTP_200_OK
        )

    

@api_view(['POST'])
def get_access_token(request):
    refresh_token = request.data.get('refresh',None)
    if not refresh_token:
        return Response('no refresh token was provided',400)
    token = RefreshToken(refresh_token)
    if token.check_exp():
        return Response({'detail':'the refresh token has been expired, please login again'},status=status.HTTP_408_REQUEST_TIMEOUT)
    access_token = str(token.access_token)
    return Response({'access_token': access_token}, status=status.HTTP_200_OK)