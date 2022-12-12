from django.urls import path
from .views import *

urlpatterns = [
    path('<slug:course_slug>/<slug:test_slug>/start/', start_test, name='starttest')

]