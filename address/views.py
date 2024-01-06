from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from address.repositories.address_repository import AddressRepository
from address.serializers.address_serializer import AddressSerializer


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_address(request):
    user = request.user
    serializer = AddressSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        address = AddressRepository.create_address(serializer.validated_data, user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def edit_or_delete_address(request, address_id):
    user = request.user
    address = AddressRepository.get_address_by_id(address_id, user)

    if not address:
        return Response({'message': 'Address not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':
        updated_data = AddressRepository.update_address(address, request.data)
        return Response(updated_data)

    if request.method == 'DELETE':
        AddressRepository.delete_address(address)
        return Response({'message': 'Address deleted'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_user_addresses(request):
    user = request.user
    addresses = AddressRepository.get_user_addresses(user)
    return Response(addresses, status=status.HTTP_200_OK)
