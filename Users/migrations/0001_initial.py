# Generated by Django 4.0.4 on 2022-11-15 13:18

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
        ),
        migrations.CreateModel(
            name='StudentInCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('e_mail', models.EmailField(max_length=254, verbose_name='e-mail')),
                ('role', models.CharField(default='student', max_length=70, verbose_name='Роль на ресурсі')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.courseconfig')),
            ],
        ),
    ]