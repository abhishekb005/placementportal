import datetime
from typing_extensions import final

import pyrebase
from django.conf.urls import include
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import query,Avg, Max, Min

from django.shortcuts import redirect, render,HttpResponse,redirect,get_object_or_404,HttpResponseRedirect
from .forms import *
from django.core.files.storage import default_storage
from django.http import Http404
from django.contrib import messages
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required
from .models import *
#from django.forms import modelform_factory
from django.forms import modelformset_factory
import csv
from .Credential import conf

firebase=pyrebase.initialize_app(conf.getConfig())
storage=firebase.storage()
# *.log
# local_settings.py
# db.sqlite3
# pywin32==301
# pywin32-ctypes==0.2.0
# pypiwin32==223
# Create your views here.
def userlogin(request):
    if request.user.is_authenticated:
        return HttpResponse('<h1> Current Session User is already Authenticated <a href="/Dashboard"> Dashboard </a></h1>') 
        render(request,'placementapp/dashboard.html',{'user':request.user})
    else:
        if request.method=="POST":
            form=AuthenticationForm(request,data=request.POST)
            if form.is_valid():
                username=form.cleaned_data.get('username')
                password=form.cleaned_data.get('password')
                varuser=authenticate(username=username,password=password)
                if varuser is not None:
                    login(request,varuser)
                    messages.info(request,f"You are logged in as {username}")
                    return render(request,'placementapp/dashboard.html',{'user':varuser})
                else:
                    messages.error(request,f"Invalid")
            else:
                messages.error(request,"Invalid username")

        form=AuthenticationForm()
        return render(request,'placementapp/login.html',{'form':form})
            
def userlogout(request):
    logout(request)
    messages.info(request,"You have Successfully logged out")
    return redirect("/login")
    
def signup(request):
    if request.user.is_authenticated:
        return redirect("/dashboard")
    else:
        if request.method=='POST':
            form=StudentSignUpForm(request.POST)
            if form.is_valid():
                form.save()
                form=StudentSignUpForm()
                #return render(request,'placementapp/signup.html',{'form':form})
        else:
            form=StudentSignUpForm()
        return render(request,'placementapp/signup.html',{'form':form})

def Stusignup(request):
    if request.user.is_authenticated and request.user.user_type!=2:
        return redirect("/dashboard")
    else:
        if request.method=='POST':
            form=StudentSignUpForm(request.POST)

            if form.is_valid():
                form.save()
                messages.success(request, 'Student Registered Successfully !')
                if request.user.is_authenticated and request.user.user_type==2:
                    form=StudentSignUpForm()
                else:
                    return redirect('/login')
                #return render(request,'placementapp/signup.html',{'form':form})
            else:
                messages.error(request, 'Enter Valid Information')
        else:
            messages.info(request, 'Enter University Enrollment No.(Upper Case) in Username Field else Account will not get Verifield')
            form=StudentSignUpForm()
        return render(request,'placementapp/Student/signup.html',{'form':form})
    
def CompanySignUp(request):
    if request.user.user_type==2 and request.user.verified:
        if request.method=='POST':
            form=CompanySignUpForm(request.POST)
            form2=CompanyProfile(request.POST)
            if form.is_valid() and form2.is_valid():
                user=form.save()
                if request.user.user_type==2:
                    user.verified=True
                else:
                    user.verified=False
                    user.save()
                form2.save(user)
                messages.success(request, 'Company registered successfully.')
                form=CompanySignUpForm()
                form2=CompanyProfile()
            else:
                messages.error(request, 'Company Sign Up Not Valid ,Fill the Form Correctly')
                #return render(request,'placementapp/signup.html',{'form':form})
        else:
            form=CompanySignUpForm()
            form2=CompanyProfile()
        return render(request,'placementapp/Company/signup.html',{'form':form,'form2':form2})
    return HttpResponse('<h1> Current User is not Authorised </h1>')

def MentorSignUp(request):
    if request.user.user_type==2 and request.user.verified:
        if request.method=='POST':
            form=MentorSignUpForm(request.POST)
            form2=MentorProfile(request.POST)
            if form.is_valid() and form2.is_valid():
                form.save()
                messages.success(request, 'Mentor registered successfully.')
                
                form=MentorSignUpForm()
                form2=MentorProfile(request.POST)
            else:
                messages.error(request, 'Mentor Sign Up Not Valid ,Fill the Form Correctly')
            
                #return render(request,'placementapp/signup.html',{'form':form})
        else:
            form=MentorSignUpForm()
            form2=MentorProfile()
        return render(request,'placementapp/Mentor/signup.html',{'form':form,'form2':form2})
    return HttpResponse('<h1> Current User is not Authorised </h1>')

def PlacementOfficerSignUp(request):
    if request.user.user_type==2 and request.user.verified:
        if request.method=='POST':
            form=PlacementOfficerSignUpForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'PlacementOfficer registered successfully.')
         
                form=PlacementOfficerSignUpForm()
            else:
                messages.error(request,f"Invalid Form , Fill Correctly")
                #return render(request,'placementapp/signup.html',{'form':form})
        else:
            form=PlacementOfficerSignUpForm()
        return render(request,'placementapp/PlacementOff/signup.html',{'form':form})
# def AppliedPositions(request):
#     if request.user.is_authenticated and request.user.user_type==1 and request.user.verified:
#         applied=Applied.objects.filter(Student__user=request.user)
#         # position=[]
#         # for x in applied:
#         #     position.append(x.Position)
#         return render(request,'placementapp/PositionApply.html',{'Positions':position})
#     return HttpResponse('<h1> Current User is not A Student or  verified </h1>')

def applyView(request):
    if request.user.is_authenticated and request.user.user_type==1 and request.user.verified:
        alreadyApplied=Applied.objects.filter(Student__user=request.user)
        alreadyAppliedPositions=[]
        alreadyAppliedOffer=[]
        Stu=Student.objects.get(user=request.user)
        max=Stu.maxCTC
        for applied in alreadyApplied:
            alreadyAppliedPositions.append(applied.Position.id)
            if applied.FinalOffer is not None:
                if max<applied.FinalOffer.FinalCTC:
                    max=applied.FinalOffer.FinalCTC
        Stu.maxCTC=max
        Stu.save()
        position=Position.objects.filter(branch=Stu.Branch,visible=True).exclude(id__in=alreadyAppliedPositions,)
        return render(request,'placementapp/Student/PositionApply.html',{'Positions':position})
    return HttpResponse('<h1> Current User is not A Student or  verified </h1>')

