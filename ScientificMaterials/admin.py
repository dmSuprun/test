from django.contrib import admin
from .models import *


class ScientificMaterialsConfigAdmin(admin.ModelAdmin):

    list_display = ('material_name', 'key_words', 'author')


admin.site.register(ScientificMaterials, ScientificMaterialsConfigAdmin)
