from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group

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
        elif user.groups.filter(name="user"):
            return redirect("/myapp/userhome_get/")
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


def logout_get(request):
    # logout(request.user)
    return redirect("/myapp/login_get/")

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








def sentreply_get(request,id):
    return render(request,'adminpages/sentreply.html',{'id':id})

def sentreply_post(request):
    reply=request.POST['reply']
    id=request.POST['id']
    data = Complaint.objects.get(id=id)
    data.reply=reply
    data.status='replied'
    data.save()
    return redirect("/myapp/viewcomplaint_get/")


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
    data=Users.objects.filter(status='pending')
    return render(request,'adminpages/viewuser.html',{'data':data})

def blockusers_get(request,id):
    Users.objects.filter(id=id).update(status='Blocked')
    return redirect('/myapp/viewuser_get/#a')


def viewblockedusers_get(request):
    data = Users.objects.filter(status='Blocked')
    return render(request,'adminpages/viewblockedusers.html',{'data':data})

def unblockuser_get(request,id):
    Users.objects.filter(id=id).update(status='pending')
    return redirect('/myapp/viewuser_get/#a')



# U S E R S -----------------------



def edit_get(request):
    u = Users.objects.get(AUTHUSER=request.user)

    return render(request,'users/edit.html',{'data':u})



def edit_post(request):
    name = request.POST['name']
    gender = request.POST['gender']
    dob = request.POST['dob']
    phone = request.POST['phone']
    email = request.POST['email']
    place = request.POST['place']

    u = Users.objects.get(AUTHUSER=request.user)

    u.name = name
    u.dob = dob
    u.email = email
    u.phone = phone
    u.gender = gender
    u.place = place
    u.save()

    messages.success(request, 'Edited successfully')
    return redirect("/myapp/viewprofile_get/")


def register_get(request):
    return render(request,'users/Register.html')
def register_post(request):
    name=request.POST['name']
    gender=request.POST['gender']
    dob=request.POST['dob']
    phone=request.POST['phone']
    email=request.POST['email']
    place=request.POST['place']
    password=request.POST['password']
    conpassword=request.POST['confirmpassword']

    if password==conpassword:
        a=User.objects.create_user(username=email,password=conpassword)
        a.groups.add(Group.objects.get(name='user'))
        a.save()

        u=Users()
        u.name=name
        u.dob=dob
        u.email=email
        u.phone=phone
        u.gender=gender
        u.place=place
        u.status='pending'
        u.AUTHUSER=a
        u.save()

        messages.success(request,'Registered successfully')
        return redirect("/myapp/login_get/")
    else:
        messages.error(request, 'Password does not match')
        return redirect("/myapp/register_get/")


def sentcomplaint_get(request):
    return render(request,'users/sentcomplaint.html')
def sentcomplaint_post(request):
    complaint=request.POST['complaint']
    data=Complaint()
    data.reply='pending'
    data.status='pending'
    data.complaint=complaint
    data.date=datetime.now().date()
    data.USER=Users.objects.get(AUTHUSER=request.user)
    data.save()
    return redirect("/myapp/viewreply_get/")

def viewprofile_get(request):
    data=Users.objects.get(AUTHUSER_id=request.user.id)
    return render(request,'users/viewprofile.html',{'data':data})

def viewreply_get(request):
    a=Complaint.objects.filter(USERS__AUTHUSER=request.user)
    return render(request,'users/viewreply.html',{'data':a})


def userhome_get(request):
    return render(request,'users/userhomeindex.html')

def userviewlogs_get(request):
    data=Logs.objects.filter(USER__AUTHUSER=request.user)
    return render(request,'users/logs.html',{'data':data})
def sendreview_get(request):
    return render(request, 'users/sendreview.html')
def sendreview_post(request):
    review = request.POST['review']
    rating= request.POST['rating']

    data = Review()
    data.rating = rating
    data.review = review
    data.date = datetime.now().date()
    data.USER = Users.objects.get(AUTHUSER=request.user)
    data.save()
    return redirect("/myapp/userhome_get/")