def applyForPosition(request,id):
    varuser=request.user
    if request.method=='POST' and varuser.is_authenticated and varuser.user_type==1 :
        Stu=Student.objects.get(user=varuser)
        pos=Position.objects.get(pk=id)
        #branchds=pos.branch
        #if stu.branch in branchds:
        if pos.minScore10<=Stu.Score10 and pos.minScore12<=Stu.Score12 and pos.minJeePercentile<=Stu.JeePercentile and pos.maxCTC>Stu.maxCTC+2 and pos.visible :
            Applied.objects.get_or_create(Position=pos,Student=Stu)
            print(f'{Stu} {pos}')
            return HttpResponseRedirect('/ApplyPosition')
        else:
            return HttpResponse('<h1> Not Eligible For Position Due To Marks Or Might Be Placed with Good CTC</h1>')
    else:
        return HttpResponse('<h1> Not Authenticated or verified Student </h1>')


def StudentList(request):
    varuser=request.user
    if varuser.user_type==4:
        mentr=Mentor.objects.get(user=varuser)
        Stu=Student.objects.filter(mentor=mentr)
        return Stu
    if varuser.user_type==2:
        Stu=Student.objects.all().order_by('Branch')
        return Stu


def StudentUpdateProfile(request):
    if request.user.is_authenticated:
        if request.user.user_type==1:
            stu=Student.objects.get(user=request.user)
            url=stu.ResumeURL
            if request.method=='POST':
                form=StudentForm(request.POST,request.FILES,instance=stu)
                if form.is_valid():
                    f=form.save(commit=False)
                    file = request.FILES['Resume']
                    print(file)
                    print(f)
                    if file is not None:
                        file_save = default_storage.save(file.name, file)
                        storage.child("resume/"+file.name).put("media/" + file.name)
                        url=storage.child("resume/"+file.name).get_url(None)
                        print(url)
                        delete = default_storage.delete(file.name)
                        messages.success(request, "File upload in Firebase Storage successful")
                        f.ResumeURL=url
                    f.save()
                    messages.success(request, "Profile Updated Successfully")
                else:
                    messages.error(request,f"Invalid Form ,profile Not Updated")
            else:
                messages.info(request,f"After Updating the Profile ,Only then This Account will be Verified")
                form=StudentForm(instance=stu)
                url=stu.ResumeURL
            return render(request,'placementapp/Student/UpdateProfile.html',{'form':form,'url':url})
        else:
            return HttpResponse('<h1> Current User is not of A Student </h1>')
    else:
        return HttpResponse('<h1> Current Session User Not Authenticated </h1>') 


def getMsg2S(request):
    varuser=request.user
    msg=None
    if varuser.is_authenticated and varuser.user_type==1 :
        stu=Student.objects.get(user=varuser)
        msg=MessageP2S.objects.filter(receivers=stu).order_by('TimeStamps')
    if varuser.is_authenticated and varuser.user_type==2 and varuser.verified:
        msg=MessageP2S.objects.all().order_by('TimeStamps')
    return msg

def getMsg2C(request):
    varuser=request.user
    msg=None
    if varuser.is_authenticated and varuser.user_type==3 and varuser.verified:
        comp=Company.objects.get(user=varuser)
        msg=MessageP2C.objects.filter(receivers=comp).order_by('TimeStamps')
    if varuser.is_authenticated and varuser.user_type==2 and varuser.verified:
        msg=MessageP2C.objects.all().order_by('TimeStamps')
    return msg

# retrive Msg Recieved By Placement Officer or sended to placementCell by Company
def getMsg2P(request):
#USer VAriable
    varuser=request.user
    msg=None
    #if User is 
    if varuser.is_authenticated and varuser.user_type==3 and varuser.verified:
        comp=Company.objects.get(user=varuser)
        msg=MessageC2P.objects.filter(sender=comp).order_by('TimeStamps')

    if varuser.is_authenticated and varuser.user_type==2 and varuser.verified:
        msg=MessageC2P.objects.all().order_by('TimeStamps')
    return msg
def ListOfPositionsApplied(request):
    varuser=request.user
    applied=None
    if varuser.is_authenticated and varuser.verified :
        if varuser.user_type==3:
            comp=Company.objects.get(user=varuser)
            applied=Applied.objects.filter(Position__Company=comp)
            return render(request,'placementapp/Company/ListAppliedStuForPos.html',{'dataset':applied})

        if varuser.user_type==1:
            stu=Student.objects.get(user=varuser)
            applied=Applied.objects.filter(Student=stu)
            return render(request,'placementapp/Student/ListOfPositionsApplied.html',{'dataset':applied})

        elif varuser.user_type==2:
            applied=Applied.objects.all().order_by('-Time')
            return render(request,'placementapp/PlacementOff/ListOfApplied.html',{'dataset':applied})

    return HttpResponse('<h1> Session User not a verified User </h1>')

def AppliedDetailView(request,id):
    varuser=request.user
    if varuser.verified and varuser.is_authenticated:
        if varuser.user_type==2:
            applied=Applied.objects.get(pk=id)
            if applied is not None:
                return render(request,'placementapp/PlacementOff/AppliedDetail.html',{'data': applied})
            return HttpResponse('<h1>No Applied Detail  </h1>')
        return HttpResponse('<h1>Not Authorised  </h1>')

def DeleteApplied(request,id):
    try:
        applied = get_object_or_404(Applied,id =id)
    except Exception:
        raise Http404('Does Not Exist')
 
    #if request.method == 'POST':
    applied.delete()
    return HttpResponseRedirect('/applied')
    # else:
    #     return render(request, 'placementapp/PlacementOff/deleteapplied.html')

def UpdateApplied(request,id):
    try:
        old_data = get_object_or_404(Applied,id=id)
    except Exception:
        raise Http404('Does Not Exist')
    if request.method =='POST':
        form =AppliedForm(request.POST, instance =old_data)
        if form.is_valid():
            form.save()
            return redirect(f'/Applied/update/{id}')
    else:
        form = AppliedForm(instance = old_data)
        context ={
            'form':form
        }
        return render(request,'placementapp/PlacementOff/updateApplied.html',context)

def OfferStudentView(request):
    varuser=request.user
    if varuser.is_authenticated and varuser.verified and varuser.user_type==1:
        applieds=Applied.objects.filter(Student__user=varuser,Status='Selected').exclude(FinalOffer=None)
        offers=[]
        if applieds is not  None:
            for applied in applieds:
                offers.append(applied.FinalOffer)
            
            return render(request,'placementapp/Student/Offers.html',{'dataset':offers})
        return HttpResponse('<h1>No Offers </h1>')
    return HttpResponse('<h1> Session User not a verified Student </h1>')

def ListOfAppliedStuForPos(request,id):
    varuser=request.user
    appliedStu=None
    if varuser.is_authenticated and varuser.verified:
        if varuser.user_type==3:
            appliedStu=Applied.objects.filter(Position__id=id)
            return render(request,'placementapp/Company/ListAppliedStuForPos.html',{'dataset':appliedStu})
        elif varuser.user_type==2:
            appliedStu=Applied.objects.filter(Position__id=id)
            return render(request,'placementapp/PlacementOff/ListAppliedStuForPos.html',{'dataset':appliedStu})
    return HttpResponse('<h1> Current Session User is not  Authorised</h1>') 


