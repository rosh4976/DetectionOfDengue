from datetime import datetime, timezone

import pandas as pd
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group

# Create your views here.
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

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
    data.USERS=Users.objects.get(AUTHUSER=request.user)
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




# Random forest

def dataset_get(request):
    return render(request,'users/dataset.html')



def dataset_post(request):

    from django.shortcuts import render
    import pandas as pd
    from sklearn.preprocessing import LabelEncoder
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split

    if request.method == "POST":

        Gender = request.POST['gender']
        Age = int(request.POST['age'])
        NS1 = int(request.POST['ns1'])
        IgG = int(request.POST['igg'])
        IgM = int(request.POST['igm'])
        Area = request.POST['area']
        AreaType = request.POST['areatype']
        HouseType = request.POST['housetype']
        District = request.POST['district']

        data = pd.read_csv("C:\\Users\\rmurs\\PycharmProjects\\detection_of_dengue\\myapp\\datasetdengue.csv")

        label_encoders = {}
        for column in data.columns:
            if data[column].dtype == 'object':
                le = LabelEncoder()
                data[column] = le.fit_transform(data[column])
                label_encoders[column] = le

        X = data.drop("Outcome", axis=1)
        y = data["Outcome"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        new_patient = pd.DataFrame([{
            'Gender': Gender,
            'Age': Age,
            'NS1': NS1,
            'IgG': IgG,
            'IgM': IgM,
            'Area': Area,
            'AreaType': AreaType,
            'HouseType': HouseType,
            'District': District
        }])

        for column in new_patient.columns:
            if column in label_encoders:
                new_patient[column] = label_encoders[column].transform(new_patient[column])

        prediction = model.predict(new_patient)

        if prediction[0] == 1:
            result = "Dengue Positive"

            from django.utils import timezone
            resultlog=Logs()
            resultlog.date = datetime.now().date()
            resultlog.time = datetime.now().time()
            resultlog.result=result
            resultlog.USER=Users.objects.get(AUTHUSER_id=request.user.id)
            resultlog.save()



        else:
            result = "Dengue Negative"
            from django.utils import timezone
            resultlog = Logs()
            resultlog.date = datetime.now().date()
            resultlog.time = datetime.now().time()
            resultlog.result = result
            resultlog.USER = Users.objects.get(AUTHUSER_id=request.user.id)
            resultlog.save()

        return render(request, "users/dataset.html", {"result": result})

    return render(request, "users/dataset.html")



#Linear regression
def LRpred_get(request):
    return render(request,'users/LRpred.html')

def LRpred_post(request):

    if request.method == "POST":

        Gender = request.POST['gender']
        Age = int(request.POST['age'])
        NS1 = int(request.POST['ns1'])
        IgG = int(request.POST['igg'])
        IgM = int(request.POST['igm'])
        Area = request.POST['area']
        AreaType = request.POST['areatype']
        HouseType = request.POST['housetype']
        District = request.POST['district']

        data = pd.read_csv("C:\\Users\\rmurs\\PycharmProjects\\detection_of_dengue\\myapp\\datasetdengue.csv")

        label_encoders = {}
        for column in data.columns:
            if data[column].dtype == 'object':
                le = LabelEncoder()
                data[column] = le.fit_transform(data[column])
                label_encoders[column] = le

        X = data.drop("Outcome", axis=1)
        y = data["Outcome"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        from sklearn.linear_model import LogisticRegression
        model = LogisticRegression(max_iter=1000)
        model.fit(X_train, y_train)

        new_patient = pd.DataFrame([{
            'Gender': Gender,
            'Age': Age,
            'NS1': NS1,
            'IgG': IgG,
            'IgM': IgM,
            'Area': Area,
            'AreaType': AreaType,
            'HouseType': HouseType,
            'District': District
        }])

        for column in new_patient.columns:
            if column in label_encoders:
                new_patient[column] = label_encoders[column].transform(new_patient[column])

        prediction = model.predict(new_patient)

        if prediction[0] == 1:
            result = "Dengue Positive"
        else:
            result = "Dengue Negative"

        from django.utils import timezone

        resultlog = Logs()
        resultlog.date = timezone.now().date()
        resultlog.time = timezone.now().time()
        resultlog.result = result
        resultlog.USER = Users.objects.get(AUTHUSER_id=request.user.id)
        resultlog.save()

        return render(request, "users/LRpred.html", {"result": result})


    #SVM
def SVMpred_get(request):
    return render(request, 'users/SVMpred.html')

def SVMpred_post(request):

    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import LabelEncoder
    from sklearn.svm import SVC
    from django.utils import timezone
    from datetime import datetime

    if request.method == "POST":

        Gender = request.POST['gender']
        Age = int(request.POST['age'])
        NS1 = int(request.POST['ns1'])
        IgG = int(request.POST['igg'])
        IgM = int(request.POST['igm'])
        Area = request.POST['area']
        AreaType = request.POST['areatype']
        HouseType = request.POST['housetype']
        District = request.POST['district']

        data = pd.read_csv("C:\\Users\\rmurs\\PycharmProjects\\detection_of_dengue\\myapp\\datasetdengue.csv")




        label_encoders = {}
        for column in data.columns:
            if data[column].dtype == 'object':
                le = LabelEncoder()
                data[column] = le.fit_transform(data[column])
                label_encoders[column] = le

        X = data.drop("Outcome", axis=1)
        y = data["Outcome"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # SVM Model
        model = SVC(kernel='rbf', C=1.0, gamma='scale')
        model.fit(X_train, y_train)

        new_patient = pd.DataFrame([{
            'Gender': Gender,
            'Age': Age,
            'NS1': NS1,
            'IgG': IgG,
            'IgM': IgM,
            'Area': Area,
            'AreaType': AreaType,
            'HouseType': HouseType,
            'District': District
        }])

        for column in new_patient.columns:
            if column in label_encoders:
                new_patient[column] = label_encoders[column].transform(new_patient[column])

        prediction = model.predict(new_patient)

        if prediction[0] == 1:
            result = "Dengue Positive"
        else:
            result = "Dengue Negative"

        resultlog = Logs()
        resultlog.date = timezone.now().date()
        resultlog.time = timezone.now().time()
        resultlog.result = result
        resultlog.USER = Users.objects.get(AUTHUSER_id=request.user.id)
        resultlog.save()

        return render(request, "users/SVMpred.html", {"result": result})



    #Decision Tree
def DTpred_get(request):
    return render(request, 'users/DTpred.html')

def DTpred_post(request):

    if request.method == "POST":


        import pandas as pd
        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import LabelEncoder
        from sklearn.tree import DecisionTreeClassifier
        from django.utils import timezone

        Gender = request.POST['gender']
        Age = int(request.POST['age'])
        NS1 = int(request.POST['ns1'])
        IgG = int(request.POST['igg'])
        IgM = int(request.POST['igm'])
        Area = request.POST['area']
        AreaType = request.POST['areatype']
        HouseType = request.POST['housetype']
        District = request.POST['district']



        data = pd.read_csv("C:\\Users\\rmurs\\PycharmProjects\\detection_of_dengue\\myapp\\datasetdengue.csv")

        label_encoders = {}
        for column in data.columns:
            if data[column].dtype == 'object':
                le = LabelEncoder()
                data[column] = le.fit_transform(data[column])
                label_encoders[column] = le

        X = data.drop("Outcome", axis=1)
        y = data["Outcome"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Decision Tree Model
        model = DecisionTreeClassifier(
            criterion='gini',  # or 'entropy'
            max_depth=5,  # prevent overfitting
            random_state=42
        )

        model.fit(X_train, y_train)

        new_patient = pd.DataFrame([{
            'Gender': Gender,
            'Age': Age,
            'NS1': NS1,
            'IgG': IgG,
            'IgM': IgM,
            'Area': Area,
            'AreaType': AreaType,
            'HouseType': HouseType,
            'District': District
        }])

        for column in new_patient.columns:
            if column in label_encoders:
                new_patient[column] = label_encoders[column].transform(new_patient[column])

        prediction = model.predict(new_patient)

        if prediction[0] == 1:
            result = "Dengue Positive"
        else:
            result = "Dengue Negative"

        resultlog = Logs()
        resultlog.date = timezone.now().date()
        resultlog.time = timezone.now().time()
        resultlog.result = result
        resultlog.USER = Users.objects.get(AUTHUSER_id=request.user.id)
        resultlog.save()

        return render(request, "users/DTpred.html", {"result": result})


##XG Boost



def XGpred_get(request):
    return render(request, 'users/XGpred.html')


def XGpred_post(request):
    if request.method == "POST":

        import pandas as pd
        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import LabelEncoder
        from sklearn.ensemble import GradientBoostingClassifier
        from django.utils import timezone

        Gender = request.POST['gender']
        Age = int(request.POST['age'])
        NS1 = int(request.POST['ns1'])
        IgG = int(request.POST['igg'])
        IgM = int(request.POST['igm'])
        Area = request.POST['area']
        AreaType = request.POST['areatype']
        HouseType = request.POST['housetype']
        District = request.POST['district']

        data = pd.read_csv("C:\\Users\\rmurs\\PycharmProjects\\detection_of_dengue\\myapp\\datasetdengue.csv")

        label_encoders = {}
        for column in data.columns:
            if data[column].dtype == 'object':
                le = LabelEncoder()
                data[column] = le.fit_transform(data[column])
                label_encoders[column] = le

        X = data.drop("Outcome", axis=1)
        y = data["Outcome"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        model = GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=3,
            random_state=42
        )

        model.fit(X_train, y_train)

        new_patient = pd.DataFrame([{
            'Gender': Gender,
            'Age': Age,
            'NS1': NS1,
            'IgG': IgG,
            'IgM': IgM,
            'Area': Area,
            'AreaType': AreaType,
            'HouseType': HouseType,
            'District': District
        }])

        for column in new_patient.columns:
            if column in label_encoders:
                new_patient[column] = label_encoders[column].transform(new_patient[column])

        prediction = model.predict(new_patient)

        if prediction[0] == 1:
            result = "Dengue Positive"
        else:
            result = "Dengue Negative"

        resultlog = Logs()
        resultlog.date = timezone.now().date()
        resultlog.time = timezone.now().time()
        resultlog.result = result
        resultlog.USER = Users.objects.get(AUTHUSER_id=request.user.id)
        resultlog.save()

        return render(request, "users/XGpred.html", {"result": result})


