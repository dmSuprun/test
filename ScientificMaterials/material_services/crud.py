from django.shortcuts import get_object_or_404
from ScientificMaterials.models import ScientificMaterials


def read_only_one_material(**params):
    return get_object_or_404(ScientificMaterials, **params)

def read_materials(**params):
    return ScientificMaterials.objects.filter(**params)


