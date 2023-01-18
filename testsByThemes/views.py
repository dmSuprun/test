from django.http import HttpResponse
from django.shortcuts import render
from staticPages.views import get_role


def show_all_auto_created_tests(request):
    if get_role(request) != 'teacher':
        return HttpResponse('<h1 style="text-align:center;position:relative; top:10%;">Доступ заборонено!</h1>',
                            status=403)

    context = {
        'type':get_role(request)
    }
    return render(request, 'testsByThemes/all_auto_created_tests.html', context=context)
