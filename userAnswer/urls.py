from .views import *
from django.urls import path

urlpatterns = [
    path('<slug:course>/<slug:test>/complete', check_result, name='check')
]