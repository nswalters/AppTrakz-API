# Generated by Django 3.1.7 on 2021-03-13 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apptrakzapi', '0009_jobcontact_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='deleted',
            field=models.DateTimeField(editable=False, null=True),
        ),
    ]