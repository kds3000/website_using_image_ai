# Generated by Django 3.0.4 on 2020-03-05 12:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('image_prediction', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='name',
        ),
    ]
