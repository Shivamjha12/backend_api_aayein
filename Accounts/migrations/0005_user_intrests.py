# Generated by Django 4.2 on 2024-01-06 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0004_user_google_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='intrests',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
