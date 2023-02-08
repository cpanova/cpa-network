from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsSuperUser
from offer.models import Advertiser


class AdvertiserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertiser
        fields = '__all__'
        depth = 1


class AdvertiserViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, IsSuperUser,)
    serializer_class = AdvertiserSerializer
    queryset = Advertiser.objects
