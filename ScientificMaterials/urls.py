from django.urls import path
from .views import *

urlpatterns = [
    path('show_material/<str:material_id>/',show_detail_materials, name='detail_material'),
    path('select_assign/', show_all_materials_for_assign, name='assign_material'),

]