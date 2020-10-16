import rest_framework.status
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from tracker.models import Conversion, conversion_statuses
from ..permissions import IsSuperUser
from offer.models import Currency, Goal


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = (
            'code',
            'name',
        )


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = (
            'id',
            'name',
        )


class ConversionSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer()
    goal = GoalSerializer()

    class Meta:
        model = Conversion
        fields = (
            'id',  # TODO .hex
            'created_at',
            'offer_id',
            'affiliate_id',
            # TODO offer.name
            'revenue',
            'payout',
            'currency',
            'sub1',
            'sub2',
            'sub3',
            'sub4',
            'sub5',
            'status',
            'goal',
            'goal_value',
            'country',
            'ip',
            'ua',
        )


class ConversionCreateView(APIView):
    permission_classes = (IsAuthenticated, IsSuperUser,)

    def post(self, request):
        offer_id = request.data.get('offer_id')
        if not offer_id:
            return Response(
                "Required 'offer_id'",
                rest_framework.status.HTTP_400_BAD_REQUEST
            )
        affiliate_id = request.data.get('pid')
        if not affiliate_id:
            return Response(
                "Required 'pid'",
                rest_framework.status.HTTP_400_BAD_REQUEST
            )
        try:
            usr = get_user_model().objects.get(pk=affiliate_id)
        except get_user_model().DoesNotExist:
            return Response(
                "Affiliate does not exist",
                rest_framework.status.HTTP_400_BAD_REQUEST
            )
        status = request.data.get('status')
        if status and status not in map(lambda r: r[0], conversion_statuses):
            return Response(
                "Wrong status value",
                rest_framework.status.HTTP_400_BAD_REQUEST
            )
        currency_code = request.data.get('currency')
        currency = None
        if currency_code:
            currency = Currency.objects.filter(code=currency_code).first()

        conversion = Conversion()
        conversion.offer_id = offer_id
        conversion.affiliate_id = affiliate_id
        conversion.affiliate_manager = usr.profile.manager
        if request.data.get('goal'):
            conversion.goal_value = request.data.get('goal')
        if request.data.get('revenue'):
            conversion.revenue = request.data.get('revenue')
        if request.data.get('payout'):
            conversion.payout = request.data.get('payout')
        if request.data.get('sub1'):
            conversion.sub1 = request.data.get('sub1')
        if currency:
            conversion.currency = currency
        if status:
            conversion.status = status
        if request.data.get('goal_id'):
            conversion.goal_id = request.data.get('goal_id')
        conversion.save()

        return Response(
            ConversionSerializer(conversion).data,
            status=rest_framework.status.HTTP_201_CREATED
        )
