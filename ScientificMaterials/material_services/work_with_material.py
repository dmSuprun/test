from ScientificMaterials.material_services.crud import *

def get_material_data_json(material_obj):
    return material_obj.material

def get_material_key_words(material_obj):
    return material_obj.key_words
