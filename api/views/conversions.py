import rest_framework.status
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from webargs import core, fields, ValidationError
from webargs.djangoparser import parser
from django.contrib.auth import get_user_model
from tracker.models import (
    Conversion, conversion_statuses, REJECTED_STATUS
)
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


@parser.location_loader('data')
def parse_data(request, name, field):
    return core.get_value(request.data, name, field)


def user_must_exist_in_db(user_id: int) -> None:
    try:
        get_user_model().objects.get(pk=user_id)
    except get_user_model().DoesNotExist:
        raise ValidationError("Affiliate does not exist")


def status_must_be_known(status: str) -> None:
    if status and status not in map(lambda r: r[0], conversion_statuses):
        raise ValidationError("Wrong status value")


conversion_create_args = {
    'offer_id': fields.Int(required=True),
    'pid': fields.Int(required=True, validate=user_must_exist_in_db),
    'status': fields.Str(
        load_default=REJECTED_STATUS,
        validate=status_must_be_known),
    'currency': fields.Str(load_default=''),
    'goal': fields.Str(load_default=''),
    'revenue': fields.Float(load_default=.0),
    'payout': fields.Float(load_default=.0),
    'sub1': fields.Str(load_default=''),
    'goal_id': fields.Int(load_default=None),
}


class ConversionCreateView(APIView):
    permission_classes = (IsAuthenticated, IsSuperUser,)

    @parser.use_args(conversion_create_args)
    def post(self, request, args):
        usr = get_user_model().objects.get(pk=args['pid'])

        conversion = Conversion()
        conversion.offer_id = args['offer_id']
        conversion.affiliate_id = args['pid']
        conversion.affiliate_manager = usr.profile.manager
        conversion.goal_value = args['goal']
        conversion.revenue = args['revenue']
        conversion.payout = args['payout']
        conversion.sub1 = args['sub1']
        conversion.currency = (
            Currency.objects.filter(code=args['currency']).first())
        conversion.status = args['status']
        if args['goal_id']:
            conversion.goal_id = args['goal_id']
        conversion.save()

        return Response(
            ConversionSerializer(conversion).data,
            status=rest_framework.status.HTTP_201_CREATED
        )
