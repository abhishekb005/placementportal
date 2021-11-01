from django.core.management.base import BaseCommand
from faker import Faker
import random
from django.utils import timezone
import faker.providers
from placementapp.models import Branch, Offers, PlacementCell, User,School,Degree,Mentor,Company,Position,Student,MessageP2S,Message,MessageP2C,MessageC2P,Applied
class Command(BaseCommand):
    help="Command Info"
    def handle(self,*args,**kwargs):
        #fake=Faker()
        locale_list = ['en-US', 'en_IN', 'en_US']
        #Fake = Faker(locale_list)
        Fake=Faker(['en_IN','en-US'])
        # for _ in range(5):
        #     fuser_type = 1
        #     fverified =random.choice([True,False])
        #     fusername=Fake.first_name()
        #     ffirst_name=Fake.first_name()
        #     flast_name=Fake.last_name() 
        #     femail=Fake.ascii_free_email()
        #     fpassword1="qwerty"
        #     fpassword2="qwerty"
            
        #     user=User(user_type=fuser_type,verified=fverified,first_name=ffirst_name,last_name=flast_name,email=femail,username=fusername)
        #     user.set_password(fpassword2)
        #     user.save()
        #     print(f"{fusername} {fuser_type} {femail}")
        # for _ in range(5):
        #     fuser_type = 3
        #     fverified =random.choice([True,False])
        #     fusername=Fake.company()
        #     ffirst_name=Fake.company()
        #     # flast_name=Fake.last_name() 
        #     femail=Fake.ascii_company_email()
        #     fpassword1="qwerty"
        #     fpassword2="qwerty"
        #     fmobile_no=Fake.phone_number()
        #     user=User(user_type=fuser_type,verified=fverified,first_name=ffirst_name,last_name=flast_name,email=femail,username=ffirst_name)
        #     user.set_password(fpassword2)
        #     user.save()
        #     print(f"{fusername} {fuser_type} {femail}")
        # for _ in range(5):
        #     fuser_type = 4
        #     fverified =random.choice([True,False])
        #     fusername=Fake.first_name()
        #     ffirst_name=Fake.first_name()
        #     flast_name=Fake.last_name() 
        #     femail=Fake.ascii_free_email()
        #     fpassword1="qwerty"
        #     fpassword2="qwerty"
        #     fmobile_no=Fake.phone_number()
        #     user=User(user_type=fuser_type,verified=fverified,first_name=ffirst_name,last_name=flast_name,email=femail,username=fusername)
        #     user.set_password(fpassword2)
        #     user.save()
        #     print(f"{fusername} {fuser_type} {femail}")
        # for _ in range(5):
        #     fuser_type = 3
        #     fverified =random.choice([True,False])
        #     fusername=Fake.company()
        #     ffirst_name=Fake.company()
        #     flast_name=Fake.last_name() 
        #     femail=Fake.ascii_company_email()
        #     fpassword1="qwerty"
        #     fpassword2="qwerty"
        #     fmobile_no=Fake.phone_number()
        #     user=User(user_type=fuser_type,verified=fverified,first_name=ffirst_name,email=femail,username=fusername)
        #     user.set_password(fpassword2)
        #     user.save()
        #     print(f"{fusername} {fuser_type} {femail}")
        # print('Printing createdata')
        boards=['CBSE','ICSE','MP BOARD']
        # for _ in range(5):
        # #user class
        #     fschoolName=fake.name()
        #     fLocation_Name=fake.city()
        #     fBoard=random.choice(boards)
        #     print(f"{fschoolName} {fLocation_Name} {fBoard}")
        #     School.objects.get_or_create(Name=fschoolName,Location_Name=fLocation_Name,Board=fBoard)
        # d=School.objects.all()
        # print(d)
        # for _ in range(1):
        #     fDegree_Name='B.Tech'
        #     fDegree_Duration=4
        #     fTotal_Sem=8
        #     fMin_credit=Fake.random_int(100, 200)
        #     Degree.objects.get_or_create(Degree_Name=fDegree_Name,Degree_Duration=fDegree_Duration,Total_Sem=fTotal_Sem,Min_credit=fMin_credit)
        #     fDegree_Name='B.Sc'
        #     fDegree_Duration=3
        #     fTotal_Sem=6
        #     fMin_credit=Fake.random_int(50, 100)
        #     Degree.objects.get_or_create(Degree_Name=fDegree_Name,Degree_Duration=fDegree_Duration,Total_Sem=fTotal_Sem,Min_credit=fMin_credit)
        #     fDegree_Name='BCA'
        #     fDegree_Duration=3
        #     fTotal_Sem=6
        #     fMin_credit=Fake.random_int(50, 100)
        #     Degree.objects.get_or_create(Degree_Name=fDegree_Name,Degree_Duration=fDegree_Duration,Total_Sem=fTotal_Sem,Min_credit=fMin_credit)
        # d=Degree.objects.all()
        # print(d)
        # branch=['CSE','IT','ECE','EE','AU']
        # Year=[2015,2016,2017]
        #branch class
        # d=Degree.objects.all().count()
        # for _ in range(10):
        #     fBranch_Name=random.choice(branch)
        #     dno=Fake.random_int(1, d)
        #     fdegree=Degree.objects.get(pk=dno)
        #     fStart_year=random.choice(Year)
        #     print(f"{fBranch_Name} {fdegree.Degree_Name} {fStart_year}")
        #     Branch.objects.get_or_create(Branch_Name=fBranch_Name,Start_year=fStart_year)
        # bc=Branch.objects.all().count()
        # print(bc)

        # varuser=User.objects.filter(user_type=4)
        # for utr in varuser:
        #     ffirst_name=utr.first_name
        #     flast_name=utr.last_name 
        #     femail=utr.email
            
        #     fmobile_no=int(Fake.numerify(text='%#########'))
        #     Mentor.objects.get_or_create(user=utr,first_name=ffirst_name,last_name=flast_name,Mobile_No=fmobile_no)
        #     print(f"{ffirst_name} {utr.verified} {femail}")
                
        # varuser=Mentor.objects.all()
        # print(varuser.count())
        # for utr in varuser:
        #     print(f"{utr.first_name} {utr.user.verified} {utr.user.user_type}")

        #company
        # Sector_Choices=['Energy','Materials','Industrials','Utilities','Healthcare','Financials','Consumer Discretionary','Information Technology','Real Estate',]
        # varuser=User.objects.filter(user_type=3)
        # for utr in varuser:
        #     ffirst_name=utr.first_name
        #     fDescription=Fake.bs() 
        #     fMCA=Fake.numerify(text= '############')  
        #     fType=random.choice(Sector_Choices)
        #     frevenue=Fake.numerify(text= '#########')
        #     Company.objects.get_or_create(user=utr,Name=ffirst_name,MCA=fMCA,Type=fType,revenue=frevenue,Description=fDescription)
        #     print(f"{ffirst_name} {utr.verified} ")
        
        # comp=Company.objects.all()
        # bcount=Branch.objects.all().count()
        # for company in comp:
        #     fminCTC=int(Fake.numerify(text='#%'))
        #     fmaxCTC=fminCTC+2
        #     fDescription=Fake.paragraph(nb_sentences=3)
        #     fminScore10=60
        #     fminScore12=60
        #     fminJeePercentile=10
        #     id=Fake.random_int(1, bcount)
        #     b1=Branch.objects.get(pk=id)
        #     id=Fake.random_int(1, bcount)
        #     b2=Branch.objects.get(pk=id)
        #     Pos1=Position.objects.get_or_create(Company=company,minJeePercentile=fminJeePercentile,minScore10=fminScore10,minScore12=fminScore12,minCTC=fminCTC,maxCTC=fmaxCTC,Description=fDescription,)
        #     print(Pos1)
        #     Pos1.branch.add(b1)
        #     Pos1.branch.add(b2)
        #     print(f"{Pos1} {b1} {b2}")

        # varuser=Mentor.objects.all()
        # print(varuser.count())
        # for utr in varuser:
        #     print(f"{utr.first_name} {utr.user.verified} {utr.user.user_type}")

        #Students
        
        # varuser=User.objects.filter(user_type=1)
        # Gender_choice=['MALE','FEMALE','OTHERS']
        # SchoolCount=School.objects.all().count()
        # BranchCount=Branch.objects.all().count()
        # print('check1')
        # for urs in varuser:
        #     fenrollment_no=urs.username
        #     ffirst_name=urs.first_name
        #     flast_name=urs.last_name
        #     fgender=random.choice(Gender_choice)
        #     fEmail=urs.email
        #     print('check2')
        #     fMobile_No=int(Fake.numerify(text='%#########'))
        #     sno=Fake.random_int(1,SchoolCount)
        #     fSchool10=School.objects.get(pk=sno)
        #     sno=Fake.random_int(1,SchoolCount)
        #     fSchool12=School.objects.get(pk=sno)
        #     print('check3')
        #     fScore10=80.75
        #     fScore12=90.2
        #     fJeePercentile=80.65
        #     print('check4')
        #     bno=Fake.random_int(1,BranchCount)
        #     fBranch=Branch.objects.get(pk=bno)
        #     fAim=Fake.paragraph(nb_sentences=3)
        #     fObjective=Fake.paragraph(nb_sentences=3)
        #     fMission=Fake.paragraph(nb_sentences=3)
        #     fVision=Fake.paragraph(nb_sentences=3)
        #     print('check5')
        #     fPlacementCell=PlacementCell.objects.get(pk=1)
        #     Stu=Student.objects.create(user=urs,
        #     enrollment_no=fenrollment_no,
        #     first_name=ffirst_name,
        #     last_name=flast_name,
        #     gender=fgender,
        #     Email=fEmail,
        #     Mobile_No=fMobile_No,
        #     School10=fSchool10,
        #     School12=fSchool12,
        #     Score10=fScore10,
        #     Score12=fScore12,
        #     JeePercentile=fJeePercentile,
        #     Branch=fBranch,
        #     Aim=fAim,
        #     Objective=fObjective,
        #     Mission=fMission,
        #     Vision=fVision,
        #     PlacementCell=fPlacementCell,
        #     )
        #     print(Stu)

        #placementOfficer
        #Message
        #MessageP2S
        #To all Student
        # Stu=Student.objects.filter(user__verified=True)
        # dt=timezone.now()
        # print(dt)
        # pla=PlacementCell.objects.get(pk=1)
        # bd=Fake.paragraph(nb_sentences=3)
        # msg2s=MessageP2S.objects.create(Body=bd,TimeStamps=dt,sender=pla,type='Test')
        # msg2s.receivers.add(*Stu)
        # print(msg2s)

        # #MessageP2C
        # comp=Company.objects.all()
        # sndr=PlacementCell.objects.get(pk=1)
        # dt=timezone.now()
        # print(dt)
        # bd=Fake.paragraph(nb_sentences=3)
        # msg2c=MessageP2C.objects.create(sender=sndr,TimeStamps=dt,Body=bd)
        # msg2c.receivers.add(*comp)
        # print(msg2c)

        # #messagec2p
        # dt=timezone.now()
        # print(dt)
        # bd=Fake.paragraph(nb_sentences=3)
        # print(bd)
        # comp=Company.objects.filter(user__verified=True)
        # c1=comp[0]
        # print(comp)
        # print(c1)
        # rec=PlacementCell.objects.get(pk=1)
        # print(rec)
        # msg2p=MessageC2P.objects.create(sender=c1,receivers=rec,TimeStamps=dt,Body=bd)
        # print(msg2p)
        
        #Offers
        # Pos=Position.objects.get(pk=1)
        # desc=Fake.paragraph(nb_sentences=3)
        # fctc=Pos.minCTC+1
        # print(f"{Pos} {desc} {fctc}")
        # o1=Offers.objects.create(Position=Pos,
        # Description=desc,
        # FinalCTC=fctc,)
        # print(o1)

        # #Applied
        # Status_Choices=[('S','Selected'),('ENR','EligibleForNextRound'),('R','Rejected'),('UE','UnderEvaluation'),]
        # Stu=Student.objects.all()
        # print(Stu)
        # Stu=Stu[0]
        # print(Stu)
        # Pos=Position.objects.all()
        # print(Pos)
        # Pos=Pos[0]
        # print(Pos)
        # status=random.choice(Status_Choices)
        # print(status)
        # #o1=Offers.objects.get(pk=1)
        # desc=Fake.paragraph(nb_sentences=3)
        # a1=Applied.objects.create(Student=Stu,Position=Pos,Description=desc,)
        # print(a1)
        # #mentor
        # m=Mentor.objects.get(pk=1)
        # Stu=Student.objects.all()
        # m.student_set.add(*Stu)
        # #or
        # for Stud in Stu:
        #     Stud.mentor=m
        

