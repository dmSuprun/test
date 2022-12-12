from django.http import Http404
from django.shortcuts import render
from tests.models import DataForTestingCode
from statistic.views import *
from userAnswer.models import CheckinResult
from statistic.views import get_user_by_email


def get_role(req):
    if req.user.is_anonymous:
        return 'anonymous'
    elif len(TeacherInCourse.objects.filter(e_mail=req.user.email))==0:
        if len(StudentInCourse.objects.filter(e_mail=req.user.email))==0:
            return 'anonymousStudent'
        return 'student'
    return 'teacher'


def index(request):

    TYPE_PAGE=get_role(request)

    if TYPE_PAGE == 'anonymous':
        context={
            'type':TYPE_PAGE

        }
    elif TYPE_PAGE == 'teacher':
        # get teachers courses
        this_teacher_in_teachers_model=TeacherInCourse.objects.filter(e_mail=request.user.email)
        courses_name=[]
        courses=[]
        for record in this_teacher_in_teachers_model:
            courses_name.append(f'{record.course.name},')
            courses.append(record.course)
        courses_name[-1]=courses_name[-1].replace(courses_name[-1][-1], '')
        # get num of student on course, who work with this teacher
        num_of_students_on_course={}
        course_and_average_mark ={}
        num_student_in_course_in_tamplate = {}
        count_all_test_in_course = {}
        test_average_in_course={}

        test_and_num_testcases={}

        num_passage_test_on_course = {}



        num_students_who_complete_all_assign_test={} #course-num
        for course in courses:
            students_in_this_course=StudentInCourse.objects.filter(course=course)
            LEN_ASSIGNED_TESTS=len(AssignedTest.objects.filter(course=course))
            num_of_students_on_course[course.name]=len(students_in_this_course)
            course_and_average_mark[course]=average_mark_in_course(course.course_slug)
            num_student_in_course_in_tamplate[course]=num_student_in_course(course.course_slug)
            count_all_test_in_course[course] = LEN_ASSIGNED_TESTS
            assign_tests =AssignedTest.objects.filter(course=course)
            test_and_it_average_mark_in_course = {}
            test_and_num_passage={}

            all_complete_students_num=0
            for student in students_in_this_course:
                try:
                    user_obj=get_user_by_email(student.e_mail)
                    if len(UserWhoСompletedTest.objects.filter(user=user_obj, course=course)) == LEN_ASSIGNED_TESTS:
                        all_complete_students_num+=1
                except Exception:
                    continue

            if all_complete_students_num == 0:
                num_students_who_complete_all_assign_test[course] = ':('
            else:
                num_students_who_complete_all_assign_test[course] =all_complete_students_num



            for test_tmp in assign_tests:

                average=get_average_mark_on_this_test_on_chossen_course(course.course_slug, test_tmp.test.slug)
                test_and_it_average_mark_in_course[test_tmp.test] = average
                test_and_num_testcases[test_tmp.test] = len(DataForTestingCode.objects.filter(section__test=test_tmp.test))
                test_and_num_passage[test_tmp.test] = len(UserWhoСompletedTest.objects.filter(course=course, test=test_tmp.test))
            test_average_in_course[course] = test_and_it_average_mark_in_course





            num_passage_test_on_course[course]=test_and_num_passage







        context = {
            'type':TYPE_PAGE,
            'courses':courses_name,
            'num_students_on_course':num_of_students_on_course.items(),
            'title': f'{request.user.first_name} {request.user.last_name}',
            'averages_mark':course_and_average_mark.items(),
            'num_student_in_course':num_student_in_course_in_tamplate.items(),
            'count_tests':count_all_test_in_course.items(),
            'test_average_in_course':test_average_in_course.items(),
            'test_and_num_testcases':test_and_num_testcases.items(),
            'passage_num':num_passage_test_on_course.items(),
            'num_students_who_complete_all_assign_test':num_students_who_complete_all_assign_test.items()


        }

    elif TYPE_PAGE == 'student':
        # get this student courses
        this_student_info = StudentInCourse.objects.filter(e_mail=request.user.email)
        this_student_courses = []
        names_courses = []
        for stud in this_student_info:
            this_student_courses.append(stud.course)
            names_courses.append(f'{stud.course.name},')
        names_courses[-1] = names_courses[-1].replace(names_courses[-1][-1], '')
        # get this student teacher
        all_course_teachers = {}
        for course in this_student_courses:
            all_course_teachers[course] = TeacherInCourse.objects.filter(course__name=course)

        for course, teachers in all_course_teachers.items():
            teachers_on_this_course = []
            for teacher in teachers:
                try:
                    this_teacher_in_user_model = User.objects.get(email=teacher.e_mail)
                except:
                    this_teacher_in_user_model =f'Не автентифікований({teacher.e_mail}),'
                teachers_on_this_course.append(this_teacher_in_user_model)
            all_course_teachers[course] = teachers_on_this_course
        for course, teachers in all_course_teachers.items():
            create_this_user = []
            for teacher in teachers:

                try:
                    create_this_user.append(f'{teacher.first_name} {teacher.last_name},')
                except:
                    create_this_user.append(f'{teacher}')
            all_course_teachers[course] = create_this_user

        for course, teachers in all_course_teachers.items():
            try:
                teachers[-1] = teachers[-1].replace(',', ' ')
            except Exception:
                continue


        # get courses subjects
        average_mark = None
        subjects_on_course = {}
        course_and_num_students= {}
        ratings={}
        corse_average={}
        my_average={}
        courses = []
        my_results={}

        for course in this_student_courses:
            courses.append(course)
            subjects_on_course[course.name] = course.subject
            course_and_num_students[course] = num_student_in_course(course.course_slug)
            ratings[course] = student_position_in_course(course.course_slug, request.user.email)
            corse_average[course]=average_mark_in_course(course.course_slug)
            my_average[course]=get_student_average_in_course(course.course_slug, request.user.email)
            my_results[course]=UserWhoСompletedTest.objects.filter(user=request.user, course=course)

        cases_total_num={}
        for course, testing_results in my_results.items():
            for test_result in testing_results:
                try:
                    cases_total_num[test_result.test]=len(DataForTestingCode.objects.filter(section__test=test_result.test))  # якщо додавати до перевірок і поле курс, то тут потрібно додати фильтр по курсаам
                except KeyError:
                    continue


        completed_test_cases = {}
        for course, testing_results in my_results.items():
            tmp_tests_info = {}
            for testing_res in testing_results:
                tmp_tests_info[testing_res.test]=len(CheckinResult.objects.filter(testing_result=True, test=testing_res.test, course=testing_res.course, user=testing_res.user))

            completed_test_cases[course] = tmp_tests_info



        # графік успішності
        marks=[]
        dates = []
        this_student_all_result = UserWhoСompletedTest.objects.filter(user=request.user)
        for result in this_student_all_result:
            marks.append(str(result.user_point))
            dates.append(str(result.date_completion)[0:10])








        context = {
            'type': TYPE_PAGE,
            'courses': names_courses,
            'teachers_on_course': all_course_teachers.items(),
            'subjects': subjects_on_course.items(),
            'title': f'{request.user.first_name} {request.user.last_name}',
            'courses':courses,
            'num_students':course_and_num_students.items(),
            'rating':ratings.items(),
            'average':my_average.items(),
            'course_average':corse_average.items(),
            'my_res':my_results.items(),
            'cases_total_num':cases_total_num.items(),
            'cases_complete_num':completed_test_cases.items(),
            'marks':' '.join(marks),
            'dates': ' '.join(dates)


        }

    else:
        context = {
            'type': TYPE_PAGE,
            'courses': [' Користувач не зареєстрований'],
            'title': f'{request.user.first_name} {request.user.last_name}'

        }
    return render(request, 'staticPages/index.html', context=context)









    

def about_page(request):
    get_header_type=get_role(request)
    context={
        'type':get_header_type
    }
    return render(request, 'staticPages/static-pages/about.html', context=context)


def tips_page(request):
    get_header_type = get_role(request)
    context = {
        'type': get_header_type
    }


    return render(request, 'staticPages/static-pages/tips.html',context=context)




def faq_page(request):
    get_header_type = get_role(request)
    context = {
        'type': get_header_type
    }



    return render(request, 'staticPages/static-pages/faq.html',context=context )

