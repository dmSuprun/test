from django.contrib import admin
from .models import *

class CourseConfigAdmin(admin.ModelAdmin):
    prepopulated_fields = {'course_slug':('name',)}
admin.site.register(CourseConfig, CourseConfigAdmin)
admin.site.register(AssignedTest)
admin.site.register(AssignedMaterial)
admin.site.register(Comment)



