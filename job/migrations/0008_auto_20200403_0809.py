# Generated by Django 2.2.10 on 2020-04-03 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0007_auto_20200403_0724'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='subjects',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='subjects',
            constraint=models.UniqueConstraint(fields=('sub_no', 'sub_dept_no', 'sem'), name='ubique_subject'),
        ),
    ]
