from django.urls import path
from .views import *

urlpatterns = [
    path('show_material/<str:material_id>/',show_detail_materials, name='detail_material'),
    path('select_assign/<slug:test_slug>/<slug:course_slug>/', show_all_materials_for_assign, name='all_material_for_assign'),
    path('assign/<str:material_id>/<slug:test_slug>/<slug:course_slug>/', assign_material, name='assign_material'),
    path('delete_assign/<str:material_id>/<slug:test_slug>/<slug:course_slug>/', delete_assign_material, name='delete_assign_material'),

]