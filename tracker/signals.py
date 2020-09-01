from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Conversion
from postback.tasks.send_postback import send_postback


@receiver(post_save, sender=Conversion)
def on_conversion_created(sender, instance, created, **kwargs):
    if created:
        cv = {
            'affiliate_id': instance.affiliate_id,
            'offer_id': instance.offer_id,
            'sub1': instance.sub1,
            'sub2': instance.sub2,
            'sub3': instance.sub3,
            'sub4': instance.sub4,
            'sub5': instance.sub5,
            'payout': instance.payout,
            'goal_value': instance.goal_value,
            'currency': instance.currency.code if instance.currency else '',
        }
        send_postback.delay(cv)
