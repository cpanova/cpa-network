import uuid
from django.db import models
from offer.models import Offer, Goal, Currency
from django.contrib.auth import get_user_model


class Click(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    sub1 = models.CharField(max_length=500, default="")
    sub2 = models.CharField(max_length=500, default="")
    sub3 = models.CharField(max_length=500, default="")
    sub4 = models.CharField(max_length=500, default="")
    sub5 = models.CharField(max_length=500, default="")
    ip = models.GenericIPAddressField()
    country = models.CharField(max_length=2, default="")
    ua = models.CharField(max_length=200, default="")
    revenue = models.DecimalField(max_digits=7, decimal_places=2)
    payout = models.DecimalField(max_digits=7, decimal_places=2)

    offer = models.ForeignKey(
        Offer,
        related_name='clicks',
        on_delete=models.SET_NULL,
        null=True
    )

    affiliate = models.ForeignKey(
        get_user_model(),
        related_name='clicks',
        on_delete=models.SET_NULL,
        null=True
    )

    affiliate_manager = models.ForeignKey(
        get_user_model(),
        # related_name='clicks',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )


APPROVED_STATUS = 'approved'
HOLD_STATUS = 'hold'
REJECTED_STATUS = 'rejected'
conversion_statuses = (
    (APPROVED_STATUS, 'Approved',),
    (HOLD_STATUS, 'Hold',),
    (REJECTED_STATUS, 'Rejected',),
)


class Conversion(models.Model):

    class Meta:
        ordering = ('-created_at',)

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    click_id = models.UUIDField(editable=False, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    click_date = models.DateTimeField(null=True, default=None)
    sub1 = models.CharField(max_length=500, default="")
    sub2 = models.CharField(max_length=500, default="")
    sub3 = models.CharField(max_length=500, default="")
    sub4 = models.CharField(max_length=500, default="")
    sub5 = models.CharField(max_length=500, default="")
    revenue = models.DecimalField(max_digits=7, decimal_places=2, default=.0)
    payout = models.DecimalField(max_digits=7, decimal_places=2, default=.0)
    ip = models.GenericIPAddressField(null=True, default=None)
    country = models.CharField(max_length=2, default="")
    ua = models.CharField(max_length=200, default="")
    goal_value = models.CharField(max_length=20, default="")
    status = models.CharField(
        max_length=10, choices=conversion_statuses, default=REJECTED_STATUS)
    sum = models.FloatField(default=0.0)
    comment = models.CharField(max_length=128, default='', blank=True)

    goal = models.ForeignKey(
        Goal,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    currency = models.ForeignKey(
        Currency,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    offer = models.ForeignKey(
        Offer,
        related_name='conversions',
        on_delete=models.SET_NULL,
        null=True
    )

    affiliate = models.ForeignKey(
        get_user_model(),
        related_name='conversions',
        on_delete=models.SET_NULL,
        null=True
    )

    affiliate_manager = models.ForeignKey(
        get_user_model(),
        # related_name='conversions',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
