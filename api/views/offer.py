from rest_framework import status
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsSuperUser
from offer.models import Offer


class OfferCreationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Offer
        fields = (
            'id',
            'title',
            'description_html',
            'tracking_link',
            'preview_link',
            'countries',
            'categories',
            # 'traffic_sources',
            'status',
            'advertiser',
            'icon',
        )


class OfferCreateView(APIView):
    permission_classes = (IsAuthenticated, IsSuperUser,)

    def post(self, request):
        serializer = OfferCreationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
