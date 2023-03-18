import json
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from course.models import CourseConfig
from course.forms import CreateCourseTextForm, CreateCourseForm, TeacherInCourseForm
from staticPages.views import get_role
from .utils import transliteration
from .forms import TestCreateForm, CreateTest, TaskCreationForm, CreateTaskInModelForm
from tests.models import TestsSection, TestsConfig, DataForTestingCode
from django.urls import reverse, reverse_lazy
from .forms import DataForTestingCodeForm
from ScientificMaterials.forms import createMaterialForm, createMaterialText
from ScientificMaterials.material_services.crud import read_materials, read_only_one_material


def union_types(list_tmp, key_list, input_field):
    print(list_tmp)

    my_list = list_tmp.getlist(key_list)
    print(my_list)

    result_input_types = ''
    iteration = 0
    for arg in my_list:
        iteration += 1
        if arg == 'tuple' or arg == 'list' or arg == 'set' or arg == 'frozenset':

            result_input_types += arg
            result_input_types += '('
            if input_field:
                tmp = 'listItem' + str(iteration)
            else:
                tmp = 'outputlistItem' + str(iteration)

            add_list = list_tmp.getlist(tmp)

            result_input_types += add_list[0]

            result_input_types += '),'

        elif arg == 'dict':

            result_input_types += arg
            result_input_types += '('

            if input_field:
                tmp_k = 'dictKey_' + str(iteration)
                tmp_v = 'dictValue_' + str(iteration)
            else:
                tmp_k = 'dictOutputKey_' + str(iteration)
                tmp_v = 'dictOutputValue_' + str(iteration)

            add_list = list_tmp.getlist(tmp_k)
            print(add_list)
            result_input_types += add_list[0]

            add_list = list_tmp.getlist(tmp_v)
            result_input_types += ':'
            result_input_types += add_list[0]
            result_input_types += '),'
        else:
            result_input_types += arg
            result_input_types += ','

    result_input_types = result_input_types[:-1]
    return result_input_types


def _check_testcase_existence_for_some_test(test_slug):
    this_test = TestsConfig.objects.get(slug=test_slug)
    all_task_for_this_test = TestsSection.objects.filter(test=this_test)

    for task in all_task_for_this_test:
        if len(DataForTestingCode.objects.filter(section=task)) != 0:
            continue
        else:
            return False
    return True


@login_required
def designer(request):
    if get_role(request) != 'teacher':
        return HttpResponse(
            '<h1 style="text-align:center;position:relative; top:10%;">Доступ заборонено!</h1>',
            status=403)
    context = {'type': get_role(request), 'title': 'Конструктор'}
    return render(request, 'designer/designer.html', context=context)


@login_required
def create_test(request):
    if get_role(request) != 'teacher':
        return HttpResponse(
            '<h1 style="text-align:center;position:relative; top:10%;">Доступ заборонено!</h1>',
            status=403)
    if request.method == 'POST':
        form = TestCreateForm(request.POST)
        if form.is_valid():
            user_email = str(request.user.email)
            position_of_symb = user_email.index('@')

            new_username = ''
            for i in range(position_of_symb):
                if user_email[i] == '.':
                    new_username += '-'
                    continue
                new_username += user_email[i]
            new_slug = transliteration(
                form.cleaned_data['name_test']) + '-vid-' + new_username
            create_test_data = {
                'name_test': form.cleaned_data['name_test'],
                'slug': new_slug,
                'theme_test': form.cleaned_data['theme_test'],
                'author_of_test': request.user,
                'max_test_result': form.cleaned_data['max_test_result'],
                'create_func_template':
                form.cleaned_data['create_func_template'],
                'autocomplete': form.cleaned_data['autocomplete'],
                'pre_end_check': form.cleaned_data['pre_end_check']
            }

            new_test_form = CreateTest(create_test_data)
            if new_test_form.is_valid():
                new_test_form.save()

                return redirect(f'/create/{create_test_data["slug"]}/task/')
            else:
                form.add_error(
                    'name_test',
                    ValidationError('Тест з такою назвою вже існує!'))

    else:
        form = TestCreateForm()
    context = {
        'type': get_role(request),
        'title': 'Конструктор тесту',
        'form': form
    }
    return render(request, 'designer/test_designer.html', context=context)


