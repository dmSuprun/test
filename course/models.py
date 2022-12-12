from django.db import models
from tests.models import *
from django.urls import reverse



class CourseConfig(models.Model):
    name=models.CharField('Назва курсу', max_length=255)
    course_slug=models.SlugField('URL', db_index=True, unique=True, max_length=255)
    subject=models.CharField('Предмет', max_length=255)
    date_creating=models.DateField(auto_now_add=True)
    def get_absolute_url(self):
        return reverse('detail_course', kwargs={'course_slug':self.course_slug})
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-pk']




class AssignedTest(models.Model):
    course=models.ForeignKey(CourseConfig, on_delete=models.CASCADE)
    test=models.ForeignKey('tests.TestsConfig',on_delete=models.CASCADE)
    assigned_date = models.DateField('Дата призначення', auto_now_add=True)
    class Meta:
        ordering = ['-pk']
    def __str__(self):
        return f'Назначеня для курсу {self.course}'



