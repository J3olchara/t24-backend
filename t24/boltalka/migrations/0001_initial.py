# Generated by Django 5.1.2 on 2024-10-26 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Voice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('short_text', models.TextField()),
                ('voice', models.FileField(upload_to='')),
                ('session_id', models.CharField(max_length=128)),
            ],
        ),
    ]