@login_required
def update_test(request, test_slug):
    if get_role(request) != 'teacher':
        return HttpResponse(
            '<h1 style="text-align:center;position:relative; top:10%;">Доступ заборонено!</h1>',
            status=403)
    get_test = get_object_or_404(TestsConfig, slug=test_slug)
    if request.method == 'POST':
        form = TestCreateForm(request.POST)
        if form.is_valid():

            get_test.name_test = form.cleaned_data['name_test']
            get_test.slug = transliteration(form.cleaned_data['name_test'])
            get_test.theme_test = form.cleaned_data['theme_test']
            get_test.max_test_result = form.cleaned_data['max_test_result']
            get_test.create_func_template = form.cleaned_data[
                'create_func_template']
            get_test.autocomplete = form.cleaned_data['autocomplete']
            get_test.pre_end_check = form.cleaned_data['pre_end_check']
            get_test.save()
            return redirect(
                reverse('create_task', kwargs={'test_slug': get_test.slug}))
    else:
        data_for_form = {
            'name_test': get_test.name_test,
            'theme_test': get_test.theme_test,
            'max_test_result': get_test.max_test_result,
            'create_func_template': get_test.create_func_template,
            'autocomplete': get_test.autocomplete,
            'pre_end_check': get_test.pre_end_check
        }
        form = TestCreateForm(data_for_form)

    context = {
        'type': get_role(request),
        'title': 'Редакція тесту',
        'form': form,
        'test': get_test
    }
    return render(request, 'designer/test_update.html', context=context)


@login_required
def delete_test(request, test_slug):
    if get_role(request) != 'teacher':
        return HttpResponse(
            '<h1 style="text-align:center;position:relative; top:10%;">Доступ заборонено!</h1>',
            status=403)
    this_test = get_object_or_404(TestsConfig, slug=test_slug)
    this_test.delete()
    return redirect(reverse('create_test'))


@login_required
def create_course(request):
    if get_role(request) != 'teacher':
        return HttpResponse(
            '<h1 style="text-align:center;position:relative; top:10%;">Доступ заборонено!</h1>',
            status=403)
    if request.method == 'POST':
        form = CreateCourseTextForm(request.POST)

        if form.is_valid():
            new_data = {}
            data_for_register = {}
            for k, v in form.cleaned_data.items():
                if k == 'teacher_email':
                    data_for_register[k] = v
                    continue
                new_data[k] = v

            slug_with_namespace = transliteration(new_data['name'])
            if data_for_register['teacher_email'] == '':
                username_email = ''
                email_user = str(request.user.email)
                position_symb = email_user.index('@')
                for i in range(position_symb):
                    if email_user[i] == '.':
                        username_email += '-'
                        continue

                    username_email += email_user[i]

                slug_with_namespace += '-vid-' + username_email
            else:
                username_from_email = ''
                email = str(data_for_register['teacher_email'])
                position = email.index('@')
                for i in range(position):
                    if email[i] == '.':
                        username_from_email += '-'
                        continue

                    username_from_email += email[i]
                slug_with_namespace += '-vid-' + username_from_email

            new_data['course_slug'] = slug_with_namespace
            create_course = CreateCourseForm(new_data)
            if create_course.is_valid():
                create_course.save()
                get_course_obj = CourseConfig.objects.get(
                    course_slug=new_data['course_slug'])
                if data_for_register['teacher_email'] == '':
                    data_for_register['e_mail'] = request.user.email
                else:
                    data_for_register['e_mail'] = data_for_register[
                        'teacher_email']
                data_for_register['course'] = get_course_obj
                teacher_create_form = TeacherInCourseForm(data_for_register)
                if teacher_create_form.is_valid():
                    teacher_create_form.save()
                    if data_for_register['teacher_email'] == '':
                        return redirect(
                            f'/course/detail/{new_data["course_slug"]}/')

                    else:

                        return redirect(
                            f'/create/course/?status={True}&course={new_data["name"]}'
                        )
            else:
                form.add_error('name', 'Такий курс вже існує!')

    else:
        form = CreateCourseTextForm()

    context = {
        'form': form,
        'type': get_role(request),
        'title': 'Створити курс',
        'status': request.GET.get('status'),
        'new_course_name': request.GET.get('course')
    }
    return render(request, 'designer/course_designer.html', context=context)


