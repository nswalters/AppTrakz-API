# Generated by Django 3.1.7 on 2021-03-06 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apptrakzapi', '0002_auto_20210306_0252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='post_link',
            field=models.URLField(),
        ),
    ]
