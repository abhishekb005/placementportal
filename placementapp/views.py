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
                    #messages.info(request,f"You are not logged in as {username}")
                    return render(request,'placementapp/dashboard.html',{'user':varuser})
                else:
                    messages.error(request,f"InValid")
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

def applyView(request):
    position=Position.objects.all()
    return render(request,'placementapp/PositionApply.html',{'Positions':position})
    
def applyForPosition(request,id):
    varuser=request.user
    if request.method=='POST' and varuser.is_authenticated and varuser.user_type==1 :
        Stu=Student.objects.get(user=varuser)
        pos=Position.objects.get(pk=id)
        if pos.minScore10<=Stu.Score10 and pos.minScore12<=Stu.Score12 and pos.minJeePercentile<=Stu.JeePercentile :
            Applied.objects.create(Position=pos,Student=Stu)
            print(f'{Stu} {pos}')
            return HttpResponseRedirect('/ApplyPosition')
        else:
            print("Not Eligible for the Position")
    else:
        print(' Student not varified ')

def StudentList(request):
    varuser=request.user
    if varuser.user_type==4:
        mentr=Mentor.objects.get(user=varuser)
        Stu=Student.objects.filter(mentor=mentr)
        return Stu

def VerifyStudent(request):
    varuser=request.user
    Stu=None
    if varuser.user_type==4:
        Stu=Student.objects.filter(mentor__user=varuser)
    return Stu
def StudentUpdate(request):
    if request.user.is_authenticated:
        if request.user.user_type==1:
            stu=Student.objects.get(user=request.user)
            if request.method=='POST':
                form=StudentForm(request.POST,instance=stu)
                if form.is_valid():
                    form.save()
            else:
                form=StudentForm(instance=stu)
            return render(request,'placementapp/testform.html',{'form':form})

def studentdashboard(request):
    return render(request,'placementapp/dashboard.html')
def companydashboard(request):
    pass
def placementoffdashboard(request):
    pass
def mentordashboard(request):
    pass

def getallPosition(request):
    if request.user.is_authenticated and request.user.user_type==1 and request.user.verified:
        Stu=Student.objects.get(user=request.user)
        if(request.user.verified):
            positions=Position.objects.filter(branch=Stu.Branch)
        else:
            positions=None
    elif request.user.is_authenticated and request.user.user_type==3 and request.user.verified:
        Comp=Company.objects.get(user=request.user)
        positions=Position.objects.filter(Company=Comp)
    elif request.user.is_authenticated and request.user.user_type==2 and request.user.verified:
        positions=Position.objects.all().order_by('branch__Start_year')
    else:
        positions=None
    return positions
        
def getallOffers(request):
    if request.user.is_authenticated and request.user.verified:
        if request.user.user_type==1:
            Stu=Student.objects.get(user=request.user)
            offers=Offers.objects.filter(Student=Stu).order_by('FinalCTC')
        if request.user.user_type==3:
            comp=Company.objects.get(user=request.user)
            #positions=Position.objects.filter(Company=comp)
            offers=Offers.objects.filter(Position__Company=comp)
        else:
            offers=None
    else:
        offers=None
    return offers

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

#Create Forms For Below functionalities-
    # send Msg from PlacementOfficer to Company
    # send Msg from PlacementOfficer to Student
    # send Msg from Company to PlacementOfficer  
    # Update Student Details based on Model
    # Update Mentor Detail 
    # Update Company Detail 

# For Company 
# Create New Position -Create A Form and then save it 
# Update Existing Position -Create A form and save the existing Position
# Delete Existing Positions
# Get all student who applied for a particular position and are eligible and not rejected before
def getStudentApplied(request):
    varuser=request.user
    applied=None
    if varuser.is_authenticated and varuser.verified :
        if varuser.user_type==3:
            comp=Company.objects.get(user=varuser)
            applied=Applied.objects.filter(Position__Company=comp)
            return applied
        elif varuser.user_type==1:
            stu=Student.objects.get(user=varuser)
            applied=Applied.objects.filter(Student=stu)
        elif varuser.user_type==2:
            applied=Applied.objects.all().order_by('Time')
        return applied
    return applied
#Update status of Students who are eligible for next round
# Create New Offer for Particular Position -Create A form then save
# Update Existing Offer
#  
# Delete Offer
def deleteOffer(request,id):
    offer=Offers.objects.get(pk=id)
    offer.delete()
    return None
#Update or assign Offer to those Student who applied for the position and got selected
#NEw

def StudentDetail(request,id):
    varuser=request.user
    if varuser.user_type==4:
        StuUser=User.objects.get(pk=id)
        Stu=None
        if StuUser.user_type==1:
            Stu=Student.objects.get(user=StuUser)
        
        if Stu is None:
            return None
        else:
            return Stu
    if varuser.user_type==3:
        StuUser=User.objects.get(pk=id)
        Stu=None
        applied=None
        if StuUser.user_type==1:
            Stu=Student.objects.get(user=StuUser)
            comp=Company.objects.get(user=varuser)
            applied=Applied.objects.filter(Student=Stu,Position__Company=comp)
        if applied is not None:
            return Stu
        return None
    return None

