# Generated by Django 2.2.10 on 2020-04-08 15:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0010_auto_20200408_1647'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='backlog',
            name='clear_status',
        ),
    ]
