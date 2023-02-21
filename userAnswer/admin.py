from django.contrib import admin
from .models import *


class UserAnswerConfigAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'course', 'test_section', 'answer')
    list_filter = ( 'user',)


class UserWhoСompletedTestConfigAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'course', 'user_point', 'success_percent')
    list_filter = ('test', 'course', 'user')


class CheckinResultConfigAdmin(admin.ModelAdmin):
    list_display = ('answer', 'data_on_which_they_checked', 'user', 'course',
                    'test', 'actual_user_result')


admin.site.register(UserAnswer, UserAnswerConfigAdmin)
admin.site.register(UserWhoСompletedTest, UserWhoСompletedTestConfigAdmin)
admin.site.register(CheckinResult, CheckinResultConfigAdmin)
