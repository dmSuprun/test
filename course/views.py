import json
from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from userAnswer.models import UserAnswer, CheckinResult, UserWhoСompletedTest
from staticPages.views import get_role
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib.auth.models import User
from django.http import HttpResponse
from designer.utils import transliteration
from django.db import transaction
from ScientificMaterials.material_services.crud import read_only_one_material, read_materials
from .models import AssignedMaterial


@login_required
def show_all_course(request):
    user_role = get_role(request)
    if user_role == 'anonymousStudent':
        context = {'title': 'Курси', 'type': user_role}

    elif user_role == 'student':
        courses = []
        teachers_on_course = {}
        this_student_info = StudentInCourse.objects.filter(
            e_mail=request.user.email)
        for record in this_student_info:
            courses.append(record.course)

        for course in courses:
            list_with_teachers = []
            teachers_local = TeacherInCourse.objects.filter(course=course)
            for teacher in teachers_local:
                try:
                    tmp = User.objects.get(email=teacher.e_mail)
                    this_teacher = f'{tmp.first_name} {tmp.last_name},'
                except:
                    this_teacher = f'Не автентифікований({teacher.e_mail}),'
                list_with_teachers.append(this_teacher)
            teachers_on_course[course] = list_with_teachers
        for val in teachers_on_course.values():
            try:
                val[-1] = val[-1].replace(val[-1][-1], '')
            except Exception:
                continue

        context = {
            'title': 'Курси',
            'type': user_role,
            'courses': teachers_on_course.items(),
        }
    else:
        courses = []
        teachers_on_course = {}
        this_teacher_info = TeacherInCourse.objects.filter(
            e_mail=request.user.email)
        for record in this_teacher_info:
            courses.append(record.course)

        for course in courses:
            list_with_teachers = []
            teachers_local = TeacherInCourse.objects.filter(course=course)
            for teacher in teachers_local:
                try:
                    tmp = User.objects.get(email=teacher.e_mail)
                    this_teacher = f'{tmp.first_name} {tmp.last_name},'
                except:
                    this_teacher = f'Не автентифікований({teacher.e_mail}),'
                list_with_teachers.append(this_teacher)
            teachers_on_course[course] = list_with_teachers
        for val in teachers_on_course.values():

            val[-1] = val[-1].replace(val[-1][-1], '')

        context = {
            'title': 'Курси',
            'type': user_role,
            'courses': teachers_on_course.items()
        }

    return render(request, 'course/all course.html', context=context)


@login_required
def show_detail_course(request, course_slug):

    user_role = get_role(request)
    post = get_object_or_404(CourseConfig, course_slug=course_slug)
    teachers = TeacherInCourse.objects.filter(course=post)
    teachers_em = [i.e_mail for i in teachers]
    teachers_result = {}

    for teacher in teachers:
        try:
            get_user = User.objects.get(email=teacher.e_mail)

            tmp = f'{get_user.first_name} {get_user.last_name}, '
        except:
            tmp = f'Не автентифікований ({teacher.e_mail}),'
        teachers_result[teacher.e_mail] = tmp

    get_students = StudentInCourse.objects.filter(course=post)
    students = {}  #email-name
    completed_tests = {}
    for student in get_students:
        try:
            tmp_user = User.objects.get(email=student.e_mail)
            get = f'{tmp_user.first_name} {tmp_user.last_name} '
            get_this_user_complete_test = UserWhoСompletedTest.objects.filter(
                user=tmp_user, course__course_slug=course_slug)

        except:
            get = f'Не автентифікований ({student.e_mail})'
            get_this_user_complete_test = None

        students[student.e_mail] = get
        completed_tests[student.e_mail] = get_this_user_complete_test

    num_students = len(students.values())
    num_teachers = len(teachers_result)
    ''' get tests and materials'''
    tests = AssignedTest.objects.filter(course=post)

    materials = AssignedMaterial.objects.filter(course=post)
    materials_and_test = {}

    for material in materials:
        materials_and_test[material] = material.test
    ''' get this student test result on course with dates '''
    get_all_results = UserWhoСompletedTest.objects.filter(
        user=request.user, course__course_slug=course_slug)
    COUNT_RESULT = len(get_all_results)
    marks = []
    dates = []
    for result in get_all_results:
        marks.append(str(result.user_point))
        dates.append(str(result.date_completion)[0:10])
    ''' результати '''
    test_results = {}

    for test_iter in tests:
        this_test_user_results = UserWhoСompletedTest.objects.filter(
            course=post, test=test_iter.test).order_by('user')
        test_results[test_iter.test] = this_test_user_results

    context = {
        'title':
        f'{post.name}',
        'type':
        user_role,
        'post':
        post,
        'teachers':
        teachers_result.items(),
        'students':
        students.items(),
        'num_students':
        num_students,
        'num_teachers':
        num_teachers,
        'tests':
        tests,
        'student_completed_tests':
        completed_tests.items(),
        'this_teacher_assign_test': [
            i.test for i in AssignedTest.objects.filter(
                course__course_slug=course_slug,
                test__author_of_test=request.user)
        ],
        'count_materials':
        len(materials_and_test),
        'materials':
        materials_and_test.items(),
        'COUNT_RESULT':
        COUNT_RESULT,
        'marks':
        ' '.join(marks),
        'dates':
        ' '.join(dates),
        'tests_results':
        test_results.items(),
        'teachers_em':
        teachers_em
    }
    return render(request, 'course/course.html', context=context)


