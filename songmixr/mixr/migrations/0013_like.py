# Generated by Django 2.1.7 on 2019-05-01 21:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mixr', '0012_profile_photo_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like_for', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mixr.Profile')),
                ('like_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('playlist_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mixr.Playlist')),
            ],
        ),
    ]