@login_required
def update_task(request, test_slug, pk_this_task,
                num_task_in_designer_template):
    if get_role(request) != 'teacher':
        return HttpResponse(
            '<h1 style="text-align:center;position:relative; top:10%;">Доступ заборонено!</h1>',
            status=403)
    this_test = get_object_or_404(TestsConfig, slug=test_slug)
    this_task = get_object_or_404(TestsSection,
                                  pk=pk_this_task,
                                  test=this_test)
    if request.method == 'POST':
        form = TaskCreationForm(request.POST)
        if form.is_valid():
            this_task.function_name = form.cleaned_data['function']
            this_task.question = form.cleaned_data['question']
            this_task.save()

            return redirect(
                reverse('create_task', kwargs={'test_slug': this_test.slug}))

    else:
        data = {
            'function': this_task.function_name,
            'question': this_task.question
        }

        form = TaskCreationForm(data)
        data_for_testing_code_for_this_test = DataForTestingCode.objects.filter(
            section=this_task)
        all_testcases = {}
        iteration = 0
        for testcase in data_for_testing_code_for_this_test:
            iteration += 1
            all_testcases[iteration] = testcase

    context = {
        'task': this_task,
        'type': get_role(request),
        'form': form,
        'title': 'Редакція завдання',
        'test': this_test,
        'testcases': all_testcases.items(),
        'relatively_num': num_task_in_designer_template,
        'this_task_pk': pk_this_task
    }
    return render(request, 'designer/task_update.html', context=context)


@login_required
def update_testcase(request, testcase_pk, case_number_in_designer_template):

    if get_role(request) != 'teacher':
        return HttpResponse(
            '<h1 style="text-align:center;position:relative; top:10%;">Доступ заборонено!</h1>',
            status=403)
    get_this_testcase = get_object_or_404(DataForTestingCode, pk=testcase_pk)
    if request.method == 'POST':

        result_input_types = union_types(request.POST, 'argumentConfig', True)
        result_output_types = union_types(request.POST, 'outputConfig', False)

        count_testcase = len(request.POST.getlist('inp_value')) // len(
            request.POST.getlist('argumentConfig'))
        count_argument = len(request.POST.getlist('argumentConfig'))
        inp_values = request.POST.getlist('inp_value')
        output_values = request.POST.getlist('out_value')
        prices = request.POST.getlist('price')

        for testcaseNumber in range(count_testcase):
            index_from = testcaseNumber * count_argument
            index_to = (index_from + count_argument)
            get_this_testcase.input_test_data = ','.join(
                inp_values[index_from:index_to])
            get_this_testcase.input_test_data_type = result_input_types
            get_this_testcase.output_test_data = output_values[testcaseNumber]
            get_this_testcase.output_test_data_type = result_output_types
            get_this_testcase.num_of_point = prices[testcaseNumber]

            get_this_testcase.save()
            return redirect(
                reverse(
                    'create_task',
                    kwargs={'test_slug': get_this_testcase.section.test.slug}))

    # get input types
    all_inp_types_in_this_testcase = []
    tmp_type = ''
    for type_sym in (get_this_testcase.input_test_data_type + ','):
        if type_sym != ',':
            tmp_type += type_sym
        else:
            all_inp_types_in_this_testcase.append(tmp_type)
            tmp_type = ''
    argument_types_and_he_num = {}
    iter_num = 0
    for arg in all_inp_types_in_this_testcase:
        iter_num += 1
        argument_types_and_he_num[iter_num] = arg

    # get output types

    all_out_types_in_this_testcase = []
    tmp_out_type = ''
    for type_sym in (get_this_testcase.output_test_data_type + ','):
        if type_sym != ',':
            tmp_type += type_sym
        else:
            all_out_types_in_this_testcase.append(tmp_type)
            tmp_type = ''
    output_argument_types_and_he_num = {}
    iter_num = 0
    for arg in all_out_types_in_this_testcase:

        iter_num += 1
        output_argument_types_and_he_num[iter_num] = arg

    # get input values

    all_input_values_in_this_testcase = []
    tmp_value = ''
    for val_sym in (get_this_testcase.input_test_data + ','):
        if val_sym != ',':
            tmp_value += val_sym
        else:
            all_input_values_in_this_testcase.append(tmp_value)
            tmp_value = ''

    input_values_and_he_num = {}
    iter_num = 0
    for value in all_input_values_in_this_testcase:
        iter_num += 1
        input_values_and_he_num[iter_num] = value

    # get output values

    all_output_values_in_this_testcase = []
    tmp_value = ''
    for val_sym in (get_this_testcase.output_test_data + ','):
        if val_sym != ',':
            tmp_value += val_sym
        else:
            all_output_values_in_this_testcase.append(tmp_value)
            tmp_value = ''

    output_values_and_he_num = {}
    iter_num = 0
    for value in all_output_values_in_this_testcase:
        iter_num += 1
        output_values_and_he_num[iter_num] = value

    context = {
        'type':
        get_role(request),
        'testcase_num':
        case_number_in_designer_template,
        'title':
        f'Оновити тесткейс №{case_number_in_designer_template}',
        'testcase_pk':
        testcase_pk,
        'count_input_arg':
        range(1,
              len(all_inp_types_in_this_testcase) + 1, 1),
        'count_arg':
        len(all_inp_types_in_this_testcase),
        'arguments':
        argument_types_and_he_num,
        'generate_out_arg':
        range(1,
              len(all_out_types_in_this_testcase) + 1, 1),
        'count_output':
        len(all_out_types_in_this_testcase),
        'outputs':
        output_argument_types_and_he_num,
        'generate_input_values':
        range(1,
              len(all_input_values_in_this_testcase) + 1, 1),
        'input_values':
        input_values_and_he_num,
        'generate_output_values':
        range(1,
              len(all_output_values_in_this_testcase) + 1, 1),
        'output_values':
        output_values_and_he_num,
        'testcase_price':
        int(get_this_testcase.num_of_point)
    }

    return render(request, 'designer/update_testcase.html', context=context)


