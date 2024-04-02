from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.response import Response

@api_view(['GET'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
def dashboard(request):
    user = request.user
    
    username = user.username
    email = user.email
    phone_number = user.phone_number
    first_name = user.first_name
    last_name = user.last_name
    
    return Response({
        'username': username, 'email': email, 'phone number': phone_number,
        'first name': first_name, 'last name': last_name})