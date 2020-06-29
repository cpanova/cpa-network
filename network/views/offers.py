from rest_framework import generics
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from countries_plus.models import Country
from offer.models import (
    Offer,
    Category,
    Advertiser,
    Currency,
    Goal,
    TrafficSource,
    OfferTrafficSource,
    Payout
)


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = (
            'iso',
        )


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = (
            'name',
        )


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = (
            'code',
            'name',
        )


class PayoutSerializer(serializers.ModelSerializer):
    countries = CountrySerializer(many=True, read_only=True)
    goal = GoalSerializer(read_only=True)
    currency = CurrencySerializer(read_only=True)

    class Meta:
        model = Payout
        fields = (
            'revenue',
            'payout',
            'countries',
            'goal_value',
            'type',
            'currency',
            'goal'
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'name',
        )


class TrafficSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficSource
        fields = (
            'name',
        )


class OfferTrafficSourceSerializer(serializers.ModelSerializer):
    name = serializers.SlugRelatedField(
        source='traffic_source',
        many=False, read_only=True, slug_field='name')

    class Meta:
        model = OfferTrafficSource
        fields = (
            'name',
            'allowed'
        )


class AdvertiserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertiser
        fields = (
            'company',
            'email',
            'contact_person',
            'messenger',
            'site',
            'comment',
        )


class OfferSerializer(serializers.ModelSerializer):
    countries = CountrySerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    traffic_sources = OfferTrafficSourceSerializer(
        source='offertrafficsource_set', many=True, read_only=True)
    advertiser = AdvertiserSerializer(read_only=True)
    payouts = PayoutSerializer(many=True, read_only=True)

    class Meta:
        model = Offer
        fields = (
            'id',
            'title',
            'description',
            'tracking_link',
            'preview_link',
            'countries',
            'categories',
            'traffic_sources',
            'status',
            'advertiser',
            'payouts',
        )


class OfferListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, IsAdminUser,)
    serializer_class = OfferSerializer
    queryset = Offer.objects


class OfferRetrieveView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated, IsAdminUser,)
    serializer_class = OfferSerializer
    queryset = Offer.objects
