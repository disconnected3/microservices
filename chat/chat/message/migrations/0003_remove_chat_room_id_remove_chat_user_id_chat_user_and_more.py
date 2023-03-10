# Generated by Django 4.1.1 on 2022-09-08 12:24

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("message", "0002_userprofile_friend"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="chat",
            name="room_id",
        ),
        migrations.RemoveField(
            model_name="chat",
            name="user_id",
        ),
        migrations.AddField(
            model_name="chat",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="chat_user_related",
                to="message.userprofile",
            ),
        ),
        migrations.CreateModel(
            name="Room",
            fields=[
                (
                    "uid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "friends",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="message.friend"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="chat",
            name="room",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="chat_room_related",
                to="message.room",
            ),
        ),
    ]