def StudentDetailView(request,id):
    varuser=request.user
    if varuser.verified and varuser.is_authenticated:
        if varuser.user_type==4:
            StuUser=User.objects.get(pk=id)
            mentorr=Mentor.objects.get(user=varuser)
            Stu=None
            if StuUser.user_type==1:
                Stu=Student.objects.get(user=StuUser,mentor=mentorr)
            
            if Stu is not None:
                return render(request,'placementapp/Mentor/StudentDetail.html',{'dataset': Stu})
            else:
                return HttpResponse('<h1>This Student Mentor is different from current  </h1>')
        if varuser.user_type==2:
            StuUser=User.objects.get(pk=id)
            Stu=None
            if StuUser.user_type==1:
                Stu=Student.objects.get(user=StuUser)
            if Stu is None:
                return HttpResponse('<h1>This Student Mentor is different from current  </h1>')

            else:
                return render(request,'placementapp/PlacementOff/StudentDetail.html',{'dataset': Stu})
            
        if varuser.user_type==3:
            StuUser=User.objects.get(pk=id)
            Stu=None
            applied=None
            if StuUser.user_type==1:
                Stu=Student.objects.get(user=StuUser)
                comp=Company.objects.get(user=varuser)
                applied=Applied.objects.filter(Student=Stu,Position__Company=comp)
            if applied is not None:
                return render(request,'placementapp/Company/StudentDetail.html',{'dataset': Stu})
            return HttpResponse('<h1>Student Did Not Apply for This Compny , So Detail View Not Available  </h1>')
    return HttpResponse('<h1> Current User Not Authorised or Verified  </h1>')

def StudentDetailView1(request,Stuenrollment):
    varuser=request.user
    Stu=Student.objects.get(enrollment_no=Stuenrollment)
    id=10
    if Stu is not None:
        id=Stu.user.id
    if varuser.verified and varuser.is_authenticated:
        if varuser.user_type==4:
            StuUser=User.objects.get(pk=id)
            mentorr=Mentor.objects.get(user=varuser)
            Stu=None
            if StuUser.user_type==1:
                Stu=Student.objects.get(user=StuUser,mentor=mentorr)
            
            if Stu is not None:
                return render(request,'placementapp/Mentor/StudentDetail.html',{'dataset': Stu})
            else:
                return HttpResponse('<h1>This Student Mentor is different from current  </h1>')
        if varuser.user_type==2:
            StuUser=User.objects.get(pk=id)
            Stu=None
            if StuUser.user_type==1:
                Stu=Student.objects.get(user=StuUser)
            if Stu is None:
                return HttpResponse('<h1>This Student Mentor is different from current  </h1>')

            else:
                return render(request,'placementapp/PlacementOff/StudentDetail.html',{'dataset': Stu})
            
        if varuser.user_type==3:
            StuUser=User.objects.get(pk=id)
            Stu=None
            applied=None
            if StuUser.user_type==1:
                Stu=Student.objects.get(user=StuUser)
                comp=Company.objects.get(user=varuser)
                applied=Applied.objects.filter(Student=Stu,Position__Company=comp)
            if applied is not None:
                return render(request,'placementapp/Company/StudentDetail.html',{'dataset': Stu})
            return HttpResponse('<h1>Student Did Not Apply for This Compny , So Detail View Not Available  </h1>')
    return HttpResponse('<h1> Current User Not Authorised or Verified  </h1>')

def DeleteStudent(request,id):
    varuser=request.user
    if varuser.verified and varuser.is_authenticated:
        if varuser.user_type==4 or varuser.user_type==2:

            try:
                student = Student.objects.get(user__id=id)
            except Exception:
                raise Http404('Does Not Exist')
        
            if request.method == 'POST':
                student.delete()
                return redirect('/')
            else:
                return render(request, 'placementapp/PlacementOff/deleteStudent.html')
    return HttpResponse('<h1> Current Session User is not  Authorised</h1>') 

def UpdateStudent(request,id):
    varuser=request.user
    if varuser.verified and varuser.is_authenticated:
        if varuser.user_type==4 or varuser.user_type==2:

            try:
                student = Student.objects.get(user__id=id)
            except Exception:
                raise Http404('Does Not Exist')
            if request.method =='POST':
                form =StudentForm(request.POST, instance=student)
                if form.is_valid():
                    form.save()
                    return redirect(f'/Student/update/{id}')
            else:
                form = StudentForm(instance = student)
                context ={
                    'form':form
                }
                return render(request,'placementapp/PlacementOff/updateStudent.html',context)
    return HttpResponse('<h1> Current Session User is not  Authorised</h1>') 

def ListStudentView(request):
    varuser=request.user
    if varuser.is_authenticated and varuser.verified and varuser.user_type==4:
        mentr=Mentor.objects.get(user=varuser)
        Stu=Student.objects.filter(mentor=mentr)
        return render(request, 'placementapp/Mentor/ListStudent.html',{'dataset':Stu})

    if varuser.is_authenticated and varuser.verified and varuser.user_type==2:
        Stu=Student.objects.all()
        return render(request, 'placementapp/PlacementOff/ListStudent.html',{'dataset':Stu})
    return HttpResponse('<h1> Current User Not Authorised or Verified  </h1>')


def createPosition(request):
    if request.method=='POST' and request.user.user_type==3 :
        comp=Company.objects.get(user=request.user)
        form=PositionForm(request.POST)
        if form.is_valid():
            pos=form.save(commit=False)
            pos.Company=comp
            pos.save()
            messages.success(request,f"Position Created Successfully")
        else:
            messages.error(request,f"Invalid Form , Position Not Created")
    messages.info(request,f"Create A Position/Role for which The Company want to Hire Students")
    form=PositionForm()
    return render(request,'placementapp/Company/createposition.html',{'form':form})
    
def UpdatePosition(request,_id):
    if request.user.is_authenticated and request.user.verified:
        if request.user.user_type==2:

            try:
                old_data = get_object_or_404(Position,id =_id)
            except Exception:
                raise Http404('Does Not Exist')
        
            if request.method =='POST':
                form =PositionPlacementForm(request.POST, instance =old_data)
                if form.is_valid():
                    form.save()
                    return redirect(f'/Position')
            else:
                form = PositionPlacementForm(instance = old_data)
                context ={
                    'form':form
                }
                return render(request,'placementapp/PlacementOff/updateposition.html',context)
        if request.user.user_type==3:

            try:
                old_data = get_object_or_404(Position,id =_id)
                if old_data.Company.user!=request.user:
                    return HttpResponse('<h1> Current Session User is not  Authorised</h1>')
            except Exception:
                raise Http404('Does Not Exist')
        
            if request.method =='POST':
                form =PositionForm(request.POST, instance =old_data)
                if form.is_valid():
                    form.save()
                    return redirect(f'/Position')
            else:
                form = PositionForm(instance = old_data)
                context ={
                    'form':form
                }
                return render(request,'placementapp/Company/updateposition.html',context)
    return HttpResponse('<h1> Current Session User is not  Authorised</h1>') 

