from django import template
from course.models import AssignedTest
from course.models import AssignedMaterial



register = template.Library()


def check_assign_test_type(assign_obj):
    tests= AssignedTest.objects.all()
    if assign_obj in tests:
        return True
    return False


def check_assign_material_type(assign_obj):
    materials = AssignedMaterial.objects.all()
    if assign_obj in materials:
        return True
    return False

@register.inclusion_tag('course/test_in_course.html')
def render_test(type,assign_test_obj,this_teacher_assign_test,student_completed_tests,course_slug):
    return {
        'type':type,
        'assign_test_obj':assign_test_obj,
        'this_teacher_assign_test':this_teacher_assign_test,
        'student_completed_tests':student_completed_tests,
        'course_slug':course_slug
    }


@register.inclusion_tag('course/material_in_course.html')
def render_material(type, assign_material_obj):
    return {
        'type':type,
        'assign_material_obj':assign_material_obj
    }