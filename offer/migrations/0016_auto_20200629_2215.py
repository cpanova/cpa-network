# Generated by Django 3.0.7 on 2020-06-29 22:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0015_offer_advertiser'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payout',
            options={'ordering': ('-payout',)},
        ),
    ]