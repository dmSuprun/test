from django.contrib import admin
from .models import *
class TestsConfigAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name_test',)}

admin.site.register(TestsConfig, TestsConfigAdmin)
admin.site.register(TestsSection)
admin.site.register(DataForTestingCode)


