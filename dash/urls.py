"""covid_dash URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from . import views

urlpatterns = [
    path('home', views.home, name='home'),
    path('', views.home, name='home'),
    path('deathdetailview',views.deathdetailview, name='deathdetailview'),
    path('indianabroadview', views.indianabroadview, name='indianabroadview'),
    path('statewisedetailview<str:state>', views.statewisedetailview, name='statewisedetailview'),
    path('statewisedetailview', views.statewisedetailview, name='statewisedetailview'),
    path('reset', views.reset, name='reset'),
    path('feedbackview', views.feedbackview, name='feedbackview'),
    path('aboutview', views.aboutview, name='aboutview')
]
