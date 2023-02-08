from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsSuperUser
from offer.models import Offer


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'
        depth = 1


class OfferViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, IsSuperUser,)
    serializer_class = OfferSerializer
    queryset = Offer.objects
