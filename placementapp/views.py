from django.conf.urls import include
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import query
from django.shortcuts import redirect, render,HttpResponse,redirect,get_object_or_404,HttpResponseRedirect
from .forms import *
from django.contrib import messages
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required
from .models import *
#from django.forms import modelform_factory
from django.forms import modelformset_factory
import csv
# Create your views here.
def userlogin(request):
    if request.user.is_authenticated:
        return HttpResponse('<h1> Current Session User is already Authenticated </h1>') 
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
def anu(request):
    pass

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
                form=StudentSignUpForm()
                #return render(request,'placementapp/signup.html',{'form':form})
        else:
            form=StudentSignUpForm()
        return render(request,'placementapp/Student/signup.html',{'form':form})
    
def CompanySignUp(request):
    if request.user.user_type==2 and request.user.verified:
        if request.method=='POST':
            form=CompanySignUpForm(request.POST)
            if form.is_valid():
                form.save()
                form=CompanySignUpForm()
                #return render(request,'placementapp/signup.html',{'form':form})
        else:
            form=CompanySignUpForm()
        return render(request,'placementapp/Company/signup.html',{'form':form})
    return HttpResponse('<h1> Current User is not Authorised </h1>')

def MentorSignUp(request):
    if request.user.user_type==2 and request.user.verified:
        if request.method=='POST':
            form=MentorSignUpForm(request.POST)
            if form.is_valid():
                form.save()
                form=MentorSignUpForm()
                #return render(request,'placementapp/signup.html',{'form':form})
        else:
            form=MentorSignUpForm()
        return render(request,'placementapp/Mentor/signup.html',{'form':form})
    return HttpResponse('<h1> Current User is not Authorised </h1>')

def PlacementOfficerSignUp(request):
    if request.user.user_type==2 and request.user.verified:
        if request.method=='POST':
            form=PlacementOfficerSignUpForm(request.POST)
            if form.is_valid():
                form.save()
                form=PlacementOfficerSignUpForm()
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
        Stu=Student.objects.get(user=request.user)
        for applied in alreadyApplied:
            alreadyAppliedPositions.append(applied.Position.id)
        position=Position.objects.filter(branch=Stu.Branch).exclude(id__in=alreadyAppliedPositions)
        return render(request,'placementapp/Student/PositionApply.html',{'Positions':position})
    return HttpResponse('<h1> Current User is not A Student or  verified </h1>')

def applyForPosition(request,id):
    varuser=request.user
    if request.method=='POST' and varuser.is_authenticated and varuser.user_type==1 :
        Stu=Student.objects.get(user=varuser)
        pos=Position.objects.get(pk=id)
        #branchds=pos.branch
        #if stu.branch in branchds:
        if pos.minScore10<=Stu.Score10 and pos.minScore12<=Stu.Score12 and pos.minJeePercentile<=Stu.JeePercentile :
            Applied.objects.create(Position=pos,Student=Stu)
            print(f'{Stu} {pos}')
            return HttpResponseRedirect('/ApplyPosition')
        else:
            return HttpResponse('<h1> Not Eligible For Position </h1>')
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
            if request.method=='POST':
                form=StudentForm(request.POST,instance=stu)
                if form.is_valid():
                    form.save()
            else:
                form=StudentForm(instance=stu)
            return render(request,'placementapp/Student/UpdateProfile.html',{'form':form})
        else:
            return HttpResponse('<h1> Current User is not of A Student </h1>')
    else:
        return HttpResponse('<h1> Current Session User Not Authenticated </h1>') 

def dashboard(request):
    return render(request,'placementapp/dashboard.html')


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
            applied=Applied.objects.all().order_by('Time')
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
 
    if request.method == 'POST':
        applied.delete()
        return redirect('/')
    else:
        return render(request, 'placementapp/PlacementOff/deleteapplied.html')
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
        applied=Applied.objects.filter(Student__user=varuser,Status='Selected')
        if applied is None:
            return HttpResponse('<h1>No Offers </h1>')
        return render(request,'placementapp/Offers.html',{'dataset':applied})
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
                form =PositionForm(request.POST, instance =old_data)
                if form.is_valid():
                    form.save()
                    return redirect(f'/Position/update/{_id}')
            else:
                form = PositionForm(instance = old_data)
                context ={
                    'form':form
                }
                return render(request,'placementapp/PlacementOff/updateposition.html',context)
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
                return redirect('/')
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
                return redirect('/')
        else:
            form=OfferForm(request.user)
            return render(request,'placementapp/Company/CreateOffer.html',{'form':form})    
    return redirect('/')    

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
                    data=None
            except Exception:
                raise Http404('Does Not Exist')
        
            if request.method == 'POST':
                data.delete()
                return redirect('/')
            else:
                return render(request, 'placementapp/Company/deleteOffer.html')
        elif request.user.user_type==2:
            try:
                data = get_object_or_404(Offers,id=id)
                
                
            except Exception:
                raise Http404('Does Not Exist')
        
            if request.method == 'POST':
                data.delete()
                return redirect('/')
            else:
                return render(request, 'placementapp/PlacementOff/deleteOffer.html')
    return HttpResponse('<h1> Current Session User is not  Authorised</h1>') 


def ListOffer(request):
    if request.user.is_authenticated and request.user.verified:
        if request.user.user_type==1:
            Stu=Student.objects.get(user=request.user)
            offers=Offers.objects.filter(Student=Stu).order_by('FinalCTC')
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
                    return redirect(f'/Company/update/{id}')
            else:
                form = AppliedForm(instance = company)
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
                return redirect('/')
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
                #formset=BaseAppliedFormSet,
                #form=MyAppliedForm,
            )
            if request.method=='POST':
                formset=AppliedForm(
                request.POST,
                queryset=Applied.objects.filter(Position__Company=comp,Status='Selected'),
                #form_kwargs={'user': request.user},
                #user=request.user,
                )
                if formset.is_valid():
                    v=formset.save()
            if request.method=='GET':
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
            fields=['verified','username'],
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
    
