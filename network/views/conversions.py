import iso8601
import pytz
from datetime import datetime, time, date
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from tracker.models import Conversion
from django.conf import settings


class ConversionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Conversion
        fields = (
            'id',  # TODO .hex
            'created_at',
            'offer_id',
            # TODO offer.name
            'revenue',
            'payout',
            'sub1',
            'sub2',
            'sub3',
            'sub4',
            'sub5',
            'status',
            'goal',
            'country',
            'ip',
            'ua',
        )


class ConversionListView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser,)

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
