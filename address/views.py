from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from address.models.address import Address
from .serializers import AddressSerializer


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_address(request):
    user = request.user
    serializer = AddressSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def edit_or_delete_address(request, address_id):
    user = request.user

    try:
        address = Address.objects.get(pk=address_id, user=user)

        if request.method == 'PATCH':
            serializer = AddressSerializer(address, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            address.delete()
            return Response({'message': 'Address deleted'}, status=status.HTTP_204_NO_CONTENT)
    except Address.DoesNotExist:
        return Response({'message': 'Address not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_user_addresses(request):
    user = request.user

    addresses = Address.objects.filter(user=user)
    serializer = AddressSerializer(addresses, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class AddressViewSet(ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
