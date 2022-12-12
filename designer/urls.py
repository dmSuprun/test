from django.urls import path
from .views import *

urlpatterns = [
    path('', designer,name='designer'),
    path('test/',create_test, name='create_test'),
    path('test/<slug:test_slug>/update/', update_test, name='update_test'),
    path('test/<slug:test_slug>/delete/', delete_test, name='delete_test'),
    path('<slug:test_slug>/task/', create_tasks_to_test, name='create_task'),
    path('<slug:test_slug>/task/<int:pk_this_task>/update/in_template/<int:num_task_in_designer_template>/', update_task, name='update_task'),
    path('<slug:test_slug>/task/<int:pk_this_task>/delete/', delete_task, name='delete_task'),
    path('course/', create_course, name='create_course'),
    path('show_tests/', show_all_tests, name='show_all_tests'),
    path('update_testcase/<int:testcase_pk>/in_template/<int:case_number_in_designer_template>/', update_testcase, name='testcaseupdate'),
    path('create_testcase/for_task/<int:task_pk>/',create_testcase_to_task,name='create_testcase'),
    path('delete_testcase/from_task/testcase/<int:testcase_pk>/', delete_testcase_from_task,name='delete_testcase')

]