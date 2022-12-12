# Generated by Django 4.0.4 on 2022-11-15 13:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tests', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Назва курсу')),
                ('course_slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('subject', models.CharField(max_length=255, verbose_name='Предмет')),
                ('date_creating', models.DateField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-pk'],
            },
        ),
        migrations.CreateModel(
            name='AssignedTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_date', models.DateField(auto_now_add=True, verbose_name='Дата призначення')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.courseconfig')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.testsconfig')),
            ],
            options={
                'ordering': ['-pk'],
            },
        ),
    ]