@login_required
def create_testcase_to_task(request, task_pk):
    if get_role(request) != 'teacher':
        return HttpResponse(
            '<h1 style="text-align:center;position:relative; top:10%;">Доступ заборонено!</h1>',
            status=403)

    if request.method == 'POST':
        result_input_types = union_types(request.POST, 'argumentConfig', True)
        result_output_types = union_types(request.POST, 'outputConfig', False)

        count_testcase = len(request.POST.getlist('inp_value')) // len(
            request.POST.getlist('argumentConfig'))
        count_argument = len(request.POST.getlist('argumentConfig'))
        inp_values = request.POST.getlist('inp_value')
        output_values = request.POST.getlist('out_value')
        prices = request.POST.getlist('price')
        this_test_section = get_object_or_404(TestsSection, pk=task_pk)

        for testcaseNumber in range(count_testcase):
            index_from = testcaseNumber * count_argument
            index_to = (index_from + count_argument)
            form_context = {
                'section': this_test_section,
                'input_test_data': ','.join(inp_values[index_from:index_to]),
                'input_test_data_type': result_input_types,
                'output_test_data': output_values[testcaseNumber],
                'output_test_data_type': result_output_types,
                'num_of_point': prices[testcaseNumber]
            }
            add_task_form = DataForTestingCodeForm(form_context)
            if add_task_form.is_valid():
                add_task_form.save()

    context = {'type': get_role(request), 'title': 'Нові тесткейси'}
    return render(request, 'designer/create_testcase.html', context=context)


def delete_testcase_from_task(request, testcase_pk):
    if get_role(request) != 'teacher':
        return HttpResponse(
            '<h1 style="text-align:center;position:relative; top:10%;">Доступ заборонено!</h1>',
            status=403)
    testcase = get_object_or_404(DataForTestingCode, pk=testcase_pk)
    test_slug = testcase.section.test.slug
    testcase.delete()
    return redirect(reverse('create_task', kwargs={'test_slug': test_slug}))


@login_required
def delete_task(request, test_slug, pk_this_task):
    if get_role(request) != 'teacher':
        return HttpResponse(
            '<h1 style="text-align:center;position:relative; top:10%;">Доступ заборонено!</h1>',
            status=403)
    get_test = get_object_or_404(TestsConfig, slug=test_slug)
    get_task = get_object_or_404(TestsSection, pk=pk_this_task,
                                 test=get_test).delete()
    return redirect(f'/create/{get_test.slug}/task/')


