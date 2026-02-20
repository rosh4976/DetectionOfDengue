"""
URL configuration for detection_of_dengue project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from myapp import views

urlpatterns = [
    path('login_get/',views.login_get),
    path('login_post/',views.login_post),
    path('forgotpassword_get/',views.forgotpassword_get),
    path('forgotpassword_post/',views.forgotpassword_post),
    path('changepassword_get/',views.changepassword_get),
    path('changepassword_post/',views.changepassword_post),
    path('sentreply_get/<id>',views.sentreply_get),
    path('sentreply_post/',views.sentreply_post),
    path('viewblockedusers_get/',views.viewblockedusers_get),
    path('viewcomplaint_get/', views.viewcomplaint_get),
    path('viewlogs_get/',views.viewlogs_get),
    path('viewuser_get/',views.viewuser_get),
    path('review_get/',views.review_get),
    path('edit_get/', views.edit_get),
    path('edit_post/', views.edit_post),
    path('register_get/', views.register_get),
    path('register_post/', views.register_post),
    path('sentcomplaint_get/', views.sentcomplaint_get),
    path('sentcomplaint_post/',views.sentcomplaint_post),
    path('viewprofile_get/',views.viewprofile_get),
    path('viewreply_get/',views.viewreply_get),
    path('adminhome/',views.adminhome),
    path('logout_get/',views.logout_get),
    path('blockusers_get/<id>', views.blockusers_get),
    path('unblockuser_get/<id>', views.unblockuser_get),
    path('userhome_get/', views.userhome_get),
    path('userviewlogs_get/', views.userviewlogs_get),
    path('sendreview_get/', views.sendreview_get),
    path('sendreview_post/', views.sendreview_post),
]
