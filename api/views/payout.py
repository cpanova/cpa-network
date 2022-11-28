from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsSuperUser
from offer.models import Payout


class PayoutSerializer(serializers.ModelSerializer):
    offer_id = serializers.IntegerField(write_only=True)
    currency_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Payout
        fields = '__all__'
        depth = 1


class PayoutViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, IsSuperUser,)
    serializer_class = PayoutSerializer
    queryset = Payout.objects
    filterset_fields = ['offer_id']
