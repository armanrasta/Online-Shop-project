from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Address
from ..serializers import AddressSerializer
#dashboard
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
    
#addresses
@api_view(['POST', 'GET'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
def address(request):
    user = request.user
    
    if request.method == 'GET':
        
        addresses = Address.objects.filter(Customer=user)
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(Customer=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
