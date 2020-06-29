from rest_framework import generics
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import get_user_model


class AffiliateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
        )


class AffiliateListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, IsAdminUser,)
    serializer_class = AffiliateSerializer
    # queryset = get_user_model().objects

    def get_queryset(self):
        return get_user_model().objects.filter(is_staff=False)


class AffiliateRetrieveView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated, IsAdminUser,)
    serializer_class = AffiliateSerializer

    def get_queryset(self):
        return get_user_model().objects.filter(is_staff=False)
