from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsSuperUser
from offer.models import Landing


class LandingSerializer(serializers.ModelSerializer):
    offer_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Landing
        fields = '__all__'
        depth = 1


class LandingViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, IsSuperUser,)
    serializer_class = LandingSerializer
    queryset = Landing.objects
    filterset_fields = ['offer_id']
