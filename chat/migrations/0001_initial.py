# Generated by Django 3.2.11 on 2022-01-11 13:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatingRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('user1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user1_chating_room', to=settings.AUTH_USER_MODEL)),
                ('user2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user2_chating_room', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user1', 'user2')},
            },
        ),
        migrations.CreateModel(
            name='ChatingRoomMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('slug', models.SlugField()),
                ('seen', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('chat_room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ch_messages', to='chat.chatingroom')),
                ('sent_by_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='msgs_sent_by', to=settings.AUTH_USER_MODEL)),
                ('user1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user1_msgs', to=settings.AUTH_USER_MODEL)),
                ('user2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user2_msgs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
    ]
