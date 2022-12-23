from django.forms import ModelForm, TextInput, JSONField
from django.core.exceptions import ValidationError
from course.models import AssignedMaterial
from django import forms
from .models import *


class createMaterialText(forms.Form):
    material_name = forms.CharField(label="Тема матеріалу", max_length=255,widget=forms.TextInput(
            attrs={'class': 'form-control shadow-lg p-3 mb-5 bg-white mt-3 rounded ', }))
    key_words = forms.CharField(label="Ключові слова", max_length=255,widget=forms.TextInput(
            attrs={'class': 'form-control shadow-lg p-3 mb-5 bg-white mt-3 rounded ', }))
    material = forms.CharField(label="Матеріал", widget=forms.Textarea(
            attrs={'class': 'form-control shadow-lg p-3 mb-5 bg-white mt-3 rounded ', }))



class createMaterialForm(ModelForm):
    class Meta:
        model=ScientificMaterials
        fields='__all__'


class AssignMaterialForm(ModelForm):
    class Meta:
        model=AssignedMaterial
        fields='__all__'

    def clean(self):
        data = self.cleaned_data
        if len(AssignedMaterial.objects.filter(course=data['course'], test=data['test'], material=data['material'])) >= 1:

            raise ValidationError('Вже призначено')



