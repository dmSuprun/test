from django.urls import path
from .views import *

urlpatterns = [
    path('<slug:course_slug>/<slug:test_slug>/start/', start_test, name='starttest'),
    path('check_one_task/<slug:course_slug>/<slug:test_slug>/<int:task_num>', check_task, name='check_task_before_end')

]