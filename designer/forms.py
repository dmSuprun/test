from django.forms import ModelForm
from designer.utils import transliteration
from course.models import CourseConfig
from django.core.exceptions import ValidationError

from tests.models import TestsConfig, TestsSection, DataForTestingCode
from django import forms

class TestCreateForm(forms.Form):
    name_test = forms.CharField(label="Назва тесту", max_length=255, widget=forms.TextInput(
            attrs={'class': 'form-control shadow-lg p-3 mb-5 bg-white mt-3 rounded ', }))
    theme_test = forms.CharField(label='Опис тесту', max_length=255, widget=forms.TextInput(
            attrs={'class': 'form-control shadow-lg p-3 mb-5 mt-3 bg-white rounded ', }))
    max_test_result=forms.IntegerField(label='Максимальний бал',  widget=forms.NumberInput(
            attrs={'class': 'form-control shadow-lg p-3 mb-5 mt-3 bg-white rounded ', 'min':'0.1', 'step':'0.1'}))
    create_func_template = forms.BooleanField(label='Автоматичне створення шаблону функції', required=False, widget=forms.CheckboxInput(
        attrs={'class': 'form-check-input'}
    ))

    def clean_name_test(self):
        get_name=self.cleaned_data['name_test']
        get_this_name_slug=transliteration(get_name)

        if len(TestsConfig.objects.filter(slug=get_this_name_slug)) !=0:
            raise ValidationError('Такий тест вже існує!')
        return get_name

    def clean_max_test_result(self):
        get_result=self.cleaned_data['max_test_result']


        if get_result <= 0:
            raise ValidationError('Бал повинен бути більше за нуль!')
        return get_result




class CreateTest(ModelForm):
    class Meta:
        model=TestsConfig
        fields='__all__'


class TaskCreationForm(forms.Form):
    function = forms.CharField(label='Назва функції', max_length=255,widget=forms.TextInput(attrs={ 'class':'form-control shadow-lg p-3 mb-5 bg-white mt-3 rounded '}))

    question =forms.CharField(label='Питання',widget=forms.Textarea(attrs={ 'class':'form-control shadow-lg p-3 mb-5 bg-white mt-3 rounded ','cols':20, 'rows':10}))

    def clean_function(self):
        function_name = self.cleaned_data['function']
        ValidSymb = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'a', 'A', 'b', 'B', 'c', 'C', 'd', 'D', 'e', 'E',
                     'f', 'F', 'g', 'G', 'h', 'H', 'i', 'I', 'j', 'J', 'k', 'K', 'L', 'l', 'm', 'M', 'N', 'n', 'o', 'O',
                     'p', 'P', 'q', 'Q', 'r', 'R', 's', 'S', 't', 'T', 'U', 'u', 'v', 'V', 'w', 'W', 'x', 'X', 'y', 'Y',
                     'z', 'Z', '_']
        for sym in function_name:
            if not(sym in ValidSymb):
                raise ValidationError(f'Функція має не коректний({sym}) символ!')
            continue
        return function_name

class CreateTaskInModelForm(ModelForm):
    class Meta:
        model=TestsSection
        fields='__all__'


class DataForTestingCodeForm(ModelForm):
    class Meta:
        model=DataForTestingCode
        fields='__all__'

























# class CreateTask(ModelForm):
#     class Meta:
#         model=TestsSection
#         fields='__all__'
#
# class CreateDataForTestForm(ModelForm):
#     class Meta:
#         model=DataForTestingCode
#         fields = '__all__'



