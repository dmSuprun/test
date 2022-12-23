from django.shortcuts import get_object_or_404, redirect,reverse

from ScientificMaterials.forms import AssignMaterialForm
from ScientificMaterials.models import ScientificMaterials
from course.models import AssignedMaterial


def read_only_one_material(**params):
    return get_object_or_404(ScientificMaterials, **params)

def read_materials(**params):
    return ScientificMaterials.objects.filter(**params)


def create_assign_material_object(**kwargs):
    form = AssignMaterialForm(kwargs)
    if form.is_valid():
        form.save()
        return True
    else:
        return False



def delete_assign(material_id,test_slug,course_slug):
    try:
        this_assign_material = get_object_or_404(AssignedMaterial, course__course_slug=course_slug, test__slug=test_slug,
                                                 material__material_uuid=material_id)
        this_assign_material.delete()
        return True
    except Exception:
        return False




