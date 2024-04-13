from rest_framework import generics
from ..models import Address
from ..serializers import AddressSerializer
from rest_framework.permissions import IsAuthenticated

class AddressListCreateView(generics.ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter the queryset to only include addresses for the current user
        return Address.objects.filter(Customer=self.request.user)

class AddressRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter the queryset to only include addresses for the current user
        return Address.objects.filter(Customer=self.request.user)