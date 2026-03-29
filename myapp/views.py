from datetime import datetime, timezone
import pickle

import pandas as pd
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
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
    logout(request)
    return redirect("/myapp/login_get/")







# A D M I N ---------------------










@login_required(login_url="/myapp/login_get/")
def adminhome(request):
    return render(request,'adminpages/adminhomeindex.html')

@login_required(login_url="/myapp/login_get/")
def changepassword_get(request):
    return render(request,'adminpages/changepassword.html')

@login_required(login_url="/myapp/login_get/")
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



@login_required(login_url="/myapp/login_get/")
def sentreply_get(request,id):
    return render(request,'adminpages/sentreply.html',{'id':id})

@login_required(login_url="/myapp/login_get/")
def sentreply_post(request):
    reply=request.POST['reply']
    id=request.POST['id']
    data = Complaint.objects.get(id=id)
    data.reply=reply
    data.status='replied'
    data.save()
    return redirect("/myapp/viewcomplaint_get/")

@login_required(login_url="/myapp/login_get/")
def viewcomplaint_get(request):
    data=Complaint.objects.all()
    return render(request,'adminpages/viewcomplaint.html',{'data':data})

@login_required(login_url="/myapp/login_get/")
def review_get(request):
    data=Review.objects.all()
    return render(request,'adminpages/review.html',{'data':data})
@login_required(login_url="/myapp/login_get/")
def viewlogs_get(request):
    data=Logs.objects.all()
    return render(request,'adminpages/viewlogs.html',{'data':data})
@login_required(login_url="/myapp/login_get/")
def viewuser_get(request):
    data=Users.objects.filter(status='pending')
    return render(request,'adminpages/viewuser.html',{'data':data})
@login_required(login_url="/myapp/login_get/")
def blockusers_get(request,id):
    Users.objects.filter(id=id).update(status='Blocked')
    return redirect('/myapp/viewuser_get/#a')

@login_required(login_url="/myapp/login_get/")
def viewblockedusers_get(request):
    data = Users.objects.filter(status='Blocked')
    return render(request,'adminpages/viewblockedusers.html',{'data':data})
@login_required(login_url="/myapp/login_get/")
def unblockuser_get(request,id):
    Users.objects.filter(id=id).update(status='pending')
    return redirect('/myapp/viewuser_get/#a')







# U S E R S -----------------------






@login_required(login_url="/myapp/login_get/")
def edit_get(request):
    u = Users.objects.get(AUTHUSER=request.user)

    return render(request,'users/edit.html',{'data':u})


@login_required(login_url="/myapp/login_get/")
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
    return redirect("/myapp/viewprofile_get/#a")


def register_get(request):
    return render(request,'users/Register.html')
def register_post(request):
    name = request.POST['name']

    if not name.replace(" ", "").isalpha():
        return redirect('/myapp/register_get/')
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

@login_required(login_url="/myapp/login_get/")
def sentcomplaint_get(request):
    return render(request,'users/sentcomplaint.html')
@login_required(login_url="/myapp/login_get/")
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
@login_required(login_url="/myapp/login_get/")
def viewprofile_get(request):
    data=Users.objects.get(AUTHUSER_id=request.user.id)
    return render(request,'users/viewprofile.html',{'data':data})
@login_required(login_url="/myapp/login_get/")
def viewreply_get(request):
    a=Complaint.objects.filter(USERS__AUTHUSER=request.user)
    return render(request,'users/viewreply.html',{'data':a})

@login_required(login_url="/myapp/login_get/")
def userhome_get(request):
    return render(request,'users/userhomeindex.html')
@login_required(login_url="/myapp/login_get/")
def userviewlogs_get(request):
    data=Logs.objects.filter(USER__AUTHUSER=request.user)
    return render(request,'users/logs.html',{'data':data})
@login_required(login_url="/myapp/login_get/")
def sendreview_get(request):
    return render(request, 'users/sendreview.html')
@login_required(login_url="/myapp/login_get/")
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