def open_csv_file(file, this_user_role, slug_required_course):
    ''' this function open .csv file with e-mails, who send
    from the form. After register user with this e-mails on a course '''
    all_emails_in_line = []
    tmp_element_index_in_list = -1
    for line in file.readlines():
        all_emails_in_line.append(line.strip())
    for email in all_emails_in_line:
        tmp_element_index_in_list += 1
        tmp_email = ''
        for index_element_of_email in range(0, len(email)):
            tmp_email += str(chr(email[index_element_of_email]))
        all_emails_in_line[tmp_element_index_in_list] = tmp_email
    return all_emails_in_line


@login_required
def add_students(request, course_slug):
    '''this func get a file with student email, and transmits here to open_file_func'''

    if get_role(request) != 'teacher':
        return HttpResponse(
            '<h1 style="text-align:center;position:relative; top:10%;">Доступ заборонено!</h1>',
            status=403)
    this_course = get_object_or_404(CourseConfig, course_slug=course_slug)
    user_role = get_role(request)

    if request.method == 'POST':
        get_users_form = CreateUserForm(request.POST, request.FILES)

        if get_users_form.is_valid():
            try:
                method_name(course_slug, request, this_course, user_role)
            except RuntimeError:
                get_users_form.add_error('csv_file_with_emails',
                                         'Неможливо додати учнів до курсу!')

            else:
                return redirect(f'/course/detail/{course_slug}')

    else:
        get_users_form = CreateUserForm()
    context = {
        'type': user_role,
        'form': get_users_form,
        'title': 'Реєстрація студентів',
        'course': this_course,
        'add_teacher': False
    }
    return render(request, 'course/add_users.html', context=context)


@transaction.atomic
def method_name(course_slug, request, this_course, user_role):
    get_emails = (i for i in open_csv_file(
        request.FILES['csv_file_with_emails'], user_role, course_slug))
    for email in get_emails:

        data_for_form = {'e_mail': email, 'course': this_course}
        add_student_form = StudentInCourseForm(data_for_form)
        if add_student_form.is_valid():
            add_student_form.save()

        else:

            raise RuntimeError("error")


@login_required
def add_teachers(request, course_slug):
    '''this func get a file with student email, and transmits here to open_file_func'''
    if get_role(request) != 'teacher':
        return HttpResponse(
            '<h1 style="text-align:center;position:relative; top:10%;">Доступ заборонено!</h1>',
            status=403)
    this_course = get_object_or_404(CourseConfig, course_slug=course_slug)
    user_role = get_role(request)
    if request.method == 'POST':
        get_users_form = CreateUserForm(request.POST, request.FILES)
        if get_users_form.is_valid():
            try:
                add_teachers_logic(course_slug, request, this_course,
                                   user_role)
            except RuntimeError:

                get_users_form.add_error(
                    'csv_file_with_emails',
                    'Неможливо додати викладачів до курсу!')

            else:
                return redirect(f'/course/detail/{course_slug}')
    else:
        get_users_form = CreateUserForm()
    context = {
        'type': user_role,
        'form': get_users_form,
        'title': 'Реєстрація вчителів',
        'course': this_course,
        'add_teacher': True
    }
    return render(request, 'course/add_users.html', context=context)


