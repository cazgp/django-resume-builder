"""resumebuilder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import RedirectView

from ..resume import views as resume_views
from ..user import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path(r'', RedirectView.as_view(pattern_name='resume')),

    #########
    # RESUMES
    #########
    path(r'resume/', resume_views.resumes, name='resume'),
    path(
        r'resume/<int:resume_id>',
        resume_views.resume_view,
        name='resume-view'
    ),
    path(
        r'resume/create/',
        resume_views.resume_create_view,
        name='resume-create'
    ),
    path(
        r'resume/edit/<int:resume_id>/',
        resume_views.resume_edit_view,
        name='resume-edit'
    ),

    ##############
    # RESUME ITEMS
    ##############

    # having resume_id and resume_item_id is redundant.
    # it does, however, make the URLs consistent.
    path(
        r'resume/<int:resume_id>/item/edit/<int:resume_item_id>/',
        resume_views.resume_item_edit_view,
        name='resume-item-edit'
    ),
    path(
        r'resume/<int:resume_id>/item/create/',
        resume_views.resume_item_create_view,
        name='resume-item-create'
    ),

    #######
    # USERS
    #######
    path(r'user/', user_views.account_edit_view, name='account-edit'),
    path(
        r'create-account/',
        user_views.account_create_view,
        name='account-create'
    ),
]