#################################################################
# 1. Random forest
import pandas as pd
from django.shortcuts import render
from .models import *
from datetime import datetime

# with open(r"C:\Users\user\PycharmProjects\detection_of_dengue\trained models\randomforest_dengue_model.pkl", "rb") as f:
with open(r"C:\Users\rmurs\Downloads\detection_of_dengue_28-03-2026\detection_of_dengue\trained models\randomforest_dengue_model.pkl","rb") as f:
    model, label_encoders = pickle.load(f)

@login_required(login_url="/myapp/login_get/")
def dataset_get(request):
    return render(request, 'users/dataset.html')


def dataset_post(request):

    if request.method == "POST":

        Gender = request.POST['gender']
        Age = int(request.POST['age'])
        NS1 = int(request.POST['ns1'])
        IgG = int(request.POST['igg'])
        IgM = int(request.POST['igm'])

        # Create input
        new_patient = pd.DataFrame([{
            'Gender': Gender,
            'Age': Age,
            'NS1': NS1,
            'IgG': IgG,
            'IgM': IgM
        }])

        # Encode input
        for column in new_patient.columns:
            if column in label_encoders:
                new_patient[column] = label_encoders[column].transform(new_patient[column])

        # Predict
        prediction = model.predict(new_patient)

        if prediction[0] == 1:
            result = "Dengue Positive"
        else:
            result = "Dengue Negative"

        # Save log
        resultlog = Logs()
        resultlog.date = datetime.now().date()
        resultlog.time = datetime.now().time()
        resultlog.result = result
        resultlog.USER = Users.objects.get(AUTHUSER_id=request.user.id)
        resultlog.save()

        return render(request, "users/dataset.html", {"result": result})

    return render(request, "users/dataset.html")


#2. Linear regression
import pickle
with open(r"C:\Users\rmurs\Downloads\detection_of_dengue_28-03-2026\detection_of_dengue\trained models\linear_regression_dengue_model.pkl", "rb") as f:
    lr_model, label_encoders = pickle.load(f)

@login_required(login_url="/myapp/login_get/")
def LRpred_get(request):
    return render(request, 'users/LRpred.html')


@login_required(login_url="/myapp/login_get/")
def LRpred_post(request):

    if request.method == "POST":

        Gender = request.POST['gender']
        Age = int(request.POST['age'])
        NS1 = int(request.POST['ns1'])
        IgG = int(request.POST['igg'])
        IgM = int(request.POST['igm'])

        # Create input
        new_patient = pd.DataFrame([{
            'Gender': Gender,
            'Age': Age,
            'NS1': NS1,
            'IgG': IgG,
            'IgM': IgM
        }])

        # Encode safely
        for column in new_patient.columns:
            if column in label_encoders:
                le = label_encoders[column]
                if new_patient[column][0] in le.classes_:
                    new_patient[column] = le.transform(new_patient[column])
                else:
                    new_patient[column] = -1  # unknown value handling

        # Predict
        prediction = lr_model.predict(new_patient)

        result = "Dengue Positive" if prediction[0] == 1 else "Dengue Negative"

        # Save log
        from django.utils import timezone

        resultlog = Logs()
        resultlog.date = timezone.now().date()
        resultlog.time = timezone.now().time()
        resultlog.result = result
        resultlog.USER = Users.objects.get(AUTHUSER_id=request.user.id)
        resultlog.save()

        return render(request, "users/LRpred.html", {"result": result})

#3. SVM
import pickle
with open(r"C:\Users\rmurs\Downloads\detection_of_dengue_28-03-2026\detection_of_dengue\trained models\svm_dengue_model.pkl", "rb") as f:
    svm_model, label_encoders = pickle.load(f)

@login_required(login_url="/myapp/login_get/")
def SVMpred_get(request):
    return render(request, 'users/SVMpred.html')


