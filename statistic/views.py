from django.shortcuts import get_object_or_404
from course.models import CourseConfig
from Users.models import StudentInCourse,TeacherInCourse
from django.contrib.auth.models import User
from course.models import AssignedTest
from userAnswer.models import UserWhoСompletedTest
from tests.models import TestsConfig

def get_test_by_slug(slug):
    return get_object_or_404(TestsConfig, slug=slug)

def get_test_by_kwargs(**kwargs):
    return TestsConfig.objects.filter(**kwargs)
def get_students_by_course(course):
    return StudentInCourse.objects.filter(course=course)
def get_course_by_slug(course_slug):
    return get_object_or_404(CourseConfig, course_slug=course_slug)

def get_assign_test(course):
    return AssignedTest.objects.filter( course=course)

def get_user_by_email(email):
    return get_object_or_404(User, email=email)

def get_student_in_course(student_email, course):
    return StudentInCourse.objects.get(e_mail=student_email, course=course)


def percent_part(total_num, chosen_part):
    if total_num == 0:
        return ':('
    return (chosen_part * 100)/total_num


''' student statistic methods '''

def num_student_in_course(course_slug):
    STUDENT_NUM=0
    try:
        this_course = get_course_by_slug(course_slug)
        students = get_students_by_course(this_course)
    except Exception:
        return ':('
    for i in students:
        STUDENT_NUM+=1

    return STUDENT_NUM




def get_student_average_in_course(course_slug, student_email):
    TOTAL_MARK = 0
    STUDENT_MARK_NUMBER = 0

    try:
        this_course = get_course_by_slug(course_slug)
        tests = get_assign_test(this_course)
        student = get_user_by_email(student_email)
    except Exception:
        return ':('


    assign_tests = []

    for assign_ob in tests:
        assign_tests.append(assign_ob.test)


    for test in assign_tests:
        try:
            testing_result_obj= UserWhoСompletedTest.objects.get(test=test, course=this_course, user=student)
        except Exception:
            continue
        TOTAL_MARK+=testing_result_obj.user_point
        STUDENT_MARK_NUMBER+=1

    try:
        AVERAGE = round(TOTAL_MARK/STUDENT_MARK_NUMBER, 2)
    except ZeroDivisionError:
        return ':('

    return AVERAGE



def average_mark_in_course(course_slug):
    TOTAL_MARK = 0
    MARK_NUMBER = 0
    try:
        this_course = get_course_by_slug(course_slug)
        completed_tests=UserWhoСompletedTest.objects.filter(course=this_course)
    except Exception:
        return ':('


    for complete_test in completed_tests:
        TOTAL_MARK+=complete_test.user_point
        MARK_NUMBER+=1

    try:
        AVERAGE = round(TOTAL_MARK/MARK_NUMBER, 2)
    except ZeroDivisionError:
        return ':('

    return AVERAGE



def student_position_in_course(course_slug, student_email):
    try:
        this_course = get_course_by_slug(course_slug)
        student = get_user_by_email(student_email)
        student_in_course = get_student_in_course(student_email, this_course)
        all_students =get_students_by_course(this_course)
        student_num = num_student_in_course(course_slug)

    except Exception:
        return ':('




    students = {}

    for student in all_students:
        tmp_average = get_student_average_in_course(course_slug, student.e_mail)
        students[student.e_mail] = tmp_average


    if students[student_email] == ':(':
        return students[student_email]

    left_limit = students[student_email] - 3
    right_limit = students[student_email] + 3


    Count_User_In_Limits = 0

    for e,ob in students.items():
        if ob == ':(':
            continue
        elif ob >= left_limit and ob <= right_limit and e != student_email:
            Count_User_In_Limits+=1


    this_user_percent= percent_part(student_num, Count_User_In_Limits)
    if this_user_percent == ':(' or this_user_percent == 0:
        return ':('
    return f'{round((this_user_percent),1)}% учнів мають аналогічні результати!'












'''teacher statistic '''
def get_average_mark_on_this_test_on_chossen_course(course_slug,test_slug):
    TOTAL_MARK = 0
    MARK_NUMBER = 0
    try:
        this_course = get_course_by_slug(course_slug)
        this_test = get_test_by_slug(slug=test_slug)
        this_test_results=UserWhoСompletedTest.objects.filter(course=this_course, test=this_test)

        for result in this_test_results:
            print(result.date_completion)
            TOTAL_MARK+=result.user_point
            MARK_NUMBER+=1
        return round(TOTAL_MARK/MARK_NUMBER,2)

    except Exception:
        return ':('





