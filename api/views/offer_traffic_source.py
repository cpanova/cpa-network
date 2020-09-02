from rest_framework import status
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsSuperUser
from offer.models import OfferTrafficSource


class OfferTrafficSourceCreationSerializer(serializers.ModelSerializer):

    class Meta:
        model = OfferTrafficSource
        fields = (
            'offer',
            'traffic_source',
            'allowed',
        )


class OfferTrafficSourceCreateView(APIView):
    permission_classes = (IsAuthenticated, IsSuperUser,)

    def post(self, request, pk):
        serializer = OfferTrafficSourceCreationSerializer(
            data=dict(request.data, offer=pk)
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
