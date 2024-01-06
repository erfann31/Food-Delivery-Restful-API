from address.models.address import Address
from address.serializers.address_serializer import AddressSerializer

class AddressRepository:
    @staticmethod
    def create_address(data, user):
        address = Address(user=user, **data)
        address.save()
        return address

    @staticmethod
    def get_address_by_id(address_id, user):
        try:
            return Address.objects.get(pk=address_id, user=user)
        except Address.DoesNotExist:
            return None

    @staticmethod
    def update_address(address, data):
        serializer = AddressSerializer(address, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        return serializer.errors

    @staticmethod
    def delete_address(address):
        address.delete()

    @staticmethod
    def get_user_addresses(user):
        addresses = Address.objects.filter(user=user)
        serializer = AddressSerializer(addresses, many=True)
        return serializer.data
