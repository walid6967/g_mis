from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status

@api_view(['POST'])
@authentication_classes([])  # Disable authentication for this view
@permission_classes([])       # Disable permission checks for this view
def get_access_token(request):
    """
    API to authenticate the user and return an access token.
    """
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:
        # Generate access token
        access = AccessToken.for_user(user)
        return Response({
            "access": str(access),
            "message": "Login successful"
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            "error": "Invalid username or password",
            "message": "Authentication failed"
        }, status=status.HTTP_401_UNAUTHORIZED)