@login_required
def create_tasks_to_test(request, test_slug):
    if get_role(request) != 'teacher':
        return HttpResponse(
            '<h1 style="text-align:center;position:relative; top:10%;">Доступ заборонено!</h1>',
            status=403)
    get_this_test = get_object_or_404(TestsConfig, slug=test_slug)
    get_this_test_section = TestsSection.objects.filter(test=get_this_test)

    if request.method == 'POST':

        form_who_create_task = TaskCreationForm(request.POST)
        if form_who_create_task.is_valid():
            data_for_model_form = {
                'test': get_this_test,
                'function_name': form_who_create_task.cleaned_data['function'],
                'question': form_who_create_task.cleaned_data['question']
            }

            model_form = CreateTaskInModelForm(data_for_model_form)
            if model_form.is_valid():
                model_form.save()

                result_input_types = union_types(request.POST,
                                                 'argumentConfig', True)
                result_output_types = union_types(request.POST, 'outputConfig',
                                                  False)

                count_testcase = len(request.POST.getlist('inp_value')) // len(
                    request.POST.getlist('argumentConfig'))
                count_argument = len(request.POST.getlist('argumentConfig'))
                inp_values = request.POST.getlist('inp_value')
                output_values = request.POST.getlist('out_value')
                prices = request.POST.getlist('price')
                this_test_section = get_object_or_404(
                    TestsSection,
                    test=data_for_model_form['test'],
                    function_name=data_for_model_form['function_name'],
                    question=data_for_model_form['question'])

                for testcaseNumber in range(count_testcase):
                    index_from = testcaseNumber * count_argument
                    index_to = (index_from + count_argument)
                    form_context = {
                        'section':
                        this_test_section,
                        'input_test_data':
                        ','.join(inp_values[index_from:index_to]),
                        'input_test_data_type':
                        result_input_types,
                        'output_test_data':
                        output_values[testcaseNumber],
                        'output_test_data_type':
                        result_output_types,
                        'num_of_point':
                        prices[testcaseNumber]
                    }
                    add_task_form = DataForTestingCodeForm(form_context)
                    if add_task_form.is_valid():
                        add_task_form.save()

                return redirect(
                    reverse('create_task',
                            kwargs={'test_slug': get_this_test.slug}))

    else:
        form_who_create_task = TaskCreationForm()
    tasks_with_it_num = {}
    num = 0
    for task in get_this_test_section:
        num += 1
        tasks_with_it_num[task] = num

    context = {
        'type': get_role(request),
        'title': 'Конструктор завдань',
        'tasks': tasks_with_it_num.items(),
        'form': form_who_create_task,
        'test': get_this_test
    }
    return render(request, 'designer/task_designer.html', context=context)


@login_required
def create_materials(request):
    if get_role(request) != 'teacher':
        return HttpResponse(
            '<h1 style="text-align:center;position:relative; top:10%;">Доступ заборонено!</h1>',
            status=403)
    if request.method == 'POST':
        form = createMaterialText(request.POST)
        if form.is_valid():
            data_for_model_form = {
                'material_name': form.cleaned_data['material_name'],
                'key_words': form.cleaned_data['key_words'],
                'material': form.cleaned_data['material'],
                'author': request.user
            }
            model_form = createMaterialForm(data_for_model_form)
            if model_form.is_valid():
                model_form.save()
                return redirect(reverse('show_all_tests'))
    else:
        form = createMaterialText()

    context = {
        'type': get_role(request),
        'form': form,
        'title': 'Створити науковий матеріал'
    }
    return render(request, 'designer/create_material.html', context=context)


@login_required
def show_all_tests(request):
    if get_role(request) != 'teacher':
        return HttpResponse(
            '<h1 style="text-align:center;position:relative; top:10%;">Доступ заборонено!</h1>',
            status=403)
    get_my_tests = TestsConfig.objects.filter(
        author_of_test__username=request.user.username)
    get_materials = read_materials(author=request.user)
    context = {
        'type': get_role(request),
        'title': 'Мої розробки',
        'my_tests': get_my_tests,
        'count_test': len(get_my_tests),
        'count_material': len(get_materials),
        'materials': get_materials
    }
    return render(request,
                  'designer/show_all_tests_and_materials.html',
                  context=context)


def update_material(request, uuid_material):
    if get_role(request) != 'teacher':
        return HttpResponse(
            '<h1 style="text-align:center;position:relative; top:10%;">Доступ заборонено!</h1>',
            status=403)
    get_material = read_only_one_material(material_uuid=uuid_material)
    if request.method == 'POST':
        form = createMaterialText(request.POST)
        if form.is_valid():
            get_material.material_name = form.cleaned_data['material_name']
            get_material.key_words = form.cleaned_data['key_words']
            get_material.material = form.cleaned_data['material']
            get_material.save()
            return redirect(reverse('show_all_tests'))

    form = createMaterialText({
        'material_name': get_material.material_name,
        'key_words': get_material.key_words,
        'material': get_material.material
    })

    context = {
        'type': get_role(request),
        'material_data': get_material.material,
        'form': form
    }
    return render(request, 'designer/update_material.html', context=context)
