from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsSuperUser
from offer.models import OfferTrafficSource


class OfferTrafficSourceSerializer(serializers.ModelSerializer):
    offer_id = serializers.IntegerField(write_only=True)
    traffic_source_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = OfferTrafficSource
        fields = '__all__'
        depth = 1


class OfferTrafficSourceViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, IsSuperUser,)
    serializer_class = OfferTrafficSourceSerializer
    queryset = OfferTrafficSource.objects
    filterset_fields = ['offer_id']
