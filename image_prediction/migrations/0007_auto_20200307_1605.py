# Generated by Django 3.0.4 on 2020-03-07 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image_prediction', '0006_auto_20200307_1559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='images_model/'),
        ),
    ]
