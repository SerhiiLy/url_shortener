# Generated by Django 4.0.2 on 2022-02-16 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shorter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='urldata',
            name='url_was_shorted',
            field=models.IntegerField(default=1),
        ),
    ]