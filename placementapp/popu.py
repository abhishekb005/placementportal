import os
import random
#os.environ.setdefault('DJANGO_SETTINGS_MODULE','fbvplacementportal.settings')
#import django
#django.setup()

from placementapp.models import *
from faker import Faker
from random import *

faker=Faker()
boards=['CBSE','ICSE','MP BOARD']
def populate(n):
    for i in range(n):
        #user class
        fuser_type = FAKE.random_int(1,5)
        fverified =Fake.random.choice([True,False])
        
        #school class
        fschoolName=Fake.name()
        fLocation_Name=Fake.city()
        fBoard=random.choice(boards)
        
        #dgree class
        fDegree_Name=Fake.name()
        fDegree_Duration=Fake.random_digit()
        fTotal_Sem=Fake.random_digit()
        fMin_credit=Fake.random_int(100, 200)
        
    #     #branch class
    #     fBranch_Name=Fake.word()
    #     fStart_year=Fake.year()
        
    #     #staff class
    #     fstafffirst_name=Fake.first_name()
#     fstafflast_name=Fake.last_name()
    #     fstaffgender=random.choice(['M','F','O'])
    #     fstaffEmail=Fake.email()
    #     fstaffMobile_No=Fake.phone_number()
       
    #    #placment cell class
    #     funiversityname=Fake.name()
    #     funiversityphone_no=Fake.phone_number()
    #     funiversityemail=Fake.email()
        
    #     #comapany class
    #     fcompanyName=Fake.name()
    #     fcompanyDescription=Fake.text()
    #     fMCA=Fake.random_int()
    #     fcompanyType=Fake.word()
    #     frevenue=Fake.random_int()
        
    #     #position class
    #     fminCTC=Fake.random_int(100000, 200000)
    #     fmaxCTC=Fake.random_int(200000, 1000000)
    #     fpositionDescription=Fake.text()
    #     fpositionminScore10=Fake.random_int(0, 100)
    #     fpositionminScore12=Fake.random_int(0, 100)
    #     fpositionminJeePercentile=Fake.random_int(0, 100)
         
    #     #student class
    #     fstudentenrollment_no=Fake.random_int()
    #     fstudentfirst_name=Fake.first_name()
    #     fstudentlast_name=Fake.last_name()
    #     fstudentgender=random.choice(['M','F','O'])
    #     fstudentEmail=Fake.email()
    #     fstudentMobile_No=Fake.phone_number()
    #     fstudentminScore10=Fake.random_int(0, 100)
    #     fstudentminScore12=Fake.random_int(0, 100)
    #     fstudentminJeePercentile=Fake.random_int(0, 100)
    #     fAim=Fake.text()
    #     fObjective=Fake.text()
    #     fMission=Fake.text()
    #     fVision=Fake.text()
    #     fverified=random.choice([0,1])
    #     fAppliedPositions=Fake.words()
        
    #     #message class
    #     fTimeStamps=Fake.date_time_this_century()
    #     fBody=Fake.text()
        
    #     #messagep2s class
    #     ftype=Fake.word()
        
    #     #offers class
    #     fDescription=Fake.text()
    #     fFinalCTC=Fake.random_int(200000, 1000000)
         
    #     #applied class
    #     fStatus=random.choice(['S','ENR','R','UE'])
    #     fTime=Fake.date_time()
    #     fappliedDescription=Fake.text()
        
        user_record=User.objects.get_or_create(user_type =fuser_type,verified=fverified)
        school_record=School.objects.get_or_create(Name=fschoolName,Location_Name=fLocation_Name,Board=fBoard)
        degree_record=Degree.objects.get_or_create(Degree_Name=fDegree_Name,Degree_Duration=fDegree_Duration,Total_Sem=fTotal_Sem,Min_credit=fMin_credit)
        # branch_record=Branch.objects.get_or_create(Branch_Name=fBranch_Name,Start_year=fStart_year)
        # placmentcell_record=PlacementCell.objects.get_or_create(University=funiversityname,phone_no=funiversityphone_no,email=funiversityemail)
        # company_record=Company.objects.get_or_create(Name=fcompanyName,Description=fcompanyDescription,MCA=fMCA,Type=fcompanyType,revenue=frevenue)
        # position_record=Position.objects.get_or_create(minCTC=fminCTC,maxCTC=fmaxCTC,Description=fpositionDescription,minScore10=fpositionminScore10,minScore12=fpositionminScore12,minJeePercentile=fstudentminJeePercentile)
        # student_record=Student.objects.get_or_create(enrollment_no=fstudentenrollment_no,first_name=fstudentfirst_name,last_name=fstudentlast_name,gender=fstudentgender,Email=fstudentEmail,Score10=fstudentminScore10,Score12=fstudentminScore12,JeePercentile=fstudentminJeePercentile,Branch=fstudent,Aim=fAim,Objective=fObjective,Mission=fMission,Vision=fVision)
        # message_record=Message.objects.get_or_create(Body=fBody)
        # messagep2s_recordschool_record=MessageP2S.objects.get_or_create(type=ftype)
        # offers_record=Offers.objects.get_or_create(Description=fDescription,FinalCTC=fFinalCTC)
        # applied_record=Applied.objects.get_or_create(Status=fStatus,Description=fappliedDescription)
#populate(10)