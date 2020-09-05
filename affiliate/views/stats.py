import iso8601
from datetime import datetime, time, timedelta, date
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..dao import daily_report, offer_report, goal_report, report_bysub


class DailyStatsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        start_date_arg = request.query_params.get('start_date')
        end_date_arg = request.query_params.get('end_date')
        offer_id = request.query_params.get('offer_id')

        if start_date_arg:
            start_date = iso8601.parse_date(start_date_arg)
        else:
            start_date = date.today() - timedelta(days=6)

        if end_date_arg:
            end_date = iso8601.parse_date(end_date_arg)
        else:
            end_date = date.today()

        start_datetime = datetime.combine(start_date, time.min)
        end_datetime = datetime.combine(end_date, time.max)

        data = daily_report(
            request.user.id, start_datetime, end_datetime, offer_id)

        return Response(data)


class OffersStatsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        start_date_arg = request.query_params.get('start_date')
        end_date_arg = request.query_params.get('end_date')

        if start_date_arg:
            start_date = iso8601.parse_date(start_date_arg)
        else:
            start_date = date.today() - timedelta(days=6)

        if end_date_arg:
            end_date = iso8601.parse_date(end_date_arg)
        else:
            end_date = date.today()

        start_datetime = datetime.combine(start_date, time.min)
        end_datetime = datetime.combine(end_date, time.max)

        data = offer_report(request.user.id, start_datetime, end_datetime)

        return Response(data)


class GoalStatsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        start_date_arg = request.query_params.get('start_date')
        end_date_arg = request.query_params.get('end_date')

        if start_date_arg:
            start_date = iso8601.parse_date(start_date_arg)
        else:
            start_date = date.today() - timedelta(days=6)

        if end_date_arg:
            end_date = iso8601.parse_date(end_date_arg)
        else:
            end_date = date.today()

        start_datetime = datetime.combine(start_date, time.min)
        end_datetime = datetime.combine(end_date, time.max)

        data = goal_report(request.user.id, start_datetime, end_datetime)

        return Response(data)


class SubStatsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, sub):
        if sub not in range(1, 6):
            return Response(status.HTTP_404_NOT_FOUND)

        offer_id = request.query_params.get('offer_id')
        if not offer_id:
            return Response(
                {'message': 'offer must be specified'},
                status.HTTP_400_BAD_REQUEST
            )

        start_date_arg = request.query_params.get('start_date')
        end_date_arg = request.query_params.get('end_date')

        if start_date_arg:
            start_date = iso8601.parse_date(start_date_arg)
        else:
            start_date = date.today() - timedelta(days=6)

        if end_date_arg:
            end_date = iso8601.parse_date(end_date_arg)
        else:
            end_date = date.today()

        start_datetime = datetime.combine(start_date, time.min)
        end_datetime = datetime.combine(end_date, time.max)

        data = report_bysub(
            sub, offer_id, request.user.id,
            start_datetime, end_datetime
        )

        return Response(data)