def DeletePosition(request,_id):
    if request.user.is_authenticated and request.user.verified:
        if request.user.user_type==2:

            try:
                data = get_object_or_404(Position,id =_id)
            except Exception:
                raise Http404('Does Not Exist')
        
            if request.method == 'POST':
                data.delete()
                return HttpResponseRedirect('/Position')
            else:
                return render(request, 'placementapp/PlacementOff/deleteposition.html')
    return HttpResponse('<h1> Current Session User is not  Authorised</h1>') 


def CreateOffer(request):
    if request.user.user_type==3 or request.user.user_type==2 and request.user.verified:
        if request.method=='POST':
            form=OfferForm(request.user,request.POST,)
            if form.is_valid():
                offer=form.save(commit=False)
                offer.save()
                messages.success(request,f'Offer Created Succesfully')
                return redirect('/Dashboard')
            else:
                messages.error(request,f'invalid Form')
        else:
            messages.info(request,f"Create Offer Group and Then Assign This Created offer to Selected Students")
            form=OfferForm(request.user)
            return render(request,'placementapp/Company/CreateOffer.html',{'form':form})    
    return redirect('/Dashboard')    

def UpdateOffer(request,id):
    if request.user.is_authenticated and request.user.verified :
        if request.user.user_type==3:
    
            try:
                old_data = get_object_or_404(Offers,id =id)
                Pos=old_data.Position
                if Pos.Company.user==request.user:
                    print("Correct User")
                else:
                    old_data=None
            except Exception:
                raise Http404('Does Not Exist')
        
            if request.method =='POST':
                form =OfferForm(request.user,request.POST, instance =old_data)
                if form.is_valid():
                    form.save()
                    return redirect(f'/Offer/update/{id}')
            else:
                form = OfferForm(request.user,instance = old_data)
                context ={
                    'form':form
                }
                return render(request,'placementapp/Company/updateOffer.html',context)
        elif request.user.user_type==2:
    
            try:
                old_data = get_object_or_404(Offers,id =id)
               
            except Exception:
                raise Http404('Does Not Exist')
        
            if request.method =='POST':
                form =OfferForm(request.user,request.POST, instance =old_data)
                if form.is_valid():
                    form.save()
                    return redirect(f'/Offer/update/{id}')
            else:
                form = OfferForm(request.user,instance = old_data)
                context ={
                    'form':form
                }
                return render(request,'placementapp/PlacementOff/updateOffer.html',context)

    return HttpResponse('<h1> Current Session User is not  Authorised</h1>') 


def DeleteOffer(request,id):
    if request.user.is_authenticated and request.user.verified :
        if request.user.user_type==3:
            try:
                data = get_object_or_404(Offers,id=id)
                Pos=data.Position
                if Pos.Company.user==request.user:
                    print("Correct User")
                else:
                    return HttpResponse("<H1>Not Authorised</H1>")
            except Exception:
                raise Http404('Does Not Exist')
        
            if request.method == 'POST':
                data.delete()
                return HttpResponseRedirect('/Offer')
            else:
                return render(request, 'placementapp/Company/deleteOffer.html')
        elif request.user.user_type==2:
            try:
                data = get_object_or_404(Offers,id=id)
                
                
            except Exception:
                raise Http404('Does Not Exist')
        
            if request.method == 'POST':
                data.delete()
                return HttpResponseRedirect('/Offer')
            else:
                return render(request, 'placementapp/PlacementOff/deleteOffer.html')
    return HttpResponse('<h1> Current Session User is not  Authorised</h1>') 


def ListOffer(request):
    if request.user.is_authenticated and request.user.verified:
        if request.user.user_type==1:
            Stu=Student.objects.get(user=request.user)
            offers=[]
            applieds=Applied.objects.filter(Student=Stu).exclude(FinalOffer=None)
            for applied in applieds:
                offers.append(applied.FinalOffer)
            return render(request,'placementapp/Student/Offers.html',{'dataset':offers})
        
        if request.user.user_type==3:
            comp=Company.objects.get(user=request.user)
            #positions=Position.objects.filter(Company=comp)
            offers=Offers.objects.filter(Position__Company=comp)
            return render(request,'placementapp/Company/Offers.html',{'dataset':offers})
        
        if request.user.user_type==2:
            offers=Offers.objects.all()
            return render(request,'placementapp/PlacementOff/Offers.html',{'dataset':offers})    
        
        if request.user.user_type==4:
            Stu=Student.objects.filter(mentor__user=request.user)
            applied=Applied.objects.filter(Student__in=Stu,).exclude(FinalOffer=None)
            offers={}
            for x in applied:
                offers.add(x.FinalOffer)        
            
            return render(request,'placementapp/PlacementOff/Offers.html',{'dataset':offers})    

    return HttpResponse('<h1>Not Authorised</h1>')

def ListCompany(request):
    if request.user.user_type==2 and request.user.is_authenticated and request.user.verified:
        comp=Company.objects.all()
        return render(request,'placementapp/PlacementOff/ListCompany.html',{'dataset':comp})
    return HttpResponse('<h1> Current Session User is not  Authorised</h1>') 

def UpdateCompany(request,id):
    if request.user.is_authenticated and request.user.verified:
        if request.user.user_type==2:
            try:
                company = Company.objects.get(user__id=id)
            except Exception:
                raise Http404('Does Not Exist')
            if request.method =='POST':
                form = CompanyForm(request.POST, instance=company)
                if form.is_valid():
                    form.save()
                    messages.success(request, ' Details Updated !')
                
                    return redirect(f'/CompanyList')
            else:
                form = CompanyForm(instance = company)
                context ={
                    'form':form
                }
                return render(request,'placementapp/PlacementOff/updateCompany.html',context)
    return HttpResponse('<h1> Current Session User is not  Authorised</h1>') 

def DeleteCompany(request,id):
    if request.user.is_authenticated and request.user.verified:
        if request.user.user_type==2:
            try:
                company = Company.objects.get(user__id=id)
            except Exception:
                raise Http404('Does Not Exist')
        
            if request.method == 'POST':
                if company is not None:
                    company.delete()
                return redirect('/CompanyList')
            else:
                return render(request, 'placementapp/PlacementOff/deleteCompany.html')
    return HttpResponse('<h1> Current Session User is not  Authorised</h1>') 