@transaction.atomic
def add_teachers_logic(course_slug, request, this_course, user_role):
    get_emails = (i for i in open_csv_file(
        request.FILES['csv_file_with_emails'], user_role, course_slug))
    for email in get_emails:

        data_for_form = {'e_mail': email, 'course': this_course}
        add_teachers_form = TeacherInCourseForm(data_for_form)
        if add_teachers_form.is_valid():
            add_teachers_form.save()
        else:
            raise RuntimeError("error")


@login_required
def add_only_one_student(request, course_slug):
    if get_role(request) != 'teacher':
        return HttpResponse(
            '<h1 style="text-align:center;position:relative; top:10%;">Доступ заборонено!</h1>',
            status=403)
    this_course = get_object_or_404(CourseConfig, course_slug=course_slug)
    if request.method == 'POST':
        form = getEmail(request.POST)
        if form.is_valid():
            data = {
                'e_mail': form.cleaned_data['email'],
                'course': this_course
            }
            model_form = StudentInCourseForm(data)
            if model_form.is_valid():
                model_form.save()
                return redirect(f'/course/detail/{this_course.course_slug}')
            else:

                form.add_error(
                    'email',
                    ValidationError(model_form.errors.as_text()
                                    [12:len(model_form.errors.as_text())]))
    else:
        form = getEmail()

    context = {'type': get_role(request), 'form': form, 'title': 'Додати учня'}
    return render(request, 'course/add_student.html', context=context)


@login_required
def add_only_one_teacher(request, course_slug):
    if get_role(request) != 'teacher':
        return HttpResponse(
            '<h1 style="text-align:center;position:relative; top:10%;">Доступ заборонено!</h1>',
            status=403)
    this_course = get_object_or_404(CourseConfig, course_slug=course_slug)
    if request.method == 'POST':
        form = getEmail(request.POST)
        if form.is_valid():
            data = {
                'e_mail': form.cleaned_data['email'],
                'course': this_course
            }
            model_form = TeacherInCourseForm(data)
            if model_form.is_valid():
                model_form.save()
                return redirect(f'/course/detail/{this_course.course_slug}')
            else:

                form.add_error(
                    'email',
                    ValidationError(model_form.errors.as_text()
                                    [12:len(model_form.errors.as_text())]))
    else:
        form = getEmail()

    context = {
        'type': get_role(request),
        'form': form,
        'title': 'Додати викладача'
    }
    return render(request, 'course/add_teacher.html', context=context)


@login_required
def assign_test_on_course(request, course_slug):
    if get_role(request) != 'teacher':
        return HttpResponse(
            '<h1 style="text-align:center;position:relative; top:10%;">Доступ заборонено!</h1>',
            status=403)
    this_course = get_object_or_404(CourseConfig, course_slug=course_slug)
    get_all_teachers_on_this_course = TeacherInCourse.objects.filter(
        course=this_course)
    all_teachers = []
    test_queryset = []
    for teacherInCourse in get_all_teachers_on_this_course:
        try:
            tmp_user = User.objects.get(email=teacherInCourse.e_mail)
        except:
            continue
        all_teachers.append(tmp_user)
    for teacher in all_teachers:

        test_for_this_iteration_teacher = TestsConfig.objects.filter(
            author_of_test=teacher)
        test_queryset.append(test_for_this_iteration_teacher)

    assign_error = False

    if request.GET.get('error'):
        assign_error = True

    context = {
        'type': get_role(request),
        'tests': test_queryset,
        'course': this_course,
        'errors': assign_error,
        'title': 'Призначити тест',
        'test_who_assign_now': request.GET.get('test')
    }
    return render(request, 'course/assign_test.html', context=context)


@login_required
def assign(request, course, test):
    if get_role(request) != 'teacher':
        return HttpResponse(
            '<h1 style="text-align:center;position:relative; top:10%;">Доступ заборонено!</h1>',
            status=403)
    this_course = get_object_or_404(CourseConfig, course_slug=course)
    this_test = get_object_or_404(TestsConfig, slug=test)
    data_to_assign = {'course': this_course, 'test': this_test}
    assign = AssignTestForm(data_to_assign)
    if assign.is_valid():
        assign.save()
        return redirect(
            reverse('detail_course',
                    kwargs={'course_slug': this_course.course_slug}))
    error = f'error={True}&test={this_test.name_test}&'
    return redirect(
        f'/course/{this_course.course_slug}/assign/?error={error}/')