def StudentDetailView(request,id):
    Stu=StudentDetail(request,id)
    return render(request,'placementapp/StudentDetail.html',{'dataset': Stu})


def createPosition(request):
    if request.method=='POST' and request.user.user_type==3 :
        comp=Company.objects.get(user=request.user)
        form=PositionForm(request.POST)
        if form.is_valid():
            pos=form.save(commit=False)
            pos.Company=comp
            pos.save()
            return redirect('/dashboard')
    else:
        form=PositionForm()
        return render(request,'placementapp/createposition.html',{'form':form})
    return render(request,'placementapp/createposition.html',{'form':form})
    
def UpdatePosition(request,_id):
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
        return render(request,'placementapp/createposition.html',context)

def DeletePosition(request,_id):
    try:
        data = get_object_or_404(Position,id =_id)
    except Exception:
        raise Http404('Does Not Exist')
 
    if request.method == 'POST':
        data.delete()
        return redirect('/')
    else:
        return render(request, 'placementapp/deleteposition.html')

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
            return render(request,'placementapp/createposition.html',{'form':form})    
    return redirect('/')    

def UpdateOffer(request,id):
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
        return render(request,'placementapp/createposition.html',context)

def DeleteOffer(request,id):
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
        return render(request, 'placementapp/deleteposition.html')

def ListOffer(request):
    offer=getallOffers(request)
    return render(request,'placementapp/position.html',{'dataset':offer})

def ListPosition(request):
    position=getallPosition(request)
    return render(request, 'placementapp/position.html',{'dataset':position})

def updatestudentstatus(request):
    stu=Applied.objects.all()

    return render(request,'placementapp/appliedStu.html',{'dataset':stu})

def ListOfAppliedStudent(request):
    pass

def AssignOffer(request):
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
        queryset=Applied.objects.filter(Position__Company=comp),
        #form_kwargs={'user': request.user},
        user=request.user,
        )
        if formset.is_valid():
            v=formset.save()
    if request.method=='GET':
        formset=AppliedForm(
            queryset=Applied.objects.filter(Position__Company=comp)
          #form_kwargs={'user': request.user},
          #user=request.user,
            )
    for form in formset:
        form.fields['Position'].queryset=Position.objects.filter(Company=comp)
        form.fields['Student'].queryset=Student.objects.filter(AppliedPositions__Company=comp)
        form.fields['FinalOffer'].queryset=Offers.objects.filter(Position__Company=comp)
    return render(request,'placementapp/assignOffer.html',{'formset':formset})

def ListStudentCompany(request):
    applied=getStudentApplied(request)
    return render(request,'placementapp/position.html',{'dataset':applied})

def AddStudentMentor(request):
    varuser=request.user
    if varuser.is_authenticated and varuser.user_type==4 and varuser.verified:
    #if varuser.is_authenticated:
        Mentorr=Mentor.objects.get(user=varuser)
        StudentMentorForm=modelformset_factory(
            Student,
            fields=['enrollment_no',],
            extra=18,
            max_num=20,
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
                for obj in v:
                    StuUser=User.objects.get(username=obj.enrollment_no)
                    Stu=Student.objects.get(enrollment_no=obj.enrollment_no)
                    Stu.mentor=Mentorr
                    Stu.save()
                    print(Stu)
                
        if request.method=='GET':
            formset=StudentMentorForm(
                queryset=Student.objects.filter(mentor__user=varuser),
                #form_kwargs={'user': request.user},
                #user=request.user,
                )
        # for form in formset:
        #     form.fields['Position'].queryset=Position.objects.filter(Company=comp)
        #     form.fields['Student'].queryset=Student.objects.filter(AppliedPositions__Company=comp)
        #     form.fields['FinalOffer'].queryset=Offers.objects.filter(Position__Company=comp)
    return render(request,'placementapp/assignOffer.html',{'formset':formset})

def VerifyStudentView(request):
    varuser=request.user
    if varuser.is_authenticated and varuser.user_type==4 or varuser.user_type==2 and varuser.verified:
    #if varuser.is_authenticated:
        #Mentorr=Mentor.objects.get(user=varuser)
        if varuser.user_type==4:
            Stu=Student.objects.filter(mentor__user=varuser)
        elif varuser.user_type==2:
            Stu=Student.objects.filter(verified=False)
        userr=[]
        for student in Stu:
            userr.append(student.user.id)
        StudentMentorForm=modelformset_factory(
            User,
            fields=['verified','username'],
            extra=0,
            max_num=20,
        #formset=BaseAppliedFormSet,
        #form=MyAppliedForm,
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
                
        if request.method=='GET':
            formset=StudentMentorForm(
                queryset=User.objects.filter(id__in=userr),
                #form_kwargs={'user': request.user},
                #user=request.user,
                )
        # for form in formset:
        #     form.fields['Position'].queryset=Position.objects.filter(Company=comp)
        #     form.fields['Student'].queryset=Student.objects.filter(AppliedPositions__Company=comp)
        #     form.fields['FinalOffer'].queryset=Offers.objects.filter(Position__Company=comp)
    return render(request,'placementapp/assignOffer.html',{'formset':formset})