def ListPositionView(request):
    if request.user.user_type==4 and request.user.is_authenticated and request.user.verified:
        return HttpResponse('<h1> Mentor: No Company Position </h1>')
    elif request.user.is_authenticated and request.user.verified and request.user.user_type==3:
        Comp=Company.objects.get(user=request.user)
        positions=Position.objects.filter(Company=Comp)
        return render(request, 'placementapp/Company/ListPositions.html',{'dataset':positions}) 
    elif request.user.is_authenticated and request.user.verified and request.user.user_type==1:
        Stu=Student.objects.get(user=request.user)
        positions=Position.objects.filter(branch=Stu.Branch)
        return render(request, 'placementapp/Student/ListPositions.html',{'dataset':positions}) 
    elif request.user.is_authenticated and request.user.verified and request.user.user_type==2:
        positions=Position.objects.all()
        return render(request, 'placementapp/PlacementOff/ListPositions.html',{'dataset':positions})     
    else:
        return HttpResponse('<h1> Current Session User might not be Authenticated or verified by the PlacementCell or Mentor</h1>') 
        
def AssignOffer(request):
    if request.user.is_authenticated and request.user.verified:
        if request.user.user_type==3:
            
            comp=Company.objects.get(user=request.user)
            AppliedForm=modelformset_factory(
                Applied,
                exclude=("Description",),
                extra=0,
               # formset=BaseAppliedFormSet,
                form=MyAppliedForm,
            )
            if request.method=='POST':
                formset=AppliedForm(
                request.POST,
                queryset=Applied.objects.filter(Position__Company=comp,Status='Selected'),
                #form_kwargs={'user': request.user},
               # user=request.user,
                )
                if formset.is_valid():
                    
                    v=formset.save(commit=False)
                    for form in v:
                        finaloffer=form.FinalOffer
                        print(finaloffer)
                        finalCTC=finaloffer.FinalCTC
                        print(finalCTC)
                        applieds=form
                        Stuu=applieds.Student
                        print(Stuu)
                        Stumaxctc=Stuu.maxCTC
                        print(Stumaxctc)
                        if(Stumaxctc<finalCTC):
                            Stuu.maxCTC=finalCTC
                            Stuu.save()
                        print(type(Stuu))
                        print(type(form))
                        print(str(form))
                        form.save()
                        
                    messages.success(request,f"Offers Assigned Sucessfully")
                else:
                    messages.error(request,f"Failure:Offers Not Assigned")
            if request.method=='GET':
                messages.info(request,f'Assign Offers To Selected Students')
                formset=AppliedForm(
                    queryset=Applied.objects.filter(Position__Company=comp,Status='Selected')
                #form_kwargs={'user': request.user},
                #user=request.user,
                    )
            for form in formset:
                form.fields['Position'].queryset=Position.objects.filter(Company=comp)
                form.fields['Student'].queryset=Student.objects.filter(AppliedPositions__Company=comp)
                form.fields['FinalOffer'].queryset=Offers.objects.filter(Position__Company=comp)
            return render(request,'placementapp/Company/assignOffer.html',{'formset':formset})
    return HttpResponse('<h1> Current Session User might not be Authenticated or verified by the PlacementCell or Mentor</h1>') 

def AddStudentMentor(request):
    varuser=request.user
    formset=None
    if varuser.is_authenticated and varuser.user_type==4 and varuser.verified:
    #if varuser.is_authenticated:
        Mentorr=Mentor.objects.get(user=varuser)
        StudentMentorForm=modelformset_factory(
            Student,
            fields=['enrollment_no',],
            extra=20,
            max_num=22,
            can_delete=True,
            can_delete_extra=False,
        #formset=BaseAppliedFormSet,
        #form=MyAppliedForm,
        )
        if request.method=='POST':
            formset=StudentMentorForm(
            request.POST,
            queryset=Student.objects.filter(mentor__user=varuser),
            #form_kwargs={'user': request.user},
            #user=request.user,
            )
            if formset.is_valid():
                #print(formset)
                v=formset.save(commit=False)
                for obj in formset.deleted_objects:
                    obj.mentor=None
                    obj.save()
                for obj in formset.new_objects:
                    StuUser=User.objects.get(username=obj.enrollment_no)
                    if StuUser is not None:
                        Stu=Student.objects.get(enrollment_no=obj.enrollment_no)
                        if Stu.mentor is None:
                            Stu.mentor=Mentorr
                            Stu.save()
                            print(Stu)
                        else:
                            messages.info(request,f"Mentor Already Assigned")
                            print("Mentor Already Assigned")
                    else:
                        print("Not Correct UserName")
                    
        
        formset=StudentMentorForm(
            queryset=Student.objects.filter(mentor__user=varuser),
            #form_kwargs={'user': request.user},
            #user=request.user,
            )
    # for form in formset:
    #     form.fields['Position'].queryset=Position.objects.filter(Company=comp)
    #     form.fields['Student'].queryset=Student.objects.filter(AppliedPositions__Company=comp)
    #     form.fields['FinalOffer'].queryset=Offers.objects.filter(Position__Company=comp)
    return render(request,'placementapp/PlacementOff/assignMentor.html',{'formset':formset})

def UpdateAppliedStuStatus(request):
    if request.user.is_authenticated and request.user.verified:
        if request.user.user_type==3:
            comp=Company.objects.get(user=request.user)
            AppliedForm=modelformset_factory(
                Applied,
                #fields="__all__",
                exclude=("FinalOffer","Time",),
                #formset=BaseAppliedFormSet,
                extra=0,
                #form=UpdateAppliedStuStatusForm,
            )
            if request.method=='POST':
                formset=AppliedForm(
                request.POST,
                queryset=Applied.objects.filter(Position__Company=comp).exclude(Status="Rejected"),
                #form_kwargs={'user': request.user},
                #user=request.user,
                )
                if formset.is_valid():
                    v=formset.save()
            
            formset=AppliedForm(
                queryset=Applied.objects.filter(Position__Company=comp).exclude(Status="Rejected")
                )
            for form in formset:
                form.fields['Position'].queryset=Position.objects.filter(Company=comp)
                form.fields['Student'].queryset=Student.objects.filter(AppliedPositions__Company=comp)
                #form.fields['FinalOffer'].queryset=Offers.objects.filter(Position__Company=comp)

            return render(request,'placementapp/Company/assignOffer.html',{'formset':formset})
    return HttpResponse('<h1> Current Session User might not be Authenticated or verified by the PlacementCell or Mentor</h1>') 