@login_required
def delete_course(request, course_slug):
    if get_role(request) != 'teacher':
        return HttpResponse(
            '<h1 style="text-align:center;position:relative; top:10%;">Доступ заборонено!</h1>',
            status=403)
    try:
        get_course = CourseConfig.objects.get(course_slug=course_slug)
        get_course.delete()
        return redirect(reverse('all_course'))
    except Exception:
        raise Http404


@login_required
def test_result(request, test, course):
    if get_role(request) != 'teacher':
        return HttpResponse(
            '<h1 style="text-align:center;position:relative; top:10%;">Доступ заборонено!</h1>',
            status=403)

    this_test = TestsConfig.objects.get(slug=test)
    this_course = CourseConfig.objects.get(course_slug=course)
    get_teachers_on_this_course = TeacherInCourse.objects.filter(
        course=this_course)
    teachers_emails = [i.e_mail for i in get_teachers_on_this_course]
    answers_with_teachers = UserAnswer.objects.filter(test=this_test,
                                                      course=this_course)
    all_answers_on_this_test = [
        i for i in answers_with_teachers if not i.user.email in teachers_emails
    ]
    all_tasks = TestsSection.objects.filter(test=this_test)

    task_rating = {}
    rating = 0
    for task in all_tasks:
        rating += 1
        task_rating[task] = rating
    answer_on_task = {}  # section : answer
    for answer in all_answers_on_this_test:
        answer_on_task[answer] = answer.test_section

    testing_code_result = CheckinResult.objects.filter(course=this_course,
                                                       test=this_test)

    testing_result = {}  #result_obj : answer_obj
    for test_res in testing_code_result:
        testing_result[test_res] = test_res.answer

    students = StudentInCourse.objects.filter(course=this_course)
    users = {}
    for student in students:
        try:
            this_user = User.objects.get(email=student.e_mail)
            users[
                f'{this_user.first_name} {this_user.last_name}'] = this_user.username
        except Exception:
            new_name = ''
            ind = 0
            for i in student.e_mail:

                if i != '@':
                    ind += 1
                    new_name += i
                else:
                    break
            users[f' Не автентифікований {new_name}'] = new_name

    context = {
        'type': get_role(request),
        'title': f'Результат тесту {this_test.name_test}',
        'course': this_course,
        'test': this_test,
        'tasks': task_rating.items(),
        'answers': answer_on_task.items(),
        'testcases_with_result': testing_result.items(),
        'users': users.items()
    }
    return render(request, 'course/testing_result.html', context=context)


@login_required
def detail_test_result(request, test, course, username):

    this_test = TestsConfig.objects.get(slug=test)
    this_course = CourseConfig.objects.get(course_slug=course)
    try:
        complete_result = UserWhoСompletedTest.objects.get(
            course=this_course, test=this_test, user__username=username)
    except Exception:
        complete_result = None

    this_user_answers = UserAnswer.objects.filter(test=this_test,
                                                  course=this_course,
                                                  user__username=username)
    num_answers = len(this_user_answers)
    all_task = TestsSection.objects.filter(test=this_test)

    task_rating = {}

    this_request_user = ''
    try:
        user = User.objects.get(username=username)
        this_request_user = f'{user.first_name} {user.last_name}'
    except Exception:
        this_request_user = username

    i = 0
    for task in all_task:
        i += 1
        task_rating[task] = i

    answer_on_task = {}  # section : answer
    for answer in this_user_answers:
        answer_on_task[answer] = answer.test_section

    try:
        checkin_results = CheckinResult.objects.filter(course=this_course,
                                                       test=this_test,
                                                       user__username=username)

        check_result = {}  #result_obj : answer_obj

        for case in checkin_results:
            check_result[case] = case.answer

    except Exception:
        check_result = {}
    ''' get all coments from db '''
    this_result_comments = Comment.objects.filter(course__course_slug=course,
                                                  test__slug=test,
                                                  receiver__username=username)

    context = {
        'type': get_role(request),
        'title': f'Результат {this_request_user}',
        'course': this_course,
        'test': this_test,
        'user': this_request_user,
        'tasks': task_rating.items(),
        'answers': answer_on_task.items(),
        'no_res': True if num_answers == 0 else False,
        'testcases': check_result.items(),
        'username_this_detail_user': username,
        'complete_result': complete_result,
        'comments': this_result_comments,
        'count_comment': len(this_result_comments)
    }
    return render(request, 'course/detail_result.html', context=context)


