from rest_framework import generics
from rest_framework import serializers
from rest_framework import permissions

from countries_plus.models import Country


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = (
            'iso',
            'name',
        )


class CountryListView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CountrySerializer
    queryset = Country.objects