def VerifyStudentView(request):
    varuser=request.user
    if varuser.is_authenticated and varuser.user_type==4 or varuser.user_type==2 and varuser.verified:
    #if varuser.is_authenticated:
        #Mentorr=Mentor.objects.get(user=varuser)
        if varuser.user_type==4:
            Stu=Student.objects.filter(mentor__user=varuser)
        elif varuser.user_type==2:
            Stu=Student.objects.filter(user__verified=False)
        userr=[]
        for student in Stu:
            userr.append(student.user.id)
        StudentMentorForm=modelformset_factory(
            User,
            fields=['verified','username',],
            extra=0,
            max_num=20,
        #formset=BaseAppliedFormSet,
        form=StudentVerifyForm,
        )
        if request.method=='POST':
            formset=StudentMentorForm(
            request.POST,
            queryset=User.objects.filter(id__in=userr),
            #form_kwargs={'user': request.user},
            #user=request.user,
            )
            if formset.is_valid():
                #print(formset)
                v=formset.save(commit=False)
                for obj in v:
                    obj.save()
                    #Stu=Student.objects.get(enrollment_no=obj.enrollment_no)
                    #Stu.mentor=Mentorr
                    #Stu.save()
                    #print(Stu)
                
        
        formset=StudentMentorForm(
            queryset=User.objects.filter(id__in=userr),
            #form_kwargs={'user': request.user},
            #user=request.user,
            )
    # for form in formset:
    #     form.fields['Position'].queryset=Position.objects.filter(Company=comp)
    #     form.fields['Student'].queryset=Student.objects.filter(AppliedPositions__Company=comp)
    #     form.fields['FinalOffer'].queryset=Offers.objects.filter(Position__Company=comp)
        return render(request,'placementapp/VerifyStudent.html',{'formset':formset})
    return HttpResponse("<h1> Not Authorised</h1>")


def export(request,headerrow):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(headerrow)
    print(headerrow)
    if "AppliedPosition" in headerrow:
        headerrow.remove("AppliedPosition") 
    for student in Student.objects.all().values(*headerrow):
    
        if "Branch" in headerrow:
            bds=BranchDS.objects.get(pk=student['Branch'])
            student['Branch']=str(bds)
        writer.writerow(student.values())
    response['Content-Disposition'] = 'attachment; filename="students.csv"'
    return response


def home_view(request):
    w=['enrollment_no','first_name','last_name','gender','Email','Mobile_No','School10','School12','Score10','Score12','JeePercentile',
      'Branch']
    
    w1=[]
    r=[]
    if request.method=='POST':
        form=Export(request.POST)
        if form.is_valid():
            for fields in form:
                s=form.cleaned_data[fields.html_name]
                w1.append(fields.html_name)
                print()
                if s==True:
                    r.append(fields.html_name)
                
        print(r)
        
        form=Export()
        return export(request,r)         
    else:
        form=Export()
    return render(request,'placementapp/export.html',{'form':form})
    
def exportview(request,f_id):
    if request.user.is_authenticated and request.user.verified:
        if request.user.user_type==2:
            d={1:StudentdataExportbyplacementofficer,2:PositionExportplacementofficer,3:AppliedExportplacementofficer,4:OffersExportplacementofficer,5:CompanyExportplacementofficer,6:MentorExportplacementofficer}
        if request.user.user_type==3:
            d={1:StudentdataExportbycompany,3:AppliedExportcompany}
        if request.user.user_type==4:
            d={1:StudentdataExportbymentor,3:AppliedExportmentor}
        w1=[]
        m={1:Student,2:Position,3:Applied,4:Offers,5:Company,6:Mentor}
        headerrow=[]
        if request.method=='POST':
            form=d[f_id](request.POST)
            if form.is_valid():
                for fields in form:
                    s=form.cleaned_data[fields.html_name]
                    w1.append(fields.html_name)
                    if s==True:
                        headerrow.append(fields.html_name)
                if f_id==1:
                    j={'School10':School,'School12':School,'Branch':BranchDS,'mentor':Mentor,'PlacementCell':PlacementCell} 
                    if request.user.user_type==2:
                        branchlist=[]
                        branchlist=form.cleaned_data['branchlist']
                        if branchlist is not None:
                            cusqueryset=Student.objects.filter(Branch__in=branchlist).values(*headerrow)
                        else:
                            cusqueryset=Student.objects.all().values(*headerrow)
                        print(cusqueryset)
                        
                        
                    if request.user.user_type==3:
                        cusqueryset=Student.objects.filter(AppliedPositions__Company__user=request.user).values(*headerrow)
                    if request.user.user_type==4:
                        cusqueryset=Student.objects.filter(mentor__user=request.user).values(*headerrow)
                    
                elif f_id==2:
                    j={'Company':Company}
                    if request.user.user_type==2:
                        cusqueryset=Position.objects.all().values(*headerrow)
                    
                elif f_id==3:
                    j={'Student':Student,'Position':Position,'FinalCTC': Offers}
                    if request.user.user_type==2:
                        if form.cleaned_data['Till'] is not None :
                            cusqueryset=Applied.objects.filter(Time__lte=form.cleaned_data['Till']).values(*headerrow)
                        elif form.cleaned_data['Companies'] is not None:
                            cusqueryset=Applied.objects.filter(Position__Company__in=form.cleaned_data['Companies']).values(*headerrow)
                        else:
                            cusqueryset=Applied.objects.all().values(*headerrow)
                    elif request.user.user_type==3:
                        cusqueryset=Applied.objects.filter(Position__Company__user=request.user).values(*headerrow)
                    elif request.user.user_type==4:
                        cusqueryset=Applied.objects.filter(Student__mentor=request.user).values(*headerrow)
                    
                elif f_id==4:
                    j={'Position':Position}
                    if request.user.user_type==2:
                        cusqueryset=Offers.objects.all().values(*headerrow)
                    elif request.user.user_type==3:
                        cusqueryset=Offers.objects.filter(Position__Company__user=request.user).values(*headerrow)
                    
                elif f_id==5 or f_id==6:
                    j={}

                    cusqueryset=m[id].objects.all().values(*headerrow)
                    
            form=d[f_id]()
            return export(request,headerrow,f_id,cusqueryset)         
        else:
            form=d[f_id]()
        return render(request,'placementapp/export.html',{'form':form})
    return HttpResponse("<h1>Current User Have to Verified By the PlacementOfficer or Mentor Before using this Feature</h1>")

def export(request,headerrow,id,cusqueryset):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(headerrow)
    m={1:Student,2:Position,3:Applied,4:Offers,5:Company,6:Mentor}
    if id==1:
        j={'School10':School,'School12':School,'Branch':BranchDS,'mentor':Mentor,'PlacementCell':PlacementCell} 
        
    elif id==2:
        j={'Company':Company}
        
    elif id==3:
        j={'Student':Student,'Position':Position,'FinalCTC': Offers}
        
    elif id==4:
        j={'Position':Position}
        
    elif id==5 or id==6:
        j={}
    
    for data in cusqueryset:
        for k in j:
            if k in headerrow:
                bds=j[k].objects.get(pk=data[k])
                if bds is not None:
                    data[k]=str(bds)
        writer.writerow(data.values())
    response['Content-Disposition'] = 'attachment; filename="Export.csv"'
    return response
# <script type="module">
#   // Import the functions you need from the SDKs you need
#   import { initializeApp } from "https://www.gstatic.com/firebasejs/9.4.1/firebase-app.js";
#   import { getAnalytics } from "https://www.gstatic.com/firebasejs/9.4.1/firebase-analytics.js";
#   // TODO: Add SDKs for Firebase products that you want to use
#   // https://firebase.google.com/docs/web/setup#available-libraries

