from django import forms
from django.forms import ModelForm
from .models import UserAnswer,UserWhoСompletedTest,CheckinResult
from tests.models import TestsConfig
from django.core.exceptions import ValidationError




class UserAnswerTextForm(forms.Form):
    answer=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control shadow-lg p-3 mb-5 bg-white rounded', }), label='Відповідь')
    def clean_answer(self):
        get_string_answer = self.cleaned_data['answer']
        safe_list = ['datetime','math','random','string']
        num_imports = get_string_answer.count('import')
        if num_imports == 0:
            return get_string_answer
        else:
            num_of_included_safe_moduls = 0
            for safe_el in safe_list:
                if safe_el in get_string_answer:
                    num_of_included_safe_moduls+=1
            if num_of_included_safe_moduls == num_imports:
                return get_string_answer

            raise ValidationError('Не всі модулі дозволено імпортувати!')












class UserAnswerForm(ModelForm):
    class Meta:
        model=UserAnswer
        fields='__all__'
    def clean(self):
        data = self.cleaned_data
        try:
            obj = UserAnswer.objects.get(user=data['user'], test=data['test'],course=data['course'],test_section=data['test_section'])
            existence = True
        except Exception:
            existence = False
        if existence:
            raise ValidationError('Відповідь існує')

        return data


class UserWhoCompleteForm(ModelForm):
    class Meta:
        model=UserWhoСompletedTest
        fields='__all__'

    def clean(self):
        data=self.cleaned_data

        try:
            obj = UserWhoСompletedTest.objects.get(user=data['user'], test=data['test'],course=data['course'])
            existence = True
        except Exception:
            existence = False
        if existence:
            raise ValidationError('Запис уже існує')
        return data



class CheckinResultForm(ModelForm):
    class Meta:
        model=CheckinResult
        fields='__all__'

    def clean(self):
        data = self.cleaned_data

        get_save_results = CheckinResult.objects.filter(answer=data['answer'], data_on_which_they_checked=data['data_on_which_they_checked'])
        if len(get_save_results) !=0:
            raise ValidationError('Запис вже існує')
        return data


