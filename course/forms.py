from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from designer.utils import transliteration

from Users.models import *
from django.core.validators import FileExtensionValidator



class CreateUserForm(forms.Form):
    csv_file_with_emails=forms.FileField(label='Файл з списком електронних адрес',validators =[FileExtensionValidator(allowed_extensions=['csv','CSV'], message='Файл повинен бути розширенняя .csv')])

class getEmail(forms.Form):
    email = forms.EmailField(label='E-mail',max_length=255,widget=forms.TextInput(attrs={'class':'form-control shadow-lg p-3 mb-5 mt-3 bg-white rounded detail_input_label' }))



class StudentInCourseForm(ModelForm):

    class Meta:
        model = StudentInCourse
        fields = ['e_mail','course']

    def clean(self):
        try:
            this_e_mail = self.cleaned_data['e_mail']
        except KeyError:
            raise ValidationError('Пошта записана некоректно!')

        this_course=self.cleaned_data['course']
        students_obj=StudentInCourse.objects.filter(e_mail=this_e_mail, course=this_course)
        if len(students_obj)!=0:
            raise ValidationError('Така електронна адреса вже існує на цьому курсі')
        elif len(TeacherInCourse.objects.filter(e_mail=this_e_mail))!=0:
            raise ValidationError('Така електронна адреса вже має роль')





class TeacherInCourseForm(ModelForm):
    class Meta:
        model = TeacherInCourse
        fields = ['e_mail','course']
    def clean(self):
        try:

            this_e_mail = self.cleaned_data['e_mail']
        except KeyError:
            raise ValidationError('Пошта записана некоректно!')

        this_course = self.cleaned_data['course']
        students_obj = TeacherInCourse.objects.filter(e_mail=this_e_mail, course=this_course)
        if len(students_obj) != 0:
            raise ValidationError('Така електронна адреса вже існує на цьому курсі')
        elif len(StudentInCourse.objects.filter(e_mail=this_e_mail)) != 0:
            raise ValidationError('Така електронна адреса вже має роль')



class CreateCourseForm(ModelForm):
    class Meta:
        model = CourseConfig
        fields = '__all__'




class CreateCourseTextForm(forms.Form):
    name = forms.CharField(label="Ім'я курсу",max_length=255,widget=forms.TextInput(attrs={'class':'form-control shadow-lg p-3 mb-5 bg-white mt-3 rounded min-wigth_for_label detail_input_label', }))
    subject = forms.CharField(label='Предмет курсу',max_length=255,widget=forms.TextInput(attrs={'class':'form-control shadow-lg p-3 mb-5 mt-3 bg-white rounded detail_input_label', }))
    teacher_email = forms.EmailField(required=False,label='E-mail викладача',max_length=255,widget=forms.TextInput(attrs={'class':'form-control shadow-lg p-3 mb-5 mt-3 bg-white rounded detail_input_label','placeholder':'Залиште пустим, якщо Ви будете викладачем на цьому курсі' }))
    def clean_name(self):
        data = self.cleaned_data
        get_name = data['name']
        get_slug = transliteration(get_name)
        if len(CourseConfig.objects.filter(course_slug=get_slug)) != 0:
            raise ValidationError('Такий курс вже існує')

        else:
            return data['name']

    def clean_teacher_email(self):
        this_e_mail = self.cleaned_data['teacher_email']
        if len(StudentInCourse.objects.filter(e_mail=this_e_mail)) != 0:
            raise ValidationError('Така електронна адреса вже має роль')

        elif this_e_mail.count(',') != 0 or this_e_mail.count('@') != 1:
            raise ValidationError('Адреса має бути одна!')

        else:
            if this_e_mail == '':
                return this_e_mail
            elif not('@' in this_e_mail):
                raise ValidationError('Адреса записана не коректно!')
            return this_e_mail






class AssignTestForm(ModelForm):
    class Meta:
        model = AssignedTest
        fields = '__all__'

    def clean(self):
        course = self.cleaned_data['course']
        test = self.cleaned_data['test']
        tmp_qrst = AssignedTest.objects.filter(course=course,test=test)
        if len(tmp_qrst) !=0:
            raise ValidationError('Вже призначено!')
        return self.cleaned_data



