# Generated by Django 2.2.10 on 2020-04-12 16:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0012_student_ded'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='ded',
            new_name='d2d',
        ),
    ]