@login_required(login_url="/myapp/login_get/")
def SVMpred_post(request):

    if request.method == "POST":

        Gender = request.POST['gender']
        Age = int(request.POST['age'])
        NS1 = int(request.POST['ns1'])
        IgG = int(request.POST['igg'])
        IgM = int(request.POST['igm'])

        # Input
        new_patient = pd.DataFrame([{
            'Gender': Gender,
            'Age': Age,
            'NS1': NS1,
            'IgG': IgG,
            'IgM': IgM
        }])

        # Safe encoding
        for column in new_patient.columns:
            if column in label_encoders:
                le = label_encoders[column]
                if new_patient[column][0] in le.classes_:
                    new_patient[column] = le.transform(new_patient[column])
                else:
                    new_patient[column] = -1

        # Predict
        prediction = svm_model.predict(new_patient)

        result = "Dengue Positive" if prediction[0] == 1 else "Dengue Negative"

        # Save log
        from django.utils import timezone

        resultlog = Logs()
        resultlog.date = timezone.now().date()
        resultlog.time = timezone.now().time()
        resultlog.result = result
        resultlog.USER = Users.objects.get(AUTHUSER_id=request.user.id)
        resultlog.save()

        return render(request, "users/SVMpred.html", {"result": result})


#4. Decision Tree
import pickle

with open(r"C:\Users\rmurs\Downloads\detection_of_dengue_28-03-2026\detection_of_dengue\trained models\decision_tree_dengue_model.pkl", "rb") as f:
    dt_model, label_encoders = pickle.load(f)

@login_required(login_url="/myapp/login_get/")
def DTpred_get(request):
    return render(request, 'users/DTpred.html')


@login_required(login_url="/myapp/login_get/")
def DTpred_post(request):

    if request.method == "POST":

        Gender = request.POST['gender']
        Age = int(request.POST['age'])
        NS1 = int(request.POST['ns1'])
        IgG = int(request.POST['igg'])
        IgM = int(request.POST['igm'])

        # Input
        new_patient = pd.DataFrame([{
            'Gender': Gender,
            'Age': Age,
            'NS1': NS1,
            'IgG': IgG,
            'IgM': IgM
        }])

        # Safe encoding
        for column in new_patient.columns:
            if column in label_encoders:
                le = label_encoders[column]
                if new_patient[column][0] in le.classes_:
                    new_patient[column] = le.transform(new_patient[column])
                else:
                    new_patient[column] = -1

        # Predict
        prediction = dt_model.predict(new_patient)

        result = "Dengue Positive" if prediction[0] == 1 else "Dengue Negative"

        # Save log
        from django.utils import timezone

        resultlog = Logs()
        resultlog.date = timezone.now().date()
        resultlog.time = timezone.now().time()
        resultlog.result = result
        resultlog.USER = Users.objects.get(AUTHUSER_id=request.user.id)
        resultlog.save()

        return render(request, "users/DTpred.html", {"result": result})

#6. XG Boost

import pickle

with open(r"C:\Users\rmurs\Downloads\detection_of_dengue_28-03-2026\detection_of_dengue\trained models\xgboost_dengue_model.pkl", "rb") as f:
    gb_model, label_encoders = pickle.load(f)

@login_required(login_url="/myapp/login_get/")
def XGpred_get(request):
    return render(request, 'users/XGpred.html')


@login_required(login_url="/myapp/login_get/")
def XGpred_post(request):

    if request.method == "POST":

        Gender = request.POST['gender']
        Age = int(request.POST['age'])
        NS1 = int(request.POST['ns1'])
        IgG = int(request.POST['igg'])
        IgM = int(request.POST['igm'])

        # Input
        new_patient = pd.DataFrame([{
            'Gender': Gender,
            'Age': Age,
            'NS1': NS1,
            'IgG': IgG,
            'IgM': IgM
        }])

        # Safe encoding
        for column in new_patient.columns:
            if column in label_encoders:
                le = label_encoders[column]
                if new_patient[column][0] in le.classes_:
                    new_patient[column] = le.transform(new_patient[column])
                else:
                    new_patient[column] = -1

        # Predict
        prediction = gb_model.predict(new_patient)

        result = "Dengue Positive" if prediction[0] == 1 else "Dengue Negative"

        # Save log
        from django.utils import timezone

        resultlog = Logs()
        resultlog.date = timezone.now().date()
        resultlog.time = timezone.now().time()
        resultlog.result = result
        resultlog.USER = Users.objects.get(AUTHUSER_id=request.user.id)
        resultlog.save()

        return render(request, "users/XGpred.html", {"result": result})



