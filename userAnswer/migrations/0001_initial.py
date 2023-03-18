# Generated by Django 4.1.6 on 2023-03-04 19:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('course', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tests', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserWhoСompletedTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_point', models.FloatField(verbose_name='Кількість балів цього учня')),
                ('success_percent', models.FloatField(verbose_name='Коофіцієнт успішності')),
                ('date_completion', models.DateTimeField(auto_now_add=True, verbose_name='Дата завершення')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.courseconfig', verbose_name='Курс')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.testsconfig', verbose_name='Тест')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Учень')),
            ],
            options={
                'verbose_name': 'Завершені тестування',
                'verbose_name_plural': 'Завершені тестування',
            },
        ),
        migrations.CreateModel(
            name='UserAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField(blank=True, verbose_name='Відповідь')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.courseconfig')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.testsconfig')),
                ('test_section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.testssection')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Відповіді учнів',
                'verbose_name_plural': 'Відповіді учнів',
            },
        ),
        migrations.CreateModel(
            name='CheckinResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('testing_result', models.BooleanField(verbose_name='Залік')),
                ('actual_user_result', models.TextField(blank=True, null=True, verbose_name='Результат виконання коду учня')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userAnswer.useranswer', verbose_name='Відповідь')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.courseconfig', verbose_name='Курс')),
                ('data_on_which_they_checked', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.datafortestingcode', verbose_name='Дані для перевірки')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.testsconfig', verbose_name='Тест')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Користувач')),
            ],
            options={
                'ordering': ['pk'],
            },
        ),
    ]