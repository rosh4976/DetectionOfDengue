from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect


# Create your views here.
from myapp.models import Complaint, Logs, Users, Review


def login_get(request):
    return render(request,'loginindex.html')

def login_post(request):
    username=request.POST['username']
    password= request.POST['password']
    user=authenticate(request,username=username,password=password)
    if user is not None:
        login(request,user)
        if user.groups.filter(name="admin"):
            return redirect("/myapp/adminhome/")
        else:
            messages.error(request, "group not found")
            return redirect("/myapp/login_get/")
    else:
        messages.error(request, "invalid credentials")
        return redirect("/myapp/login_get/")

def forgotpassword_get(request):
    return render(request,'forgotpassword.html')
def forgotpassword_post(request):
    return

# A D M I N ---------------------


def adminhome(request):
    return render(request,'adminpages/adminhomeindex.html')


def changepassword_get(request):
    return render(request,'adminpages/changepassword.html')

def changepassword_post(request):
    currentpassword=request.POST['currentpassword']
    newpassword=request.POST['newpassword']
    conpassword=request.POST['conpassword']
    data=request.user
    if not data.check_password(currentpassword):
        messages.error(request,"invalid password")
        return redirect("/myapp/changepassword_get/")

    if newpassword!=conpassword:
        messages.error(request,"newpassword and conpassword should be same")
        return redirect("/myapp/changepassword_get/")
    data.set_password(newpassword)
    data.save()
    return redirect("/myapp/login_get/")








def sentreply_get(request):
    return render(request,'adminpages/sentreply.html')

def sentreply_post(request):
    return

def viewblockedusers_get(request):
    return render(request,'adminpages/viewblockedusers.html')

def viewcomplaint_get(request):
    data=Complaint.objects.all()
    return render(request,'adminpages/viewcomplaint.html',{'data':data})


def review_get(request):
    data=Review.objects.all()
    return render(request,'adminpages/review.html',{'data':data})

def viewlogs_get(request):
    data=Logs.objects.all()
    return render(request,'adminpages/viewlogs.html',{'data':data})

def viewuser_get(request):
    data=Users.objects.all()
    return render(request,'adminpages/viewuser.html',{'data':data})

# U S E R S -----------------------



def edit_get(request):
    return render(request,'users/edit.html')
def edit_post(request):
    return


def register_get(request):
    return render(request,'users/Register.html')
def register_post(request):
    return

def sentcomplaint_get(request):
    return render(request,'users/sentcomplaint.html')
def sentcomplaint_post(request):
    return

def viewprofile_get(request):
    return render(request,'users/viewprofile.html')

def viewreply_get(request):
    return render(request,'users/viewreply.html')



