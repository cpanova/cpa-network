from rest_framework import generics
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsSuperUser
from offer.models import Advertiser


class AdvertiserCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertiser
        fields = (
            'id',
            'company',
            'email',
            'comment',
        )


class AdvertiserCreateAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, IsSuperUser,)
    serializer_class = AdvertiserCreationSerializer
    queryset = Advertiser.objects
