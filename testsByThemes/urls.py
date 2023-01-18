from django.urls import path
from .views import *

urlpatterns = [
    path('all_tests/', show_all_auto_created_tests, name='all_auto_created_tests')



]

