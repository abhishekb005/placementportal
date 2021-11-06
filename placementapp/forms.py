from django import forms
from django.contrib.auth.forms import UserCreationForm
#from django.forms import fields
#from django.forms import ModelForm
from .models import *

#from .models import Student,Mentor,PlacementOfficer,Company,User
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

class Schooldetails(forms.Form):
    SchoolName=forms.CharField(max_length=60,)
    Location_Name=forms.CharField(max_length=40,)
    Board=forms.CharField(max_length=50,)
    
class CollegeDetails(forms.Form):
    Degree_Name=forms.CharField(max_length=40)
    Degree_Duration=forms.IntegerField(min_value=2)
    Total_Sem=forms.IntegerField(min_value=1)
    Branch=forms.CharField(max_length=40)
    Current_Semester=forms.IntegerField(min_value=1,max_value=10)
    Current_Cgpa=forms.DecimalField(min_value=1,max_value=10,max_digits=3,decimal_places=2)
    Mentor_Name=forms.CharField(max_length=50)
    BackLog=forms.BooleanField()

class BackLogDetails(forms.Form):
    TotalBackLogs=forms.IntegerField(min_value=0)
    Subject_name=forms.CharField(max_length=50)
    CurrentBacklog=forms.BooleanField()
    CurrentBacklog_subjectname=forms.CharField(max_length=50)

class SchoolForm(forms.ModelForm):
    class Meta:
        model=School
        fields='__all__'

# Update Student Details based on Model
class StudentForm(forms.ModelForm):
    class Meta:
        model=Student
        fields='__all__'
        exclude = ['user','enrollment_no','AppliedPositions','PlacementCell','mentor','School10','School12']
    
class PositionForm(forms.ModelForm):
    class Meta:
        model=Position
        fields=('Company','minCTC','maxCTC','Description','branch','minScore10','minScore12','minJeePercentile')

class StudentStatus(forms.ModelForm):
    class Meta:
        model=Applied
        fields=['Status','FinalOffer']

class OfferForm(forms.ModelForm):
    class Meta:
        model=Offers
        fields='__all__'

class MessageC2P(forms.ModelForm):
    class Meta:
        model=MessageC2P
        fields='__all__'
class MessageP2C(forms.ModelForm):
    class Meta:
        model=MessageP2C
        fields='__all__'
class MessageP2S(forms.ModelForm):
    class Meta:
        model=MessageP2S
        fields='__all__'