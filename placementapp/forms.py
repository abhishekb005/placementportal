from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db.models import fields
#from django.forms import fields
#from django.forms import ModelForm
from .models import *
from django.forms import BaseModelFormSet
#from .models import Student,Mentor,PlacementOfficer,Company,User
from django.db import transaction
from django.forms.utils import ValidationError
from datetime import datetime

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

class PlacementOfficerSignUpForm(UserCreationForm):
    mobile_no=forms.IntegerField(max_value=9999999999,min_value=1111111111)
    password2=forms.CharField(widget=forms.PasswordInput)
    #PlacementCell=forms.ChoiceField(required=True,)
    class Meta:
        model = User
        fields = ( 'username', 'email', 'password1' ,'password2', 'mobile_no',)
        #label={'email':'Email addr'}

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.user_type=2
        user.verified=True
        user.save()
        pc=PlacementCell.objects.get(pk=1)
        mentorr = PlacementOfficer.objects.create(user=user,placementCell=pc,first_name=self.cleaned_data['first_name'],Email=self.cleaned_data['email'],Mobile_No=self.cleaned_data['mobile_no'],)
        #student.Email=*self.cleaned_data.get('email')
        return user 
        
class MentorSignUpForm(UserCreationForm):
    mobile_no=forms.IntegerField(max_value=9999999999,min_value=1111111111)
    password2=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ( 'username', 'email', 'password1' ,'password2', 'mobile_no')
        #label={'email':'Email addr'}

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.user_type=4
        user.verified=True
        user.save()
        mentorr = Mentor.objects.create(user=user,first_name=self.cleaned_data['first_name'],Email=self.cleaned_data['email'],Mobile_No=self.cleaned_data['mobile_no'],)
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

class Export(forms.Form):
    mobileno=forms.BooleanField()
    
class SchoolForm(forms.ModelForm):
    class Meta:
        model=School
        fields='__all__'

# Update Student Details based on Model
class StudentForm(forms.ModelForm):
    class Meta:
        model=Student
        fields='__all__'
        exclude = ['user','enrollment_no','AppliedPositions','PlacementCell','mentor','School10','School12','ResumeURL']

class AppliedForm(forms.ModelForm):
    #Student=forms.ModelChoiceField(disabled=True)
    class Meta:
        model=Applied
        fields=["Student","Position","Status","Description","FinalOffer"]

class CustomModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, branch):
        """ Customises the labels for checkboxes"""
        return "%s" % branch.Branch_Name

class PositionForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        """ Grants access to the request object so that only members of the current user
        are given as options"""
        #self.request = kwargs.pop('request')
        
        super(PositionForm, self).__init__(*args, **kwargs)
        self.fields['branch'].queryset = BranchDS.objects.all()
        
    class Meta:
        model=Position
        fields=('minCTC','maxCTC','Description','branch','minScore10','minScore12','minJeePercentile')
    branch = forms.ModelMultipleChoiceField(
        queryset=Branch.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

class StudentStatus(forms.ModelForm):
    class Meta:
        model=Applied
        fields=['Status','FinalOffer']

class OfferForm(forms.ModelForm):
    def __init__(self,user,*args, **kwargs):
        """ Grants access to the request object so that only members of the current user
        are given as options"""
        #self.request = kwargs.pop('request')
        
        super(OfferForm, self).__init__(*args, **kwargs)
        self.fields['Position'].queryset = Position.objects.filter(Company__user=user)
    
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

class AppliedForm(forms.ModelForm):
    class Meta:
        model=Applied
        fields="__all__"

# class MyAppliedForm(AppliedForm):
#     def __init__(self, *args, user, **kwargs):
#          self.user = user
#          super().__init__(*args, **kwargs)

# class BaseAppliedFormSet(BaseModelFormSet):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.queryset = Applied.objects.filter(Status='Selected')
class StudentVerifyForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','verified']
    username=forms.CharField(disabled=True,)

class UpdateAppliedStuStatusForm(forms.ModelForm):
    class Meta:
        model=Applied
        fields=["Student","Position","Status"]

class CompanyForm(forms.ModelForm):
    class Meta:
        model=Company
        fields='__all__'

# class Export(forms.Form):
#     enrollment_no=forms.BooleanField(required=False)
#     first_name=forms.BooleanField(required=False)
#     last_name=forms.BooleanField(required=False)
#     gender=forms.BooleanField(required=False)
#     Email=forms.BooleanField(required=False)
#     Mobile_No=forms.BooleanField(required=False)
#     School10=forms.BooleanField(required=False)
#     School12=forms.BooleanField(required=False)
#     Score10=forms.BooleanField(required=False)
#     Score12=forms.BooleanField(required=False)
#     JeePercentile=forms.BooleanField(required=False)
#     Branch=forms.BooleanField(required=False)
#forms.py
class StudentdataExportbyplacementofficer(forms.Form):
    enrollment_no=forms.BooleanField(required=False)
    first_name=forms.BooleanField(required=False)
    last_name=forms.BooleanField(required=False)
    gender=forms.BooleanField(required=False)
    Email=forms.BooleanField(required=False)
    Mobile_No=forms.BooleanField(required=False)
    Score10=forms.BooleanField(required=False)
    Score12=forms.BooleanField(required=False)
    JeePercentile=forms.BooleanField(required=False)
    Branch=forms.BooleanField(required=False)
    #mentor=forms.BooleanField(required=False)
    PlacementCell=forms.BooleanField(required=False)
    #AppliedPositions=models.ManyToManyField(to=Position,through='Applied')
    branchlist=forms.ModelMultipleChoiceField(queryset=BranchDS.objects.all())

class PositionExportplacementofficer(forms.Form):
    Company=models.ForeignKey(to=Company,on_delete=models.CASCADE)
    minCTC=forms.BooleanField(required=False)
    maxCTC=forms.BooleanField(required=False)
    Description=forms.BooleanField(required=False)
    #branch=models.ManyToManyField(to=BranchDS,)
    minScore10=forms.BooleanField(required=False)
    minScore12=forms.BooleanField(required=False)
    minJeePercentile=forms.BooleanField(required=False)

class CompanyExportplacementofficer(forms.Form):    
    Name=forms.BooleanField(required=False)
    Description=forms.BooleanField(required=False)
    MCA=forms.BooleanField(required=False)
    Type=forms.BooleanField(required=False)
    revenue=forms.BooleanField(required=False)

class AppliedExportplacementofficer(forms.Form):
    Student=forms.BooleanField(required=False)
    Position=forms.BooleanField(required=False)
    Status=forms.BooleanField(required=False)
    Time=forms.BooleanField(required=False)
    Description=forms.BooleanField(required=False)
    FinalOffer=forms.BooleanField(required=False)
    Companies=forms.ModelMultipleChoiceField(queryset=Company.objects.all())
    Till=forms.DateTimeField(initial=datetime.now)

class OffersExportplacementofficer(forms.Form):
    Position=forms.BooleanField(required=False)
    Description=forms.BooleanField(required=False)
    FinalCTC=forms.BooleanField(required=False)

class MentorExportplacementofficer(forms.Form):
    first_name=forms.BooleanField(required=False)
    last_name=forms.BooleanField(required=False)
    gender=forms.BooleanField(required=False)
    Email=forms.BooleanField(required=False)
    Mobile_No=forms.BooleanField(required=False)

class StudentdataExportbycompany(forms.Form):
    enrollment_no=forms.BooleanField(required=False)
    first_name=forms.BooleanField(required=False)
    last_name=forms.BooleanField(required=False)
    gender=forms.BooleanField(required=False)
    Email=forms.BooleanField(required=False)
    Mobile_No=forms.BooleanField(required=False)
    Score10=forms.BooleanField(required=False)
    Score12=forms.BooleanField(required=False)
    JeePercentile=forms.BooleanField(required=False)
    Branch=forms.BooleanField(required=False)
    #mentor=forms.BooleanField(required=False)
    PlacementCell=forms.BooleanField(required=False)
    #AppliedPositions=models.ManyToManyField(to=Position,through='Applied')
   
class AppliedExportcompany(forms.Form):
    Student=forms.BooleanField(required=False)
    Position=forms.BooleanField(required=False)
    Status=forms.BooleanField(required=False)
    Description=forms.BooleanField(required=False)
    FinalOffer=forms.BooleanField(required=False)

class StudentdataExportbymentor(forms.Form):
    enrollment_no=forms.BooleanField(required=False)
    first_name=forms.BooleanField(required=False)
    last_name=forms.BooleanField(required=False)
    gender=forms.BooleanField(required=False)
    Email=forms.BooleanField(required=False)
    Mobile_No=forms.BooleanField(required=False)
    School10=forms.BooleanField(required=False)
    School12=forms.BooleanField(required=False)
    Score10=forms.BooleanField(required=False)
    Score12=forms.BooleanField(required=False)
    JeePercentile=forms.BooleanField(required=False)
    Branch=forms.BooleanField(required=False)
    Aim=forms.BooleanField(required=False)
    Objective=forms.BooleanField(required=False)
    Mission=forms.BooleanField(required=False)
    Vision=forms.BooleanField(required=False)
    #mentor=forms.BooleanField(required=False)
    PlacementCell=forms.BooleanField(required=False)
    #AppliedPositions=models.ManyToManyField(to=Position,through='Applied')

class AppliedExportmentor(forms.Form):
    Student=forms.BooleanField(required=False)
    Position=forms.BooleanField(required=False)
    Status=forms.BooleanField(required=False)
    Description=forms.BooleanField(required=False)
    FinalOffer=forms.BooleanField(required=False)