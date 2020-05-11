# Generated by Django 3.0.5 on 2020-05-10 15:51

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
                ('min_th', models.IntegerField()),
                ('min_pr', models.IntegerField()),
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
            options={
                'ordering': ['sub_dept_no', 'sem', 'sub_no'],
            },
        ),
        migrations.CreateModel(
            name='student',
            fields=[
                ('enroll_no', models.TextField(max_length=20, primary_key=True, serialize=False)),
                ('fname', models.TextField(max_length=50)),
                ('lname', models.TextField(max_length=50)),
                ('d2d', models.TextField(default='No', max_length=10)),
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
                ('result_status', models.TextField(default='None', max_length=30)),
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
        ),
        migrations.CreateModel(
            name='backlog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.TextField(max_length=30)),
                ('back_enroll_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.student')),
                ('back_sub_no', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='job.subjects')),
            ],
        ),
        migrations.AddConstraint(
            model_name='subjects',
            constraint=models.UniqueConstraint(fields=('sub_no', 'sub_dept_no', 'sem'), name='unique_subject'),
        ),
        migrations.AlterUniqueTogether(
            name='marks',
            unique_together={('marks_enroll_no', 'marks_sub_no')},
        ),
        migrations.AlterUniqueTogether(
            name='backlog',
            unique_together={('back_enroll_no', 'back_sub_no')},
        ),
    ]
