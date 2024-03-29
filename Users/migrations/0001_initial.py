# Generated by Django 4.1.6 on 2023-03-04 19:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeacherInCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('e_mail', models.EmailField(max_length=254, verbose_name='e-mail')),
                ('role', models.CharField(default='teacher', max_length=70, verbose_name='Роль на ресурсі')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.courseconfig')),
            ],
            options={
                'verbose_name': 'Вчителі на курсах',
                'verbose_name_plural': 'Вчителі на курсах',
            },
        ),
        migrations.CreateModel(
            name='StudentInCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('e_mail', models.EmailField(max_length=254, verbose_name='e-mail')),
                ('role', models.CharField(default='student', max_length=70, verbose_name='Роль на ресурсі')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.courseconfig')),
            ],
            options={
                'verbose_name': 'Учні на курсах',
                'verbose_name_plural': 'Учні на курсах',
            },
        ),
    ]
