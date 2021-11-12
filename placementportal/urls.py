"""placementportal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.urls import path
from placementapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Student Sign-Up Page
    path('stusignup/',views.Stusignup ,name='usersignup'),
    # Placement Officer Sign-Up Page
    path('ploffsignup',views.PlacementOfficerSignUp),
    # Mentor Sign-Up Page
    path('mentorsignup',views.MentorSignUp),
    # Company Sign-Up Page
    path('companysignup',views.CompanySignUp),

    path("login",views.userlogin,name="userlogin"),
    path("logout",views.userlogout,name="logout"),
    # Update Student Profile Form 
    path('UpdateProfile/',views.StudentUpdateProfile,name="UpdateProfile"),
    #Student Dashboard
    path('Dashboard/',views.dashboard,name='Dashboard'),
    #For Students return all the available positions
    #For Campany return Position Associated with the company
    #For PlacementOffi return all positions 
    path('Position',views.ListPositionView),
    #path('Positions/Company/<int:id>',views.),
    path('Position/create',views.createPosition),
    path('Position/update/<int:_id>',views.UpdatePosition),
    path('Position/delete/<int:_id>',views.DeletePosition),

    path('AppliedPosition',views.ListOfAppliedPositions),

    path("Offers",views.OfferStudentView),
    path('Offer',views.ListOffer),
    path('Offer/create',views.CreateOffer),
    path('Offer/update/<int:id>/',views.UpdateOffer),
    path('Offer/delete/<int:id>',views.DeleteOffer),
    
    path('ApplyPosition',views.applyView),
    path('apply/<int:id>/',views.applyForPosition,name="applypos"),

    path('assignoffer',views.AssignOffer),
    path('Students',views.ListOfStudentCompany),
    path('Students/<int:id>',views.StudentDetailView,name='StuDetail'),
    path('AssignMentor',views.AddStudentMentor),
    path('verifyStu',views.VerifyStudentView),
    path('StudentList',views.ListStudentView),
]