#   // Your web app's Firebase configuration
#   // For Firebase JS SDK v7.20.0 and later, measurementId is optional
#   const firebaseConfig = {
#     apiKey: "AIzaSyBSuGuIEErPN0kj3Va7uvPJiJ_oBN3mYwk",
  #  'databaseURl':"https://campusplacementportal-default-rtdb.asia-southeast1.firebasedatabase.app/",
#     authDomain: "campusplacementportal.firebaseapp.com",
#     projectId: "campusplacementportal",
#     storageBucket: "campusplacementportal.appspot.com",
#     messagingSenderId: "337427571042",
#     appId: "1:337427571042:web:1a6cd408a268456c65cc3b",
#     measurementId: "G-B9XLMWY491"
#   };

#   // Initialize Firebase
#   const app = initializeApp(firebaseConfig);
#   const analytics = getAnalytics(app);
# </script>
def dashboard(request):
    if request.user.is_authenticated and request.user.user_type==1:
            
        print(f"getCtofPosApplied :{getCtofPosApplied(request)}")
        print(f"getCtofOfferInHand :{getCtofOfferInHand(request)}")
        print(f"getCtofPosSelectedIn :{getCtofPosSelectedIn(request)}")
        print(f"getCtofPosUnderEval :{getCtofPosUnderEval(request)}")
        print(f"getCtofPosRej :{getCtofPosRej(request)}")
        print(f"getCtofPosNotApplied :{getCtofPosNotApplied(request)}")
        print(f"getCtOfStuPlaced :{getCtOfStuPlaced(request)}")
        print(f"getCountOfStudentOfSameDegreeAndSameStartYear :{getCtOfStuOfDASY(request)}")
        print(f"getMaxCTCInHand :{getMaxCTCInHand(request)}")
        dict={"getCtofPosApplied" :getCtofPosApplied(request),
        "getCtofOfferInHand" :getCtofOfferInHand(request),
        "getCtofPosSelectedIn" :getCtofPosSelectedIn(request),
        "getCtofPosUnderEval" :getCtofPosUnderEval(request),
        "getCtofPosRej" :getCtofPosRej(request),
        "getCtofPosNotApplied" :getCtofPosNotApplied(request),
        "getCtOfStuPlaced" :getCtOfStuPlaced(request),
        "getCountOfStudentOfSameDegreeAndSameStartYear" :getCtOfStuOfDASY(request),
        "getMaxCTCInHand" :getMaxCTCInHand(request),
        }
    if request.user.is_authenticated and request.user.user_type==2:
            
        print(f"getCtTotlStu :{getCtTotlStu(request)}")
        print(f"getCtUnplacedStu :{getCtUnplacedStu(request)}")
        print(f"getCtCompany :{getCtCompany(request)}")
        print(f"getCtPlacedStu :{getCtPlacedStu(request)}")
        print(f"getAvgCTC :{getAvgCTC(request)}")
        print(f"getMaxCTC :{getMaxCTC(request)}")
        print(f"getCtOfUnverifiedStu :{getCtOfUnverifiedStu(request)}")
        dict={"getCtTotlStu" :getCtTotlStu(request),
        "getCtUnplacedStu" :getCtUnplacedStu(request),
        "getCtCompany" :getCtCompany(request),
        "getCtPlacedStu" :getCtPlacedStu(request),
        "getAvgCTC" :getAvgCTC(request),
        "getMaxCTC" :getMaxCTC(request),
        "getCtOfUnverifiedStu" :getCtOfUnverifiedStu(request),
        }
    if request.user.is_authenticated and request.user.user_type==3:
            
        print(f"getCtStuAppliedForComp :{getCtStuAppliedForComp(request)}")
        print(f"getCtStuSelected :{getCtStuSelected(request)}")
        print(f"getCtStuUnderEval :{getCtStuUnderEval(request)}")
        print(f"getCtStuRej :{getCtStuRej(request)}")
        print(f"getCtPosCreated :{getCtPosCreated(request)}")
        print(f"getCtOffersCreated :{getCtOffersCreated(request)}")
        print(f"getCtOfOffersAssigned :{getCtOfOffersAssigned(request)}")
        dict={"getCtStuAppliedForComp" :getCtStuAppliedForComp(request),
        "getCtStuSelected" :getCtStuSelected(request),
        "getCtStuUnderEval" :getCtStuUnderEval(request),
        "getCtStuRej" :getCtStuRej(request),
        "getCtOffersCreated" :getCtOffersCreated(request),
        "getCtPosCreated" :getCtPosCreated(request),
        "getCtOfOffersAssigned" :getCtOfOffersAssigned(request),
        }
    if request.user.is_authenticated and request.user.user_type==4:
            
        print(f"getCtStuAssigned :{getCtStuAssigned(request)}")
        print(f"getCtStuVerified :{getCtStuVerified(request)}")
        print(f"getCtUnplacedStu :{getCtUnplacedStu(request)}")
        print(f"getCtPlacedStu :{getCtPlacedStu(request)}")
        print(f"getAvgCTC :{getAvgCTC(request)}")
        dict={"getCtStuAssigned" :getCtStuAssigned(request),
        "getCtStuVerified" :getCtStuVerified(request),
        "getCtUnplacedStu" :getCtUnplacedStu(request),
        "getCtPlacedStu" :getCtPlacedStu(request),
        "getAvgCTC" :getAvgCTC(request),
        }
    return render(request,'placementapp/dashboard.html',{"data":dict})


#Student
def getCtofPosApplied(request):
    if request.user.is_authenticated and request.user.user_type==1:
        applieds=Applied.objects.filter(Student__user=request.user).count()
        return applieds
    return 0
def getCtofOfferInHand(request):
    if request.user.is_authenticated and request.user.user_type==1:
        offersInHand=Applied.objects.filter(Student__user=request.user).exclude(FinalOffer=None).count()
        return offersInHand
    return 0
def getCtofPosSelectedIn(request):
    if request.user.is_authenticated and request.user.user_type==1:
        selectedIn=Applied.objects.filter(Student__user=request.user,Status='Selected').count()
        return selectedIn
    return 0

def getCtofPosUnderEval(request):
    if request.user.is_authenticated and request.user.user_type==1:
        underEval=Applied.objects.filter(Student__user=request.user,Status='UnderEvaluation').count()
        return underEval
    return 0
    
def getCtofPosRej(request):
    if request.user.is_authenticated and request.user.user_type==1:
        rejIn=Applied.objects.filter(Student__user=request.user,Status='Rejected').count()
        return rejIn
    return 0
    
def getCtofPosNotApplied(request):
    if request.user.is_authenticated and request.user.user_type==1:
        alreadyApplied=Applied.objects.filter(Student__user=request.user,)
        alreadyAppliedPositions=[]
        alreadyAppliedOffer=[]
        Stu=Student.objects.get(user=request.user)
        
        for applied in alreadyApplied:
            alreadyAppliedPositions.append(applied.Position.id)
            
        position=Position.objects.filter(branch=Stu.Branch,visible=True).exclude(id__in=alreadyAppliedPositions).count()
        return position
    return 0
