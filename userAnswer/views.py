from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from course.models import CourseConfig
from tests.models import TestsConfig, DataForTestingCode
from .forms import UserWhoCompleteForm, CheckinResultForm
from .models import UserAnswer, CheckinResult
from django.contrib.auth.decorators import login_required
from staticPages.views import get_role
from multiprocessing import Process
import time
from datetime import datetime

def check_timeout():
    start = datetime.now()
    while (datetime.now() - start).seconds < 5:
        time.sleep(1)
    return False


def check_logic(answer, data_for_check, func_name):
    '''this  function get a three parameters: code, that need a checking, name function in this code
                and data for testing this code( can be a one model-obj or many model-obj)'''
    globals_and_locals_for_exec_func = {
        'open': None,
        'print': None,
        'settings': None
    }
    input_arguments = {}
    input_arguments_types = {}
    output_arguments = {}
    output_arguments_types = {}
    RESULTS = {}

    for data_obj in data_for_check:
        input_arguments[data_obj] = data_obj.input_test_data
        input_arguments_types[data_obj] = data_obj.input_test_data_type
        output_arguments[data_obj] = data_obj.output_test_data
        output_arguments_types[data_obj] = data_obj.output_test_data_type

    for one_data_obj in data_for_check:
        ''' input data block'''
        input_args_for_this_data_obj = input_arguments[one_data_obj]
        input_args_type_for_this_data_obj = input_arguments_types[one_data_obj]
        input_args_type_for_this_data_obj += ','
        input_args = input_args_for_this_data_obj.split(',')

        argument_num = 0
        ABSOLUTE_RESULT = ''
        arguments_type = []
        one_type = ''
        for el in input_args_type_for_this_data_obj:
            if el != ',':
                one_type += el
            else:
                arguments_type.append(one_type)
                one_type = ''
                argument_num += 1

        argument_index = -1
        for one_type_val in arguments_type:
            argument_index += 1
            if one_type_val == 'str' or one_type_val == 'int' or one_type_val == 'float' or one_type_val == 'bool':
                tmp_val = one_type_val
                tmp_val += '('

                tmp_val += str(input_args[argument_index])
                tmp_val += '),'

                ABSOLUTE_RESULT += tmp_val
            elif 'tuple' in one_type_val or 'list' in one_type_val or 'set' in one_type_val or 'frozenset' in one_type_val:
                elements_type_in_list = one_type_val[one_type_val.index('(') +
                                                     1:one_type_val.index(')')]

                input_data = str(input_args[argument_index]) + ';'

                stack_with_items = []
                item = ""
                for data in input_data:

                    if data == ';':

                        stack_with_items.append(item)
                        item = ""

                    else:
                        item += data

                if 'list' in one_type_val:
                    list_result = '['

                elif 'tuple' in one_type_val:
                    list_result = '('
                else:
                    list_result = '{'
                itr_item = -1
                for item in stack_with_items:
                    itr_item += 1
                    if len(stack_with_items) - 1 == itr_item:

                        list_result += elements_type_in_list + '(' + item + ')'
                    else:
                        list_result += elements_type_in_list + '(' + item + '),'
                if 'list' in one_type_val:
                    list_result += '],'
                elif 'tuple' in one_type_val:
                    list_result += '),'
                else:
                    list_result += '},'
                ABSOLUTE_RESULT += list_result

            else:
                dict_types = one_type_val[one_type_val.index('(') +
                                          1:one_type_val.index(')')]
                TYPE_FOR_KEY = dict_types[:dict_types.index(':')] + '('
                TYPE_FOR_VAL = dict_types[dict_types.index(':') +
                                          1:len(dict_types)] + '('

                data_values = str(
                    input_args[arguments_type.index(one_type_val)])
                stack_with_key = []
                stack_with_val = []
                input_val = ''
                for el in (data_values + ';'):
                    if el == ';':
                        stack_with_val.append(input_val)
                        input_val = ''
                    elif el != ':':
                        input_val += el
                    else:
                        stack_with_key.append(input_val)
                        input_val = ''
                dicts_items = '{'
                for one_el in stack_with_key:
                    dict_key_val = TYPE_FOR_KEY + one_el + ')'
                    dict_value_value = TYPE_FOR_VAL + stack_with_val[
                        stack_with_key.index(one_el)] + ')'
                    if stack_with_key.index(one_el) == (len(stack_with_key) -
                                                        1):

                        dicts_items += dict_key_val + ':' + dict_value_value
                    else:
                        dicts_items += dict_key_val + ':' + dict_value_value + ','

                dicts_items += '},'

                ABSOLUTE_RESULT += dicts_items
        # end inputs
        ''' output data block'''

        output_args_for_this_data_obj = output_arguments[one_data_obj]
        output_args_type_for_this_data_obj = output_arguments_types[
            one_data_obj]
        output_args_type_for_this_data_obj += ','
        output_args = output_args_for_this_data_obj.split(',')

        argument_out_num = 0
        ABSOLUTE_OUT_RESULT = ''
        out_arguments_type = []
        one_out_type = ''
        for el in output_args_type_for_this_data_obj:

            if el != ',':
                one_out_type += el

            else:
                out_arguments_type.append(one_out_type)
                one_out_type = ''
                argument_out_num += 1

        argument_index = -1
        for one_type_val in out_arguments_type:
            argument_index += 1

            if one_type_val == 'str' or one_type_val == 'int' or one_type_val == 'float' or one_type_val == 'bool':
                tmp_val = one_type_val
                tmp_val += '('
                tmp_val += str(output_args[argument_index])

                tmp_val += '),'

                ABSOLUTE_OUT_RESULT += tmp_val
            elif 'tuple' in one_type_val or 'list' in one_type_val or 'set' in one_type_val or 'frozenset' in one_type_val:
                elements_type_in_list = one_type_val[one_type_val.index('(') +
                                                     1:one_type_val.index(')')]
                out_data = str(output_args[argument_index]) + ';'

                stack_with_items = []
                item = ''
                for data in out_data:
                    if data == ';':
                        stack_with_items.append(item)
                        item = ''
                    else:
                        item += data
                if 'list' in one_type_val:
                    list_result = '['

                elif 'tuple' in one_type_val:
                    list_result = '('
                else:
                    list_result = '{'
                  

                itr_item_out = -1
                for item in stack_with_items:
                    itr_item_out += 1
                    if len(stack_with_items) - 1 == itr_item_out:

                        list_result += elements_type_in_list + '(' + item + ')'
                    else:
                        list_result += elements_type_in_list + '(' + item + '),'
                if 'list' in one_type_val:
                    list_result += '],'
                elif 'tuple' in one_type_val:
                    list_result += '),'
                else:
                    list_result += '},'

                ABSOLUTE_OUT_RESULT += list_result

            else:
                dict_types = one_type_val[one_type_val.index('(') +
                                          1:one_type_val.index(')')]
                TYPE_FOR_KEY = dict_types[:dict_types.index(':')] + '('
                TYPE_FOR_VAL = dict_types[dict_types.index(':') +
                                          1:len(dict_types)] + '('

                data_values = str(
                    output_args[out_arguments_type.index(one_type_val)])
                stack_with_key = []
                stack_with_val = []
                out_val = ''
                for el in (data_values + ';'):
                    if el == ';':
                        stack_with_val.append(out_val)
                        out_val = ''
                    elif el != ':':
                        out_val += el
                    else:
                        stack_with_key.append(out_val)
                        out_val = ''
                dicts_items = '{'
                for one_el in stack_with_key:
                    dict_key_val = TYPE_FOR_KEY + one_el + ')'
                    dict_value_value = TYPE_FOR_VAL + stack_with_val[
                        stack_with_key.index(one_el)] + ')'
                    if stack_with_key.index(one_el) == (len(stack_with_key) -
                                                        1):

                        dicts_items += dict_key_val + ':' + dict_value_value
                    else:
                        dicts_items += dict_key_val + ':' + dict_value_value + ','

                dicts_items += '},'

                ABSOLUTE_OUT_RESULT += dicts_items
        INPUT_VAL = ''
        for i in range(len(ABSOLUTE_RESULT) - 1):
            INPUT_VAL += ABSOLUTE_RESULT[i]

        OUTPUT_VAL = ''
        for i in range(len(ABSOLUTE_OUT_RESULT) - 1):
            OUTPUT_VAL += ABSOLUTE_OUT_RESULT[i]

        additional_string = f'\ntry:\n      recode_user_actual_result={func_name}({INPUT_VAL})\nexcept Exception:\n      recode_user_actual_result="Помилка виконання"\nif {func_name}({INPUT_VAL}) != ({OUTPUT_VAL}):\n      raise AssertionError("Fail")'
        mod = f'\nfrom threading import Thread\n'
        check_time = f'\nth = Thread(target={func_name}, args=[{INPUT_VAL}])\nth.start()\nth.join(timeout=10)\nif th.is_alive():\n      raise AssertionError("Fail")'

        result_answer =mod+ answer+check_time+ additional_string


        

        try:
            exec(result_answer, globals_and_locals_for_exec_func, globals_and_locals_for_exec_func)

            try:
                actual_user_result = globals_and_locals_for_exec_func[
                    'recode_user_actual_result']
            except Exception:
                actual_user_result = 'Помилка виконання'

            RESULTS[one_data_obj] = (True, actual_user_result)

        except Exception:
            ''' fail '''
            try:
                actual_user_result = globals_and_locals_for_exec_func[
                    'recode_user_actual_result']
            except Exception:
                actual_user_result = 'Помилка виконання'
            RESULTS[one_data_obj] = (False, actual_user_result)

    return RESULTS


