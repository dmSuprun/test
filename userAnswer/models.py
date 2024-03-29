from django.db import models
from course.models import CourseConfig
from tests.models import TestsSection, TestsConfig, DataForTestingCode
from django.contrib.auth.models import User


class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(TestsConfig, on_delete=models.CASCADE)
    course = models.ForeignKey(CourseConfig, on_delete=models.CASCADE)
    test_section = models.ForeignKey(TestsSection, on_delete=models.CASCADE)
    answer = models.TextField('Відповідь', blank=True)

    class Meta:
      verbose_name = 'Відповіді учнів'
      verbose_name_plural = 'Відповіді учнів'


class CheckinResult(models.Model):
    answer = models.ForeignKey(UserAnswer,
                               on_delete=models.CASCADE,
                               verbose_name='Відповідь')
    data_on_which_they_checked = models.ForeignKey(
        DataForTestingCode,
        on_delete=models.CASCADE,
        verbose_name='Дані для перевірки')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name='Користувач')
    course = models.ForeignKey(CourseConfig,
                               on_delete=models.CASCADE,
                               verbose_name='Курс')
    test = models.ForeignKey(TestsConfig,
                             on_delete=models.CASCADE,
                             verbose_name='Тест')
    testing_result = models.BooleanField('Залік')
    actual_user_result = models.TextField('Результат виконання коду учня', null=True, blank=True)
    
    

    class Meta:
        ordering = ['pk']


class UserWhoСompletedTest(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name='Учень')
    course = models.ForeignKey(CourseConfig,
                               on_delete=models.CASCADE,
                               verbose_name='Курс')
    test = models.ForeignKey(TestsConfig,
                             on_delete=models.CASCADE,
                             verbose_name='Тест')
    user_point = models.FloatField('Кількість балів цього учня')
    success_percent = models.FloatField('Коофіцієнт успішності')
    date_completion = models.DateTimeField('Дата завершення',
                                           auto_now_add=True)
    class Meta:
      verbose_name = 'Завершені тестування'
      verbose_name_plural = 'Завершені тестування'
