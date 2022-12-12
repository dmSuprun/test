from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class TestsSection(models.Model):
    test = models.ForeignKey('TestsConfig', on_delete=models.CASCADE)
    function_name = models.CharField('Назва функції', max_length=255)
    question = models.TextField('Завдання')
    def __str__(self):
        return f'Завдання до тесту {self.test}'
    class Meta:
        ordering=['pk']



class TestsConfig(models.Model):
    name_test = models.CharField('Назва тесту', max_length=255)
    slug = models.SlugField('URL', max_length=255, unique=True, db_index=True, )
    theme_test = models.CharField('Опис тесту ', max_length=255)
    author_of_test = models.ForeignKey(User,on_delete=models.CASCADE, verbose_name='Автор тесту')
    max_test_result = models.FloatField('Максимальний бал тесту')
    # time_on_test = models.CharField('Час на проходження(у хв)',max_length=255)
    date_creating=models.DateField(auto_now_add=True)
    class Meta:
        ordering=['-pk']

    def __str__(self):
        return self.name_test




class DataForTestingCode(models.Model):
    section = models.ForeignKey('TestsSection', on_delete=models.CASCADE)
    input_test_data = models.CharField('Вхідні аргументи', max_length=255)
    input_test_data_type = models.CharField('Тип вхідних данних', max_length=255)
    output_test_data = models.CharField('Вихідні данні', max_length=255)
    output_test_data_type = models.CharField('Тип вихідних данних', max_length=255)
    num_of_point = models.FloatField('Кількість балів за вдалу перевірку')

    class Meta:
        ordering=['pk']

    def __str__(self):
        return f'Тесткейс {self.pk}'
