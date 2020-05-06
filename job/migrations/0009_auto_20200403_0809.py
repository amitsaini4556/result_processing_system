# Generated by Django 2.2.10 on 2020-04-03 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0008_auto_20200403_0809'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='subjects',
            name='ubique_subject',
        ),
        migrations.AddConstraint(
            model_name='subjects',
            constraint=models.UniqueConstraint(fields=('sub_no', 'sub_dept_no', 'sem'), name='unique_subject'),
        ),
    ]