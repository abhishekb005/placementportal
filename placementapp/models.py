from django.db import models
from django.contrib.auth.models import AbstractUser

# Creating Diff User by inheriting AbstractUser  
class User(AbstractUser):
    USER_TYPE_CHOICES = (
    (1, 'student'),
    (2, 'placementOfficer'),
    (3, 'Company'),
    (4, 'Mentor'),
    (5, 'admin'),
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES,default=2)
    verified=models.BooleanField(default=False)

# Create your models here.
class School(models.Model):
    Name=models.CharField(max_length=60,)
    Location_Name=models.CharField(max_length=40,)
    Board=models.CharField(max_length=50,)

class Degree(models.Model):
    Degree_Name=models.CharField(max_length=40)
    Degree_Duration=models.DecimalField(max_digits=2,decimal_places=1)
    Total_Sem=models.PositiveIntegerField(null=True,blank=True)
    Min_credit=models.IntegerField(null=True,blank=True,)

    def __str__(self):
        return f"{self.Degree_Name}"

class Branch(models.Model):
    #Branch_Code=models.CharField()
    Branch_Name=models.CharField(max_length=40,)
    Degree=models.ManyToManyField(to=Degree)
    Start_year=models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.Branch_Name} {self.Degree} {self.Start_year}"

# Abstract Model i.e it wont be created in database Table
# Its Parent Class For Mentor and PlacementOfficer    
class Staff(models.Model):
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    Gender_Choices=[('M','MALE'),
    ('F','FEMALE'),
    ('O','OTHERS'),
    ]
    gender=models.CharField(choices=Gender_Choices,null=True,max_length=10,)
    Email=models.EmailField()
    Mobile_No=models.PositiveBigIntegerField(null=False,blank=False)

    class Meta:
        abstract=True
# Databse Will Be Created and its inheriting Staff 
class Mentor(Staff):
    user=models.OneToOneField(to=User,on_delete=models.CASCADE,primary_key=True)
    

class PlacementCell(models.Model):
    University=models.CharField(max_length=40,default='MediCaps University')
    phone_no=models.PositiveBigIntegerField(null=True,blank=True)
    email=models.EmailField()

class Company(models.Model):
    user=models.OneToOneField(to=User,on_delete=models.CASCADE,primary_key=True)
    Name=models.CharField(max_length=60)
    Description=models.TextField()
    MCA=models.CharField(verbose_name='MCA ID',max_length=50)
    Type=models.CharField(verbose_name='Company Type',max_length=70)
    revenue=models.BigIntegerField(verbose_name='Latest 1 year Revenue')

class Position(models.Model):
    Company=models.ForeignKey(to=Company,on_delete=models.CASCADE)
    minCTC=models.SmallIntegerField(verbose_name='Minimum CTC in Lakhs')
    maxCTC=models.SmallIntegerField(verbose_name='Maximum CTC in Lakhs')
    Description=models.TextField(verbose_name='Roles and Responsibility')
    branch=models.ManyToManyField(to=Branch,)
    minScore10=models.DecimalField(max_digits=4,decimal_places=2,default=0.00)
    minScore12=models.DecimalField(max_digits=4,decimal_places=2,default=0.00)
    minJeePercentile=models.DecimalField(max_digits=4,decimal_places=2,default=0.00)
    
class Student(models.Model):
    user=models.OneToOneField(to=User,on_delete=models.CASCADE,primary_key=True)
    enrollment_no=models.CharField(max_length=12)
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    Gender_Choices=[('M','MALE'),
    ('F','FEMALE'),
    ('O','OTHERS'),
    ]
    gender=models.CharField(choices=Gender_Choices,null=True,max_length=10,)
    Email=models.EmailField(null=False,blank=False)
    Mobile_No=models.PositiveBigIntegerField(null=False,blank=False)
    School10=models.ForeignKey(to=School,null=True,on_delete=models.SET_NULL,related_name='SchoolX')
    School12=models.ForeignKey(to=School,null=True,on_delete=models.SET_NULL,related_name='SchoolXII')
    Score10=models.DecimalField(max_digits=4,decimal_places=2,null=True,blank=True)
    Score12=models.DecimalField(max_digits=4,decimal_places=2,null=True,blank=True)
    JeePercentile=models.DecimalField(max_digits=4,decimal_places=2,null=True,blank=True)
    Branch=models.ForeignKey(to=Branch,on_delete=models.SET_NULL,null=True)
    Aim=models.TextField(null=True,blank=True,)
    Objective=models.TextField(null=True,blank=True,)
    Mission=models.TextField(null=True,blank=True,)
    Vision=models.TextField(null=True,blank=True,)
    mentor=models.ForeignKey(to=Mentor,on_delete=models.SET_NULL,null=True,blank=True)
    PlacementCell=models.ForeignKey(to=PlacementCell,null=True,blank=True,on_delete=models.SET_NULL)
    AppliedPositions=models.ManyToManyField(to=Position,through='Applied')

# Databse Will Be Created and its inheriting Staff
class PlacementOfficer(Staff):
    user=models.OneToOneField(to=User,on_delete=models.CASCADE,primary_key=True)
    placementCell=models.ForeignKey(to=PlacementCell,on_delete=models.CASCADE)
    
class Message(models.Model):
    TimeStamps=models.DateTimeField()
    Body=models.TextField(blank=False,null=False)
    class Meta:     
        abstract=True
    
class MessageP2S(Message):
    sender=models.ForeignKey(to=PlacementCell,on_delete=models.CASCADE)
    receivers=models.ManyToManyField(to=Student)
    type=models.CharField(max_length=40,null=True,blank=True)

class MessageP2C(Message):
    sender=models.ForeignKey(to=PlacementCell,on_delete=models.CASCADE)
    receivers=models.ManyToManyField(to=Company)

class MessageC2P(Message):
    sender=models.ForeignKey(to=Company,on_delete=models.CASCADE)
    receivers=models.ForeignKey(to=PlacementCell,on_delete=models.CASCADE)
    
class Offers(models.Model):
    Position=models.ForeignKey(to=Position,on_delete=models.CASCADE)
    Description=models.TextField(verbose_name='Extra Info About offer')
    FinalCTC=models.SmallIntegerField()
    #Student=models.ForeignKey(to=Student,on_delete=models.CASCADE)
    #appliedStu=models.ForeignKey(to=Applied,on_delete=models.CASCADE)

class Applied(models.Model):
    Status_Choices=[('S','Selected'),('ENR','EligibleForNextRound'),('R','Rejected'),('UE','UnderEvaluation'),]
    Student=models.ForeignKey(to=Student,on_delete=models.CASCADE)
    Position=models.ForeignKey(to=Position,on_delete=models.CASCADE)
    Status=models.CharField(max_length=30,choices=Status_Choices,default='UnderEvaluation')
    Time=models.DateTimeField(verbose_name='Next Round Exam Start Time',auto_now_add=True,)
    Description=models.TextField(verbose_name='Info About Next Roumd',null=True,blank=True)
    FinalOffer=models.ForeignKey(to=Offers,on_delete=models.SET_NULL,null=True)

