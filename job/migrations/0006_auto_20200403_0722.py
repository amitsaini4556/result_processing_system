# Generated by Django 2.2.10 on 2020-04-03 01:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0005_auto_20200403_0716'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='result_enroll_no',
        ),
        migrations.AlterUniqueTogether(
            name='backlog',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='marks',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='backlog',
            name='back_enroll_no',
        ),
        migrations.RemoveField(
            model_name='marks',
            name='marks_enroll_no',
        ),
    ]
