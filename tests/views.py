from userAnswer.models import UserWhoСompletedTest
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from staticPages.views import get_role
from .models import *
from userAnswer.forms import *
from course.models import CourseConfig
from userAnswer.models import UserWhoСompletedTest
from django.contrib.auth.decorators import login_required


@login_required
def start_test(request,course_slug,test_slug):
    ''' get this course and this test, tasks for this test'''
    this_request_course = get_object_or_404(CourseConfig, course_slug=course_slug)
    this_request_test = get_object_or_404(TestsConfig, slug=test_slug)
    tasks_for_this_test = TestsSection.objects.filter(test = this_request_test)
    task_len = len(tasks_for_this_test)
    ''' create pagination logic '''
    this_request_page_num = request.GET.get('page')
    paginator = Paginator(tasks_for_this_test,1)
    page = paginator.get_page(this_request_page_num)
    ''' select a this page on another color'''
    '''test logic'''
    check_complete_for_this_user = UserWhoСompletedTest.objects.filter(user = request.user, course= this_request_course, test = this_request_test)

    ''' get test section on this page obj'''
    section_obj = paginator.get_page(page.number)
    test__section = None
    for i in section_obj:
        test__section = i

    if len(check_complete_for_this_user) == 0:
        ''' логіка першого проходження '''

        ''' get section who have answer'''

        all_answers = UserAnswer.objects.filter(user=request.user, test=this_request_test, course=this_request_course)
        section_and_she_answer = {}
        completed_pages=[]
        for answer in all_answers:
            section_and_she_answer[answer.test_section]=answer.answer
        for i in page.paginator.page_range:
            tmp_objs = paginator.get_page(i)
            for obj in tmp_objs:
                if obj in section_and_she_answer.keys():
                    completed_pages.append(i)


        page_and_answer={}
        ''' form logic '''
        if request.method == 'POST':
            form = UserAnswerTextForm(request.POST)
            if form.is_valid():

                answer_for_this_task = form.cleaned_data['answer']

                data_for_form = {
                    'user': request.user,
                    'test': this_request_test,
                    'course': this_request_course,
                    'test_section': test__section,
                    'answer': answer_for_this_task
                }

                add_result_form = UserAnswerForm(data_for_form)
                if add_result_form.is_valid():
                    add_result_form.save()
                else:
                    upd_obj = UserAnswer.objects.get(user=request.user, test=this_request_test,
                                                     course=this_request_course, test_section=test__section)
                    upd_obj.answer = answer_for_this_task
                    upd_obj.save()
        else:
            if test__section in section_and_she_answer.keys():
                data_get = {'answer': section_and_she_answer[test__section]}
                form = UserAnswerTextForm(data_get)
            else:
                form = UserAnswerTextForm()

        end_test = False
        if len(UserAnswer.objects.filter(user=request.user, test=this_request_test, course=this_request_course)) == len(tasks_for_this_test):
            end_test = True
        context = {
            'this_page':page,
            'task_len':task_len,
            'completed_pages':completed_pages,
            'end_test':end_test,
            'form':form,
            'title':f'{this_request_test.name_test}',
            'course':this_request_course.course_slug,
            'test':this_request_test.slug,
            'type':get_role(request)


        }
        return render(request, 'tests/start_test.html', context=context)



    elif len(check_complete_for_this_user) !=0:

            ''' заборона проходження'''
            user_result_on_this_test = UserWhoСompletedTest.objects.filter(course=this_request_course,test=this_request_test, user=request.user)

            context={
                'course':this_request_course.course_slug,
                'type_of_error':'Всі спроби на проходження тесту використано!',
                'this_test':this_request_test,
                'title':f'{this_request_test.name_test}',
                'results_qrst':user_result_on_this_test,
                'type': get_role(request)

            }
            return render(request, 'tests/error_test.html', context=context)





