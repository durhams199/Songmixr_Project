# Generated by Django 2.1.7 on 2019-05-01 23:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mixr', '0013_like'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='like_for',
        ),
    ]
