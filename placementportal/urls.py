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
    path('signup/',views.signup ),
    path('studUpdate/',views.StudentUpdate,name="StudUpdate"),
    url(r"^accounts/",include("django.contrib.auth.urls")),
    #url(r"^dashboard/",views.studentdashboard,name="dashboard"),
    path('dashboard/',views.studentdashboard,name='dashboard'),
    path("login",views.userlogin,name="login"),
    path("logout",views.userlogout,name="logout"),
    path('Position',views.ListPosition),
    path('createposition',views.createPosition),
    path('Position/update/<int:_id>',views.UpdatePosition),
    path('Position/delete/<int:_id>',views.DeletePosition),
    path('Applied',views.updatestudentstatus),
    path('Offer/create',views.CreateOffer),
    
]
