from django.db import models
from course.models import *





class StudentInCourse(models.Model):
    e_mail=models.EmailField('e-mail')
    role=models.CharField('Роль на ресурсі',default='student', max_length=70)
    course=models.ForeignKey('course.CourseConfig', on_delete=models.CASCADE)

    class Meta:
      verbose_name = 'Учні на курсах'
      verbose_name_plural = 'Учні на курсах'

    def __str__(self):
        return f'{self.role} на курсі {self.course}'



class TeacherInCourse(models.Model):
    e_mail=models.EmailField('e-mail')
    role=models.CharField('Роль на ресурсі',default='teacher', max_length=70)
    course=models.ForeignKey('course.CourseConfig', on_delete=models.CASCADE)

    class Meta:
      verbose_name = 'Вчителі на курсах'
      verbose_name_plural = 'Вчителі на курсах'

    def __str__(self):
        return f'{self.role} на курсі {self.course}'

