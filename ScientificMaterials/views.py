from django.http import HttpResponse
from django.shortcuts import render
from ScientificMaterials.material_services.crud import *
from ScientificMaterials.material_services.work_with_material import *
from staticPages.views import get_role


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

def show_all_materials_for_assign(request):
    if get_role(request) != 'teacher':
        return HttpResponse('<h1 style="text-align:center;position:relative; top:10%;">Доступ заборонено!</h1>', status=403)

    get_this_teacher_all_materials = read_materials(author=request.user)

    context={
        'title':'Призначити матеріал',
        'type':get_role(request),
        'materials':get_this_teacher_all_materials
    }
    return render(request, 'ScientificMaterials/all_materials_for_assign.html', context=context)