def getCtofStuAppliedForPos(request,pos_id):
    if request.user.is_authenticated and request.user.user_type==1:
        countStu=Applied.objects.filter(Position__id=pos_id).count()
        return countStu
    return 0
def getCtOfStuPlaced(request):
    if request.user.is_authenticated and request.user.user_type==1:
        Stu=Student.objects.get(user=request.user)
        CtPlacedStu=Student.objects.exclude(maxCTC=0,user__verified=False).filter(Branch__degree=Stu.Branch.degree,Branch__Start_year=Stu.Branch.Start_year).count()
        return CtPlacedStu
    return 0

    #getCountOfStudentOfSameDegreeAndSameStartYear
def getCtOfStuOfDASY(request):
    if request.user.is_authenticated and request.user.user_type==1:
        Stu=Student.objects.get(user=request.user)
        CtStu=Student.objects.exclude(user__verified=False).filter(Branch__degree=Stu.Branch.degree,Branch__Start_year=Stu.Branch.Start_year).count()
        return CtStu
    return 0
def getMaxCTCInHand(request):
    if request.user.is_authenticated and request.user.user_type==1:
        Stu=Student.objects.get(user=request.user)

        return Stu.maxCTC
    return 0
#Company
def getCtStuAppliedForComp(request):
    if request.user.is_authenticated and request.user.user_type==3:
        comp=Company.objects.get(user=request.user)
        applied=Applied.objects.filter(Position__Company=comp).count()
        return applied
    return 0
def getCtStuSelected(request):
    if request.user.is_authenticated and request.user.user_type==3:
        selectedIn=Applied.objects.filter(Position__Company__user=request.user,Status='Selected').count()
        return selectedIn
    if request.user.is_authenticated and request.user.user_type==4:
        selectedIn=Applied.objects.filter(Student__mentor__user=request.user,Status='Selected').count()
        return selectedIn
    return 0
def getCtStuUnderEval(request):
    if request.user.is_authenticated and request.user.user_type==3:
        underEval=Applied.objects.filter(Position__Company__user=request.user,Status='Under Evaluation').count()
        return underEval
    if request.user.is_authenticated and request.user.user_type==4:
        underEval=Applied.objects.filter(Student__mentor__user=request.user,Status='Under Evaluation').count()
        return underEval
    return 0
def getCtStuRej(request):
    if request.user.is_authenticated and request.user.user_type==3:
        rejIn=Applied.objects.filter(Position__Company__user=request.user,Status='Rejected').count()
        return rejIn
    if request.user.is_authenticated and request.user.user_type==4:
        rejIn=Applied.objects.filter(Student__mentor__user=request.user,Status='Rejected').count()
        return rejIn
    return 0
def getCtPosCreated(request):
    if request.user.is_authenticated and request.user.user_type==3:
        CtPos=Position.objects.filter(Company__user=request.user).count()
        return CtPos
    return 0
def getCtOffersCreated(request):
    if request.user.is_authenticated and request.user.user_type==3:
        CtOffer=Offers.objects.filter(Position__Company__user=request.user).count()
        return CtOffer
    return 0
def getCtOfOffersAssigned(request):
    if request.user.is_authenticated and request.user.user_type==3:
        CtOffers=Applied.objects.filter(Position__Company__user=request.user,FinalOffer__Position__Company__user=request.user).count()
        return CtOffers
    return 0
#PlacementOff
def getCtTotlStu(request):
    if request.user.is_authenticated and request.user.user_type==2:
        totalStu=0
        
        x = datetime.now()

        totalStuCurrYr=Student.objects.filter(user__verified=True,Branch__Start_year=x.year-3).count()
        totalStuPrevYr=Student.objects.filter(user__verified=True,Branch__Start_year=x.year-4).count()
        totalStu=Student.objects.filter(user__verified=True).count()
        totalStuDict={"totalStuCurrYr":totalStuCurrYr,
        "totalStuPrevYr":totalStuPrevYr,
        "totalStu":totalStu,
        }
        return totalStu
    return 0
def getCtUnplacedStu(request):
    if request.user.is_authenticated and request.user.user_type==2: 
        x = datetime.now()   
        unplacedStu=Student.objects.filter(user__verified=True,Branch__Start_year=x.year-3,maxCTC=0).count()
        return unplacedStu
    
    if request.user.is_authenticated and request.user.user_type==4: 
        CtStu=Student.objects.filter(mentor__user=request.user,maxCTC=0).count()
        return CtStu
    return 0
def getCtCompany(request):
    if request.user.is_authenticated and request.user.user_type==2: 
        CtComp=Company.objects.all().count()
        return CtComp
    return 0

def getCtPlacedStu(request):
    if request.user.is_authenticated and request.user.user_type==2: 
        x = datetime.now()   
        placedStu=Student.objects.filter(user__verified=True,Branch__Start_year=x.year-3).exclude(maxCTC=0).count()
        return placedStu
    if request.user.is_authenticated and request.user.user_type==4: 
        CtStu=Student.objects.filter(user__verified=True,mentor__user=request.user).exclude(maxCTC=0).count()
        return CtStu
    
    return 0
def getAvgCTC(request):
    if request.user.is_authenticated and request.user.user_type==2: 
        x = datetime.now()   
        avgCTC=Student.objects.filter(user__verified=True,Branch__Start_year=x.year-3).exclude(maxCTC=0).aggregate(average_CTC=Avg('maxCTC'))
        if avgCTC['average_CTC'] is not None:
            return avgCTC['average_CTC']
    if request.user.is_authenticated and request.user.user_type==4: 
        
        avgCTC=Student.objects.filter(user__verified=True,mentor__user=request.user).exclude(maxCTC=0).aggregate(average_CTC=Avg('maxCTC'))
        if avgCTC['average_CTC'] is not None:
            return avgCTC['average_CTC']
    return 0
def getMaxCTC(request):
    if request.user.is_authenticated and request.user.user_type==2: 
        x = datetime.now()   
        maxCTC=Student.objects.filter(user__verified=True,Branch__Start_year=x.year-3).aggregate(max_CTC=Max('maxCTC'))
        return maxCTC['max_CTC']
    return 0
def getCtOfUnverifiedStu(request):
    if request.user.is_authenticated and request.user.user_type==2: 
        CtUnverified=User.objects.filter(user_type=1,verified=False).count()
        return CtUnverified
    return 0
#Mentor
def getCtStuAssigned(request):
    if request.user.is_authenticated and request.user.user_type==4: 
        CtStu=Student.objects.filter(mentor__user=request.user).count()
        return CtStu
    return 0
def getCtStuVerified(request):
    if request.user.is_authenticated and request.user.user_type==4: 
        CtStu=Student.objects.filter(mentor__user=request.user,user__verified=True).count()
        return CtStu
    return 0


