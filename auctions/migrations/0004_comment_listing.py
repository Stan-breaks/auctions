# Generated by Django 4.2.3 on 2023-07-18 14:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_bid_bid_bid_user_listing_status_listing_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='listing',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='auctions.listing'),
        ),
    ]
