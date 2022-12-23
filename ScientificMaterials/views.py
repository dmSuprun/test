from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from course.models import CourseConfig
from tests.models import TestsConfig
from ScientificMaterials.forms import AssignMaterialForm
from ScientificMaterials.material_services.crud import *
from ScientificMaterials.material_services.work_with_material import *
from staticPages.views import get_role

@login_required
def show_detail_materials(request, material_id):
    this_material = read_only_one_material(material_uuid=material_id)
    get_material_data=get_material_data_json(this_material)
    get_key_words = get_material_key_words(this_material)

    context={
        'type':get_role(request),
        'title':this_material.material_name,
        'material_data':get_material_data,
        'key_words':get_key_words
    }

    return render(request, 'ScientificMaterials/detail_material.html', context=context)

@login_required
def show_all_materials_for_assign(request,test_slug, course_slug):
    if get_role(request) != 'teacher':
        return HttpResponse('<h1 style="text-align:center;position:relative; top:10%;">Доступ заборонено!</h1>', status=403)
    materials = get_all_available_materials_on_this_course(course_slug)
    check_assign_error = check_error(request.GET)

    context={
        'title':'Призначити матеріал',
        'type':get_role(request),
        'materials':materials,
        'test_slug':test_slug,
        'course_slug':course_slug,
        'errors':check_assign_error[0],
        'already_assign_material':check_assign_error[1]
    }
    return render(request, 'ScientificMaterials/all_materials_for_assign.html', context=context)

@login_required
def assign_material(request,material_id,test_slug,course_slug):
    if get_role(request) != 'teacher':
        return HttpResponse('<h1 style="text-align:center;position:relative; top:10%;">Доступ заборонено!</h1>',
                            status=403)
    this_course=get_object_or_404(CourseConfig,course_slug=course_slug)
    this_test = get_object_or_404(TestsConfig,slug=test_slug)
    this_material = read_only_one_material(material_uuid=material_id)
    adding_result = create_assign_material_object(course=this_course, test=this_test, material=this_material)
    if adding_result:
        return redirect(reverse('detail_course', kwargs={'course_slug':course_slug}))
    else:
        return redirect(f'/materials/select_assign/{test_slug}/{course_slug}/?error=true&material_name={this_material.material_name}')


@login_required
def delete_assign_material(request,material_id,test_slug,course_slug):
    if get_role(request) != 'teacher':
        return HttpResponse('<h1 style="text-align:center;position:relative; top:10%;">Доступ заборонено!</h1>',
                            status=403)
    check_delete_status = delete_assign(material_id,test_slug,course_slug)
    return redirect(reverse('detail_course', kwargs={'course_slug':course_slug}))







