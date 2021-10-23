from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Student,Mentor,PlacementOfficer,Company,User
from django.db import transaction
from django.forms.utils import ValidationError

class StudentSignUpForm(UserCreationForm):
    mobile_no=forms.IntegerField(max_value=9999999999,min_value=1111111111)
    password2=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('first_name','last_name', 'username', 'email', 'password1' ,'password2', 'mobile_no')
        #label={'email':'Email addr'}

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.user_type=1
        user.save()
        student = Student.objects.create(user=user,enrollment_no=self.cleaned_data['username'],Email=self.cleaned_data['email'],Mobile_No=self.cleaned_data['mobile_no'],)
        #student.Email=*self.cleaned_data.get('email')
        return user

class CompanySignUpForm(UserCreationForm):
    mobile_no=forms.IntegerField(max_value=9999999999,min_value=1111111111)
    password2=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ( 'username', 'email', 'password1' ,'password2', 'mobile_no')
        #label={'email':'Email addr'}

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.user_type=3
        user.save()
        comp = Company.objects.create(user=user,name=self.cleaned_data['first_name'],Email=self.cleaned_data['email'],Mobile_No=self.cleaned_data['mobile_no'],)
        #student.Email=*self.cleaned_data.get('email')
        return user 
