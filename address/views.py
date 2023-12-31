from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from .models import Address
from .serializers import AddressSerializer
from user.models import CustomUser

@api_view(['POST'])
def create_address(request, user_id):
    try:
        user = CustomUser.objects.get(pk=user_id)
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except CustomUser.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PATCH', 'DELETE'])
def edit_or_delete_address(request, user_id, address_id):
    try:
        user = CustomUser.objects.get(pk=user_id)
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
    except (CustomUser.DoesNotExist, Address.DoesNotExist):
        return Response({'message': 'User or Address not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_user_addresses(request, user_id):
    try:
        user = CustomUser.objects.get(pk=user_id)
        addresses = Address.objects.filter(user=user)
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class AddressViewSet(ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