@login_required
def delete_assign_test(request, course_slug, test_slug):
    if get_role(request) != 'teacher':
        return HttpResponse(
            '<h1 style="text-align:center;position:relative; top:10%;">Доступ заборонено!</h1>',
            status=403)
    this_course = get_object_or_404(CourseConfig, course_slug=course_slug)
    this_test = get_object_or_404(TestsConfig,slug=test_slug)\

    #checkin result
    linked_records_with_checkin_result = CheckinResult.objects.filter(
        course=this_course, test=this_test)
    linked_records_with_checkin_result.delete()

    linked_records = 0
    # completed test
    linked_records_with_complete_test = UserWhoСompletedTest.objects.filter(
        course=this_course, test=this_test)
    linked_records_with_complete_test.delete()

    #answer
    linked_records_with_answers = UserAnswer.objects.filter(course=this_course,
                                                            test=this_test)
    linked_records_with_answers.delete()

    #assigned test
    linked_records_with_assigned_test = get_object_or_404(AssignedTest,
                                                          course=this_course,
                                                          test=this_test)
    linked_records_with_assigned_test.delete()

    return redirect(
        reverse('detail_course', kwargs={'course_slug': course_slug}))


@login_required
def delete_test_result(request, test_slug, course_slug, username):
    if get_role(request) != 'teacher':
        return HttpResponse(
            '<h1 style="text-align:center;position:relative; top:10%;">Доступ заборонено!</h1>',
            status=403)
    # complete result
    complete_result = UserWhoСompletedTest.objects.filter(
        course__course_slug=course_slug,
        user__username=username,
        test__slug=test_slug)
    complete_result.delete()

    #answers
    answers = UserAnswer.objects.filter(course__course_slug=course_slug,
                                        user__username=username,
                                        test__slug=test_slug)
    answers.delete()

    #checkin

    checkin_result_obj = CheckinResult.objects.filter(
        course__course_slug=course_slug,
        user__username=username,
        test__slug=test_slug)
    checkin_result_obj.delete()
    return redirect(
        reverse('read_result',
                kwargs={
                    'test': test_slug,
                    'course': course_slug
                }))


@login_required
def delete_student_from_course(request, student_email, course_slug):
    if get_role(request) != 'teacher':
        return HttpResponse(
            '<h1 style="text-align:center;position:relative; top:10%;">Доступ заборонено!</h1>',
            status=403)

    get_student = get_object_or_404(StudentInCourse,
                                    course__course_slug=course_slug,
                                    e_mail=student_email).delete()
    compl_tests_on_this_course = UserWhoСompletedTest.objects.filter(
        user__email=student_email, course__course_slug=course_slug)
    compl_tests_on_this_course.delete()

    answer_on_this_course = UserAnswer.objects.filter(
        user__email=student_email, course__course_slug=course_slug)
    answer_on_this_course.delete()

    checkin_results_on_this_course = CheckinResult.objects.filter(
        user__email=student_email, course__course_slug=course_slug)
    checkin_results_on_this_course.delete()
    return redirect(
        reverse('detail_course', kwargs={'course_slug': course_slug}))


@login_required
def delete_teacher_from_course(request, teacher_email, course_slug):
    if get_role(request) != 'teacher':
        return HttpResponse(
            '<h1 style="text-align:center;position:relative; top:10%;">Доступ заборонено!</h1>',
            status=403)

    get_teacher = get_object_or_404(TeacherInCourse,
                                    course__course_slug=course_slug,
                                    e_mail=teacher_email).delete()
    compl_tests_on_this_course = UserWhoСompletedTest.objects.filter(
        user__email=teacher_email, course__course_slug=course_slug)
    compl_tests_on_this_course.delete()

    answer_on_this_course = UserAnswer.objects.filter(
        user__email=teacher_email, course__course_slug=course_slug)
    answer_on_this_course.delete()

    checkin_results_on_this_course = CheckinResult.objects.filter(
        user__email=teacher_email, course__course_slug=course_slug)
    checkin_results_on_this_course.delete()

    if len(TeacherInCourse.objects.filter(
            course__course_slug=course_slug)) == 0:
        tmp_course = get_object_or_404(CourseConfig,
                                       course_slug=course_slug).delete()
        return redirect(reverse('index_page'))

    return redirect(
        reverse('detail_course', kwargs={'course_slug': course_slug}))


