# Generated by Django 2.2.10 on 2020-04-01 02:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='department',
            fields=[
                ('dept_no', models.IntegerField(primary_key=True, serialize=False)),
                ('dept_name', models.TextField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='scheme',
            fields=[
                ('scheme_no', models.IntegerField(primary_key=True, serialize=False)),
                ('theory_cr', models.IntegerField()),
                ('practical_cr', models.IntegerField()),
                ('max_th', models.IntegerField()),
                ('max_pr', models.IntegerField()),
                ('max_mid', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='subjects',
            fields=[
                ('sub_no', models.TextField(max_length=20, primary_key=True, serialize=False)),
                ('sub_name', models.TextField(default='name', max_length=50)),
                ('sem', models.IntegerField()),
                ('sub_stu_scheme', models.IntegerField()),
                ('sub_dept_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.department')),
                ('sub_scheme_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.scheme')),
            ],
        ),
        migrations.CreateModel(
            name='student',
            fields=[
                ('enroll_no', models.TextField(max_length=20, primary_key=True, serialize=False)),
                ('fname', models.TextField(max_length=50)),
                ('lname', models.TextField(max_length=50)),
                ('student_scheme_year', models.IntegerField(default=0)),
                ('student_dept_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.department')),
            ],
        ),
        migrations.CreateModel(
            name='result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sem1', models.FloatField(default=0)),
                ('sem2', models.FloatField(default=0)),
                ('sem3', models.FloatField(default=0)),
                ('sem4', models.FloatField(default=0)),
                ('sem5', models.FloatField(default=0)),
                ('sem6', models.FloatField(default=0)),
                ('sem7', models.FloatField(default=0)),
                ('sem8', models.FloatField(default=0)),
                ('ogpa', models.FloatField(default=0)),
                ('previous_grades', models.FloatField(default=0)),
                ('total_credits_hour', models.IntegerField(default=0)),
                ('result_enroll_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.student')),
            ],
        ),
        migrations.CreateModel(
            name='marks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('th', models.IntegerField()),
                ('pr', models.IntegerField()),
                ('mid', models.IntegerField()),
                ('current_result', models.FloatField()),
                ('current_cr', models.IntegerField(default=0)),
                ('marks_enroll_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.student')),
                ('marks_sub_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.subjects')),
            ],
            options={
                'unique_together': {('marks_enroll_no', 'marks_sub_no')},
            },
        ),
        migrations.CreateModel(
            name='backlog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('back_enroll_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.student')),
                ('back_sub_no', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='job.subjects')),
            ],
            options={
                'unique_together': {('back_enroll_no', 'back_sub_no')},
            },
        ),
    ]
