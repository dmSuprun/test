from django.urls import path
from .views import *

urlpatterns = [
    path('', show_all_course, name='all_course'),
    path('detail/<slug:course_slug>/', show_detail_course, name='detail_course'),
    path('<slug:course_slug>/delete/', delete_course, name='delete_course'),
    path('<slug:course_slug>/add-students/', add_students, name='add_students'),
    path('<slug:course_slug>/add-teachers/', add_teachers, name='add_teachers'),
    path('<slug:course_slug>/add-student/', add_only_one_student, name='add_only_one_student'),
    path('<slug:course_slug>/add-teacher/', add_only_one_teacher, name='add_only_one_teacher'),
    path('<slug:course_slug>/assign/', assign_test_on_course, name='assign_test'),
    path('<slug:course>/assign/<slug:test>/', assign, name='assign_complete'),
    path('<slug:test>/read_result/<slug:course>', test_result, name='read_result'),
    path('<slug:test>/read_result/<slug:course>/<str:username>/', detail_test_result, name='read_detail_result'),
    path('<slug:test_slug>/delete_user_result/<slug:course_slug>/<str:username>/', delete_test_result, name='delete_result' ),
    path('delete_student/<str:student_email>/from_course/<slug:course_slug>/', delete_student_from_course, name='delete_student'),
    path('delete_teacher/<str:teacher_email>/from_course/<slug:course_slug>/', delete_teacher_from_course,name='delete_teacher'),
    path('<slug:course_slug>/delete/assign_test/<slug:test_slug>/', delete_assign_test, name='delete_assign_test'),
    path('update_course_name/<slug:course_slug>/', update_course_name ,name='update_course_name'),
    path('update_course_subject/<slug:course_slug>/', update_course_subject, name='update_course_subject')

]