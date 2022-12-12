from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index_page'),
    path('about/', about_page, name='about'),
    path('tips/', tips_page, name='tips'),
    path('faq/', faq_page, name='faq'),


]