#7. LSTM----------------
import pickle
import numpy as np
from tensorflow.keras.models import load_model

# Load model
lstm_model = load_model(r"C:\Users\rmurs\Downloads\detection_of_dengue_28-03-2026\detection_of_dengue\trained models\lstm_model.h5")

with open(r"C:\Users\rmurs\Downloads\detection_of_dengue_28-03-2026\detection_of_dengue\trained models\lstm_meta.pkl", "rb") as f:
    label_encoders, scaler = pickle.load(f)

@login_required(login_url="/myapp/login_get/")
def LSTMpred_get(request):
    return render(request, 'users/LSTMpred.html')


@login_required(login_url="/myapp/login_get/")
def LSTMpred_post(request):

    if request.method == "POST":

        Gender = request.POST['gender']
        Age = int(request.POST['age'])
        NS1 = int(request.POST['ns1'])
        IgG = int(request.POST['igg'])
        IgM = int(request.POST['igm'])

        import pandas as pd

        new_patient = pd.DataFrame([{
            'Gender': Gender,
            'Age': Age,
            'NS1': NS1,
            'IgG': IgG,
            'IgM': IgM
        }])

        # Encode
        for column in new_patient.columns:
            if column in label_encoders:
                le = label_encoders[column]
                if new_patient[column][0] in le.classes_:
                    new_patient[column] = le.transform(new_patient[column])
                else:
                    new_patient[column] = -1

        # Scale + reshape
        new_patient = scaler.transform(new_patient)
        new_patient = np.reshape(new_patient, (1, 1, new_patient.shape[1]))

        prediction = lstm_model.predict(new_patient)

        result = "Dengue Positive" if prediction[0][0] > 0.5 else "Dengue Negative"

        from django.utils import timezone

        resultlog = Logs()
        resultlog.date = timezone.now().date()
        resultlog.time = timezone.now().time()
        resultlog.result = result
        resultlog.USER = Users.objects.get(AUTHUSER_id=request.user.id)
        resultlog.save()

        return render(request, "users/LSTMpred.html", {"result": result})

# compare predictions----------------

@login_required(login_url="/myapp/login_get/")
def comparepred_get(request):
    return render(request, 'users/comparepred.html')
