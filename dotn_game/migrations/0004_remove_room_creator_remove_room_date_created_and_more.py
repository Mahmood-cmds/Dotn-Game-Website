# Generated by Django 4.2.3 on 2023-09-04 10:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dotn_game', '0003_room_creator_room_date_created_room_player_1_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='creator',
        ),
        migrations.RemoveField(
            model_name='room',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='room',
            name='player_1',
        ),
        migrations.RemoveField(
            model_name='room',
            name='player_2',
        ),
        migrations.RemoveField(
            model_name='room',
            name='status',
        ),
    ]