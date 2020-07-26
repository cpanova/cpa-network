from django.db import models
from countries_plus.models import Country


ACTIVE_STATUS = 'Active'
PAUSED_STATUS = 'Paused'
STOPPED_STATUS = 'Stopped'
offer_statuses = (
    (ACTIVE_STATUS, 'Active'),
    (PAUSED_STATUS, 'Paused'),
    (STOPPED_STATUS, 'Stopped'),
)


class Offer(models.Model):
    title = models.CharField(max_length=256, default='')
    description = models.TextField(default='')
    tracking_link = models.CharField(max_length=1024, default='')
    preview_link = models.CharField(max_length=1024, default='')
    countries = models.ManyToManyField(Country)
    categories = models.ManyToManyField('Category', blank=True)
    traffic_sources = models.ManyToManyField(
        'TrafficSource', through='OfferTrafficSource', blank=True)
    status = models.CharField(max_length=20, choices=offer_statuses,
                              default=ACTIVE_STATUS)
    icon = models.CharField(max_length=255,
                            default=None, blank=True, null=True)
    advertiser = models.ForeignKey(
        'Advertiser',
        on_delete=models.SET_NULL,
        null=True, blank=True, default=None)

    def __str__(self):
        return f"({self.id}) {self.title}"


class Category(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class TrafficSource(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class OfferTrafficSource(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    traffic_source = models.ForeignKey(TrafficSource, on_delete=models.CASCADE)
    allowed = models.BooleanField(default=True)


FIXED_PAYOUT = 'Fixed'
PERCENT_PAYOUT = 'Percent'
payout_types = (
    (FIXED_PAYOUT, 'Fixed'),
    (PERCENT_PAYOUT, 'Percent'),
)


class Goal(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Currency(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Payout(models.Model):

    class Meta:
        ordering = ('-payout',)

    revenue = models.DecimalField(max_digits=7, decimal_places=2)
    payout = models.DecimalField(max_digits=7, decimal_places=2)
    countries = models.ManyToManyField(Country)
    goal_value = models.CharField(max_length=20, default='1')
    type = models.CharField(
        max_length=20,
        choices=payout_types,
        default=FIXED_PAYOUT
    )

    currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE
    )

    goal = models.ForeignKey(
        Goal,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    offer = models.ForeignKey(
        Offer,
        related_name='payouts',
        on_delete=models.CASCADE
    )


class Advertiser(models.Model):
    company = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    contact_person = models.CharField(max_length=64, default='')
    messenger = models.CharField(max_length=64, default='')
    site = models.CharField(max_length=64, default='')
    comment = models.TextField()

    def __str__(self):
        return self.company
