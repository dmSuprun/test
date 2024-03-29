from django import template
from tests.models import TestsSection

register = template.Library()


@register.simple_tag()
def get_num_section_in_test(test_slug):
    return len(TestsSection.objects.filter(test__slug=test_slug))


@register.simple_tag()
def cut_type_value_from_difficult_data_type(type_val):
    if type_val.count('(') == 0:
        return type_val

    new_type = ''
    for i in type_val:
        if i != '(':
            new_type += i
        else:
            break
    return new_type


def cut_items_type(type_val):
    if type_val.count('(') == 0:
        return type_val
    return type_val[(type_val.index('(') + 1):type_val.index(')')]


@register.inclusion_tag('designer/options.html')
def show_options(this_argument_num, all_arguments):
    types = ('str', 'int', 'float', 'bool', 'list', 'tuple', 'set',
             'frozenset', 'dict')
    get_this_arg_val = all_arguments[this_argument_num]

    return {'types': types, 'this_arg': get_this_arg_val}


@register.inclusion_tag('designer/items.html')
def show_item(this_argument_num, all_arguments, isOutput):
    types = ('str', 'int', 'float', 'bool')
    get_this_arg_val = all_arguments[this_argument_num]

    if cut_type_value_from_difficult_data_type(
            get_this_arg_val
    ) == 'list' or cut_type_value_from_difficult_data_type(
            get_this_arg_val
    ) == 'tuple' or cut_type_value_from_difficult_data_type(
            get_this_arg_val
    ) == 'set' or cut_type_value_from_difficult_data_type(
            get_this_arg_val) == 'frozenset':
        this_item_type = cut_items_type(get_this_arg_val)
        item_name = ''
        if isOutput == 'True':
            item_name = 'outputlistItem'
        else:
            item_name = 'listItem'

        return {
            'types': types,
            'this_item': this_item_type,
            'exist': True,
            'arg_num': this_argument_num,
            'isDict': False,
            'item_name': item_name
        }
    elif cut_type_value_from_difficult_data_type(get_this_arg_val) == 'dict':
        this_item_dict_key = cut_items_type(get_this_arg_val)[:(
            cut_items_type(get_this_arg_val).index(':'))]
        this_item_dict_val = cut_items_type(get_this_arg_val)[(
            cut_items_type(get_this_arg_val).index(':') +
            1):len(cut_items_type(get_this_arg_val))]
        dict_item = ''
        if isOutput == 'True':
            dict_item = "dictOutputKey"
        else:
            dict_item = "dictKey"

        dict_val = ''
        if isOutput == 'True':
            dict_val = "dictOutputValue"
        else:
            dict_val = "dictValue"
        
        return {
            'types': types,
            'this_key': this_item_dict_key,
            'this_val': this_item_dict_val,
            'exist': True,
            'arg_num': this_argument_num,
            'isDict': True,
            'dict_item': dict_item,
            'dict_val': dict_val
        }
    return {'exist': False}


@register.inclusion_tag('designer/float_info.html')
def check_float_type(this_argument_num, all_arguments):
    get_this_arg_val = all_arguments[this_argument_num]
    first_part_of_type = cut_type_value_from_difficult_data_type(
        get_this_arg_val)

    if first_part_of_type == 'float':
        return {
            'exist':
            True,
            'error':
            'Використання типу float призводить до неточності результатів тестування!',
        }

    elif first_part_of_type == 'list' or first_part_of_type == 'tuple' or first_part_of_type == 'set' or first_part_of_type == 'frozenset':

        second_part_of_type = cut_items_type(get_this_arg_val)

        if second_part_of_type == 'float':

            return {
                'exist':
                True,
                'error':
                'Використання типу float призводить до неточності результатів тестування!'
            }

        else:
            return {'exist': False}
    elif first_part_of_type == 'dict':
        key_type = cut_items_type(get_this_arg_val)[:(
            cut_items_type(get_this_arg_val).index(':'))]
        value_type = cut_items_type(get_this_arg_val)[(
            cut_items_type(get_this_arg_val).index(':') +
            1):len(cut_items_type(get_this_arg_val))]
        if key_type or value_type:
            return {
                'exist':
                True,
                'error':
                'Використання типу float призводить до неточності результатів тестування!'
            }

    else:
        return {'exist': False}


@register.inclusion_tag('designer/float_info.html')
def check_list(this_argument_num, all_arguments):
    get_this_arg_val = all_arguments[this_argument_num]
    first_part_of_type = cut_type_value_from_difficult_data_type(
        get_this_arg_val)

    if first_part_of_type == 'list' or first_part_of_type == 'tuple' or first_part_of_type == 'set' or first_part_of_type == 'frozenset':
        return {
            'exist':
            True,
            'error':
            'Елементи списку, під час введення вводяться  через крапку з комою! (item1;item2;item3...)',
        }

    elif first_part_of_type == 'dict':
        return {
            'exist':
            True,
            'error':
            'Елементи словника, під час введення вводяться парами, пари розділяються крапкою з комою! (key1:value1;key2:value2....)',
        }

    else:
        return {'exist': False}
