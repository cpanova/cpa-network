import iso8601
import pytz
from datetime import datetime, time, date
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from tracker.models import Conversion
from django.conf import settings
from offer.models import Offer, Goal, Currency


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = (
            'id',
            'title',
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


class ConversionSerializer(serializers.ModelSerializer):
    offer = OfferSerializer()
    goal = GoalSerializer()
    currency = CurrencySerializer()
    id = serializers.SerializerMethodField()
    click_id = serializers.SerializerMethodField()

    def get_id(self, obj):
        return obj.id.hex

    def get_click_id(self, obj):
        return obj.click_id.hex

    class Meta:
        model = Conversion
        fields = (
            'id',
            'created_at',
            'click_id',
            'offer',
            'payout',
            'sub1',
            'sub2',
            'sub3',
            'sub4',
            'sub5',
            'status',
            'goal',
            'currency',
            'country',
            'ip',
            'ua',
            'comment',
        )


class ConversionListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        start_date_arg = request.query_params.get('start_date')
        end_date_arg = request.query_params.get('end_date')
        offer_id = request.query_params.get('offer_id')

        if start_date_arg:
            start_date = iso8601.parse_date(start_date_arg)
        else:
            start_date = date.today()

        if end_date_arg:
            end_date = iso8601.parse_date(end_date_arg)
        else:
            end_date = date.today()

        tz = pytz.timezone(settings.TIME_ZONE)
        start_datetime = tz.localize(datetime.combine(start_date, time.min))
        end_datetime = tz.localize(datetime.combine(end_date, time.max))

        filters = {
            'created_at__range': [start_datetime, end_datetime],
            'affiliate_id': request.user.id,
        }

        if offer_id:
            filters['offer_id'] = offer_id

        objs = (
            Conversion.objects
            .filter(**filters)
            .order_by('-created_at')
        )

        return Response(ConversionSerializer(objs, many=True).data)
