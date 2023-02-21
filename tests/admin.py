from django.contrib import admin
from .models import *


class TestsConfigAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name_test', )}
    list_display = ('name_test', 'theme_test', 'author_of_test',
                    'create_func_template', 'autocomplete', 'pre_end_check')
    list_filter = ( 'theme_test','author_of_test','name_test')


class TestsSectionConfigAdmin(admin.ModelAdmin):
    list_display = ('test', 'function_name', 'question')


class DataForTestingCodeConfigAdmin(admin.ModelAdmin):
    list_display = ('section', 'input_test_data', 'input_test_data_type',
                    'output_test_data', 'output_test_data_type',
                    'num_of_point')


admin.site.register(TestsConfig, TestsConfigAdmin)
admin.site.register(TestsSection, TestsSectionConfigAdmin)
admin.site.register(DataForTestingCode, DataForTestingCodeConfigAdmin)
