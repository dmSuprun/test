from django.contrib import admin
from .models import *


class UsersInCourseUserAnswerConfigAdmin(admin.ModelAdmin):
    list_display = ('e_mail', 'role', 'course')


admin.site.register(StudentInCourse, UsersInCourseUserAnswerConfigAdmin)
admin.site.register(TeacherInCourse, UsersInCourseUserAnswerConfigAdmin)