@login_required(login_url="/myapp/login_get/")
def comparepred_post(request):
    if request.method == "POST":

        import pandas as pd
        import numpy as np
        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import LabelEncoder, StandardScaler
        from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
        from sklearn.linear_model import LogisticRegression
        from sklearn.svm import SVC
        from sklearn.tree import DecisionTreeClassifier
        from sklearn.metrics import accuracy_score
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import LSTM
        from tensorflow.keras.layers import Dense

        Gender = request.POST['gender']
        Age = int(request.POST['age'])
        NS1 = int(request.POST['ns1'])
        IgG = int(request.POST['igg'])
        IgM = int(request.POST['igm'])
        # Area = request.POST['area']
        # AreaType = request.POST['areatype']
        # HouseType = request.POST['housetype']
        # District = request.POST['district']
        # Area = Area.capitalize()
        # District = District.capitalize()

        data = pd.read_csv(r"C:\Users\rmurs\Downloads\detection_of_dengue_28-03-2026\detection_of_dengue\myapp\augmented_dengue_2000.csv")
        # data = pd.read_csv(r"C:\Users\rmurs\Downloads\merged_df71d34c8aa84415.csv")

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

        new_patient = pd.DataFrame([{
            'Gender': Gender,
            'Age': Age,
            'NS1': NS1,
            'IgG': IgG,
            'IgM': IgM,
            # 'Area': Area,
            # 'AreaType': AreaType,
            # 'HouseType': HouseType,
            # 'District': District
        }])

        for column in new_patient.columns:
            if column in label_encoders:
                new_patient[column] = label_encoders[column].transform(new_patient[column])

        results = {}

        # 🔹 Random Forest
        rf = RandomForestClassifier(n_estimators=100, random_state=42)
        rf.fit(X_train, y_train)
        rf_pred = rf.predict(new_patient)[0]
        rf_acc = accuracy_score(y_test, rf.predict(X_test))
        results["Random Forest"] = {
            "prediction": "Dengue Positive" if rf_pred == 1 else "Dengue Negative",
            "accuracy": round(rf_acc * 100, 2)
        }

        # 🔹 Logistic Regression
        lr = LogisticRegression(max_iter=1000)
        lr.fit(X_train, y_train)
        lr_pred = lr.predict(new_patient)[0]
        lr_acc = accuracy_score(y_test, lr.predict(X_test))
        results["Logistic Regression"] = {
            "prediction": "Dengue Positive" if lr_pred == 1 else "Dengue Negative",
            "accuracy": round(lr_acc * 100, 2)
        }

        # 🔹 SVM
        svm = SVC()
        svm.fit(X_train, y_train)
        svm_pred = svm.predict(new_patient)[0]
        svm_acc = accuracy_score(y_test, svm.predict(X_test))
        results["SVM"] = {
            "prediction": "Dengue Positive" if svm_pred == 1 else "Dengue Negative",
            "accuracy": round(svm_acc * 100, 2)
        }

        # 🔹 Decision Tree
        dt = DecisionTreeClassifier(max_depth=5)
        dt.fit(X_train, y_train)
        dt_pred = dt.predict(new_patient)[0]
        dt_acc = accuracy_score(y_test, dt.predict(X_test))
        results["Decision Tree"] = {
            "prediction": "Dengue Positive" if dt_pred == 1 else "Dengue Negative",
            "accuracy": round(dt_acc * 100, 2)
        }

        # 🔹 Gradient Boosting
        gb = GradientBoostingClassifier()
        gb.fit(X_train, y_train)
        gb_pred = gb.predict(new_patient)[0]
        gb_acc = accuracy_score(y_test, gb.predict(X_test))
        results["Gradient Boosting"] = {
            "prediction": "Dengue Positive" if gb_pred == 1 else "Dengue Negative",
            "accuracy": round(gb_acc * 100, 2)
        }

        # 🔹 LSTM
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        X_scaled = np.reshape(X_scaled, (X_scaled.shape[0], 1, X_scaled.shape[1]))

        X_train_l, X_test_l, y_train_l, y_test_l = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42
        )

        lstm_model = Sequential()
        lstm_model.add(LSTM(64, input_shape=(1, X_scaled.shape[2])))
        lstm_model.add(Dense(1, activation='sigmoid'))
        lstm_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        lstm_model.fit(X_train_l, y_train_l, epochs=5, batch_size=16, verbose=0)

        lstm_acc = accuracy_score(y_test_l, (lstm_model.predict(X_test_l) > 0.5).astype(int))
        new_scaled = scaler.transform(new_patient)
        new_scaled = np.reshape(new_scaled, (1, 1, new_scaled.shape[1]))
        lstm_pred = (lstm_model.predict(new_scaled) > 0.5).astype(int)[0][0]

        results["LSTM"] = {
            "prediction": "Dengue Positive" if lstm_pred == 1 else "Dengue Negative",
            "accuracy": round(lstm_acc * 100, 2)
        }

        # 🔥 Find Best Model
        best_model = max(results, key=lambda x: results[x]["accuracy"])
        best_result = results[best_model]["prediction"]

        return render(request, "users/comparepred.html", {
            "results": results,
            "best_model": best_model,
            "best_result": best_result
        })