@login_required
def check_result(request, course, test):
    this_course = get_object_or_404(CourseConfig, course_slug=course)
    this_test = get_object_or_404(TestsConfig, slug=test)
    ''' check user answer with model data'''
    all_user_answer_on_this_test = UserAnswer.objects.filter(
        user=request.user, test=this_test, course=this_course)
    all_data_for_testing_code_obj_in_this_test = []

    for user_answer in all_user_answer_on_this_test:
        function = user_answer.test_section.function_name
        get_data_for_testing_on_this__test_section = DataForTestingCode.objects.filter(
            section=user_answer.test_section)
        all_data_for_testing_code_obj_in_this_test.append(
            get_data_for_testing_on_this__test_section)
        try:
            checker = check_logic(user_answer.answer,
                                  get_data_for_testing_on_this__test_section,
                                  function)
        except Exception:
            return HttpResponse(
                "<h1 style='text-align:center;position:relative; top:10%;'>Виникла помилка при перевірці (неправильно сформовані тесткейси)! Зв'яжіться з викладачем!</h1>"
            )

        for data, test_res in checker.items():
            data_for_checkin_result_form = {
                'answer': user_answer,
                'data_on_which_they_checked': data,
                'user': request.user,
                'course': this_course,
                'test': this_test,
                'testing_result': test_res[0],
                'actual_user_result': test_res[1]
            }
            tmp_form = CheckinResultForm(data_for_checkin_result_form)
            if tmp_form.is_valid():
                tmp_form.save()
    ''' get all information about user results in  this test '''
    all_num_of_point = this_test.max_test_result
    user_point_num = 0
    user_test_point_num = 0
    all_test_point = 0

    all_checkin_result = CheckinResult.objects.filter(user=request.user,
                                                      course=this_course,
                                                      test=this_test)
    for res_item in all_checkin_result:
        all_test_point += res_item.data_on_which_they_checked.num_of_point
        if res_item.testing_result:
            user_test_point_num += res_item.data_on_which_they_checked.num_of_point

        else:
            continue
    try:
        user_point_num = round(
            (all_num_of_point * user_test_point_num) / all_test_point, 1)
        success_percent = int(
            round(user_point_num / all_num_of_point, 2) * 100)

    except ZeroDivisionError:
        success_percent = 0
    type_of_res = success_percent / 10
    if type_of_res <= 4:
        css_class_on_percent = 1
    elif type_of_res >= 5 and type_of_res < 8:
        css_class_on_percent = 2
    else:
        css_class_on_percent = 3
    ''' complete test model '''
    complete_test_form_data = {
        'user': request.user,
        'course': this_course,
        'test': this_test,
        'total_num_of_points': all_num_of_point,
        'user_point': user_point_num,
        'success_percent': success_percent,
    }
    complete_test_form = UserWhoCompleteForm(complete_test_form_data)
    if complete_test_form.is_valid():
        complete_test_form.save()

    context = {
        'all_point_num': all_num_of_point,
        'user_point_num': user_point_num,
        'success_percent': success_percent,
        'css_selector': css_class_on_percent,
        'type': get_role(request),
        'title': f'Результати тесту {this_test.name_test}'
    }
    return render(request, 'userAnswer/user_results.html', context=context)