@login_required
def update_course_name(request, course_slug):
    if get_role(request) != 'teacher':
        return HttpResponse(
            '<h1 style="text-align:center;position:relative; top:10%;">Доступ заборонено!</h1>',
            status=403)
    if request.method == 'POST':
        get_course = get_object_or_404(CourseConfig, course_slug=course_slug)
        if request.POST['newName'] == '':
            return HttpResponse(
                '<h1 style="text-align:center;position:relative; top:10%;">Неможливо оновити назву</h1>',
                status=400)
        try:
            old_slug = str(get_course.course_slug)
            extra_text_in_slug_index = str(old_slug).index('-')
            postfix = old_slug[extra_text_in_slug_index:len(old_slug)]
            get_course.name = request.POST['newName']
            get_course.course_slug = transliteration(
                request.POST['newName']) + postfix
            get_course.save()
        except ValueError:
            get_course.name = request.POST['newName']
            get_course.course_slug = transliteration(request.POST['newName'])
            get_course.save()
        except Exception:
            return redirect(
                reverse('detail_course', kwargs={'course_slug': course_slug}))

        return redirect(
            reverse('detail_course',
                    kwargs={'course_slug': get_course.course_slug}))
    else:
        return HttpResponse(
            '<h1 style="text-align:center;position:relative; top:10%;">Неможливо оновити дані про курс!</h1>',
            status=405)


@login_required
def update_course_subject(request, course_slug):
    if get_role(request) != 'teacher':
        return HttpResponse(
            '<h1 style="text-align:center;position:relative; top:10%;">Доступ заборонено!</h1>',
            status=403)
    if request.method == 'POST':
        get_course = get_object_or_404(CourseConfig, course_slug=course_slug)

        try:
            get_course.subject = request.POST['newSubject']
            get_course.save()
        except Exception:
            return redirect(
                reverse('detail_course', kwargs={'course_slug': course_slug}))
        return redirect(
            reverse('detail_course', kwargs={'course_slug': course_slug}))

    else:
        return HttpResponse(
            '<h1 style="text-align:center;position:relative; top:10%;">Неможливо оновити дані про курс!</h1>',
            status=405)


@login_required
def leave_course(request, course_slug):
    get_student = get_object_or_404(StudentInCourse,
                                    course__course_slug=course_slug,
                                    e_mail=request.user.email).delete()
    compl_tests_on_this_course = UserWhoСompletedTest.objects.filter(
        user__email=request.user.email, course__course_slug=course_slug)
    compl_tests_on_this_course.delete()

    answer_on_this_course = UserAnswer.objects.filter(
        user__email=request.user.email, course__course_slug=course_slug)
    answer_on_this_course.delete()

    checkin_results_on_this_course = CheckinResult.objects.filter(
        user__email=request.user.email, course__course_slug=course_slug)
    checkin_results_on_this_course.delete()
    return redirect(reverse('index_page'))


@login_required
def add_comment(request, course_slug, test_slug, receiver):
    get_course = get_object_or_404(CourseConfig, course_slug=course_slug)
    get_test = get_object_or_404(TestsConfig, slug=test_slug)
    rec = get_object_or_404(User, username=receiver)
    if request.method == 'POST':
        data = {
            'course': get_course,
            'test': get_test,
            'sender': request.user,
            'receiver': rec,
            'comment_text': request.POST.get('comment_text')
        }
        form = addCommentForm(data)
        if form.is_valid():
            form.save()

            return redirect(
                reverse('read_detail_result',
                        kwargs={
                            'username': receiver,
                            'course': course_slug,
                            'test': test_slug
                        }))


def get_async_comments(request, course_slug, test_slug, receiver):
    this_result_comments = Comment.objects.filter(
        course__course_slug=course_slug,
        test__slug=test_slug,
        receiver__username=receiver)
    iter_num = 0
    senders = ''
    senders_comments = ''
    for i in this_result_comments:
        if i.sender.username == request.user.username:

            senders += str(i.sender.username) + '~'
        else:
            senders += str(i.sender.first_name) + ' ' + str(
                i.sender.last_name) + '~'

        senders_comments += str(i.comment_text) + '~'
    senders = senders[0:len(senders) - 1]
    senders_comments = senders_comments[0:len(senders_comments) - 1]

    resp = senders + '`' + senders_comments

    return HttpResponse(resp)
