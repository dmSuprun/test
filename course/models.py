import uuid
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


class AssignedMaterial(models.Model):
    course = models.ForeignKey(CourseConfig, on_delete=models.CASCADE)
    test = models.ForeignKey(TestsConfig,on_delete=models.CASCADE)
    material=models.ForeignKey('ScientificMaterials.ScientificMaterials',on_delete=models.CASCADE)
    assigned_material_date = models.DateField('Дата призначення', auto_now_add=True)


    class Meta:
        ordering = ['-pk']
    def __str__(self):
        return f'Матеріал для курсу - {self.course}'


class Comment(models.Model):
    comment_id = models.UUIDField(verbose_name='id коментаря', primary_key=True, default=uuid.uuid4, editable=False )
    course = models.ForeignKey(CourseConfig, on_delete=models.CASCADE)
    test = models.ForeignKey(TestsConfig,on_delete=models.CASCADE)
    sender = models.ForeignKey(User,on_delete=models.CASCADE, verbose_name='Відправник',related_name='sender')
    receiver = models.ForeignKey(User,on_delete=models.CASCADE, verbose_name='Отримувач', related_name='receiver')
    comment_text = models.TextField(verbose_name='Текст коментаря')
    add_comment_date = models.DateField('Дата відправлення', auto_now_add=True)
    class Meta:
        ordering = ['add_comment_date']




