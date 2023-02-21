from django.contrib import admin
from .models import *


class CourseConfigAdmin(admin.ModelAdmin):
    prepopulated_fields = {'course_slug': ('name', )}
    list_display = ('name', 'subject', 'date_creating')

class AssignedTestConfigAdmin(admin.ModelAdmin):

    list_display = ('course', 'test', 'assigned_date')

class AssignedMaterialConfigAdmin(admin.ModelAdmin):
    list_display = ('course', 'test', 'material')


class CommentConfigAdmin(admin.ModelAdmin):
    list_display = ( 'course', 'test','sender','receiver','comment_text')


admin.site.register(CourseConfig, CourseConfigAdmin)
admin.site.register(AssignedTest, AssignedTestConfigAdmin)
admin.site.register(AssignedMaterial,AssignedMaterialConfigAdmin)
admin.site.register(Comment,CommentConfigAdmin)
