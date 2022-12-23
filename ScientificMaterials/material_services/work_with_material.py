from django.http import Http404
from course.models import CourseConfig
from ScientificMaterials.material_services.crud import *
from Users.models import TeacherInCourse

def get_material_data_json(material_obj):
    return material_obj.material

def get_material_key_words(material_obj):
    return material_obj.key_words


def check_error(get_param):
    errors = False
    already_assign_material = ''
    if get_param.get('error') == 'true':
        errors = True
        already_assign_material = get_param.get('material_name')
    return (errors, already_assign_material)


def get_all_teachers_email_in_course(course_s):
    get_course_obj = get_object_or_404(CourseConfig, course_slug=course_s)
    get_teachers_who_registered_on_this_course = TeacherInCourse.objects.filter(course=get_course_obj)
    return [i.e_mail for i in get_teachers_who_registered_on_this_course]

def get_all_available_materials_on_this_course(course_s):
    MATERIALS = []
    tmp_materials = []
    all_teachers_email_on_this_course = get_all_teachers_email_in_course(course_s)
    for teacher_email in all_teachers_email_on_this_course:
        tmp_materials.append(read_materials(author__email=teacher_email))

    for material in tmp_materials:
        for j in material:
            MATERIALS.append(j)


    return MATERIALS



