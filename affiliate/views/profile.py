from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
# from ..models import Affiliate
from django.contrib.auth import get_user_model


class AffiliateModelSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='first_name')

    class Meta:
        model = get_user_model()
        fields = (
            'name',
        )


class AffiliateRetrieveAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AffiliateModelSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.request.user.affiliate)
        return Response(serializer.data)
