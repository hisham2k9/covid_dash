from django.db import models
from django.forms import ModelForm
from django import forms
from django.core.exceptions import FieldError
import datetime
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone
from django.forms import DateTimeInput
from django.contrib.admin.widgets import AdminDateWidget,AdminTimeWidget, AdminSplitDateTime
from django.conf import settings
from django.core.exceptions import ValidationError


# Create your models here.

#create model of recover
#model of death
#model of new cases
#model of count of test each day

class death(models.Model):
    datetime_update=models.DateTimeField(default=datetime.datetime.now)
    date=models.DateField(default=datetime.date.today)
    andaman_and_nicobar=models.IntegerField(default=0)
    andhra_pradesh=models.IntegerField(default=0)
    assam=models.IntegerField(default=0)	
    bihar=models.IntegerField(default=0)	
    chandigarh=models.IntegerField(default=0)	
    chhattisgarh=models.IntegerField(default=0)
    delhi=models.IntegerField(default=0)	
    goa=models.IntegerField(default=0)	
    gujarat=models.IntegerField(default=0)	
    haryana=models.IntegerField(default=0)	
    himachal_pradesh=models.IntegerField(default=0)	
    jammu_and_kashmir=models.IntegerField(default=0)	
    karnataka=models.IntegerField(default=0)	
    kerala=models.IntegerField(default=0)	
    ladakh=models.IntegerField(default=0)	
    madhya_pradesh=models.IntegerField(default=0)	
    maharashtra=models.IntegerField(default=0)	
    manipur=models.IntegerField(default=0)	
    mizoram=models.IntegerField(default=0)
    odisha=models.IntegerField(default=0)	
    puducherry=models.IntegerField(default=0)
    punjab=models.IntegerField(default=0)	
    rajasthan=models.IntegerField(default=0)	
    tamil_nadu=models.IntegerField(default=0)	
    telangana=models.IntegerField(default=0)	
    uttarakhand=models.IntegerField(default=0)	
    uttar_pradesh=models.IntegerField(default=0)	
    west_bengal=models.IntegerField(default=0)
    
    def __str__(self):
        return "{}".format(self.date)
    
class recovery(models.Model):
    datetime_update=models.DateTimeField(default=datetime.datetime.now)
    date=models.DateField(default=datetime.date.today)
    andaman_and_nicobar=models.IntegerField(default=0)
    andhra_pradesh=models.IntegerField(default=0)
    assam=models.IntegerField(default=0)	
    bihar=models.IntegerField(default=0)	
    chandigarh=models.IntegerField(default=0)	
    chhattisgarh=models.IntegerField(default=0)
    delhi=models.IntegerField(default=0)	
    goa=models.IntegerField(default=0)	
    gujarat=models.IntegerField(default=0)	
    haryana=models.IntegerField(default=0)	
    himachal_pradesh=models.IntegerField(default=0)	
    jammu_and_kashmir=models.IntegerField(default=0)	
    karnataka=models.IntegerField(default=0)	
    kerala=models.IntegerField(default=0)	
    ladakh=models.IntegerField(default=0)	
    madhya_pradesh=models.IntegerField(default=0)	
    maharashtra=models.IntegerField(default=0)	
    manipur=models.IntegerField(default=0)	
    mizoram=models.IntegerField(default=0)
    odisha=models.IntegerField(default=0)	
    puducherry=models.IntegerField(default=0)
    punjab=models.IntegerField(default=0)	
    rajasthan=models.IntegerField(default=0)	
    tamil_nadu=models.IntegerField(default=0)	
    telangana=models.IntegerField(default=0)	
    uttarakhand=models.IntegerField(default=0)	
    uttar_pradesh=models.IntegerField(default=0)	
    west_bengal=models.IntegerField(default=0)
    
    def __str__(self):
        return "{}".format(self.date)
    
class newcase(models.Model):
    datetime_update=models.DateTimeField(default=datetime.datetime.now)
    date=models.DateField(default=datetime.date.today)
    andaman_and_nicobar=models.IntegerField(default=0)
    andhra_pradesh=models.IntegerField(default=0)
    assam=models.IntegerField(default=0)	
    bihar=models.IntegerField(default=0)	
    chandigarh=models.IntegerField(default=0)	
    chhattisgarh=models.IntegerField(default=0)
    delhi=models.IntegerField(default=0)	
    goa=models.IntegerField(default=0)	
    gujarat=models.IntegerField(default=0)	
    haryana=models.IntegerField(default=0)	
    himachal_pradesh=models.IntegerField(default=0)	
    jammu_and_kashmir=models.IntegerField(default=0)	
    karnataka=models.IntegerField(default=0)	
    kerala=models.IntegerField(default=0)	
    ladakh=models.IntegerField(default=0)	
    madhya_pradesh=models.IntegerField(default=0)	
    maharashtra=models.IntegerField(default=0)	
    manipur=models.IntegerField(default=0)	
    mizoram=models.IntegerField(default=0)
    odisha=models.IntegerField(default=0)	
    puducherry=models.IntegerField(default=0)
    punjab=models.IntegerField(default=0)	
    rajasthan=models.IntegerField(default=0)	
    tamil_nadu=models.IntegerField(default=0)	
    telangana=models.IntegerField(default=0)	
    uttarakhand=models.IntegerField(default=0)	
    uttar_pradesh=models.IntegerField(default=0)	
    west_bengal=models.IntegerField(default=0)
    
    def __str__(self):
        return "{}".format(self.date)
    
class deathdetail(models.Model):
    death_number=models.IntegerField(unique=True)
    death_date=models.DateField()
    age=models.IntegerField(null=True, blank=True)
    gender=models.CharField(max_length=10, null=True, blank=True)
    nationality=models.CharField(max_length=20, null=True, blank=True)
    state=models.CharField(max_length=50, null=True, blank=True)
    suspected_reason=models.CharField(max_length=100, null=True, blank=True)
    comorbidities=models.CharField(max_length=100, null=True, blank=True)
    source=models.CharField(max_length=300, null=True, blank=True)
    
    def __str__(self):
        return "death Number: {} , DoD: {}".format(self.death_number, self.death_date)
    
class testcount(models.Model):
    datetime_update=models.DateTimeField(default=datetime.datetime.now)
    date=models.DateField(default=datetime.date.today)
    test_count=models.IntegerField()
    
    def __str__(self):
        return "Test count: {} , Date: {}".format(self.test_count, self.date)
    
class keycountry(models.Model):
    datetime_update=models.DateTimeField(default=datetime.datetime.now)
    date=models.DateField(default=datetime.date.today)
    china=models.IntegerField()
    us=models.IntegerField()
    uk=models.IntegerField()
    italy=models.IntegerField()
    france=models.IntegerField()
    germany=models.IntegerField()
    spain=models.IntegerField()
    iran=models.IntegerField()
    india=models.IntegerField()
    
    def __str__(self):
        return "Update on {}".format(self.date)
    
class indianabroad(models.Model):
    datetime_update=models.DateTimeField(default=datetime.datetime.now)
    country=models.CharField(max_length=100)
    active_cases=models.IntegerField()
    deaths=models.IntegerField()
    
    def __str__(self):
        return "{}".format(self.country)
    
    def total_count(self):
        return self.active_cases+self.deaths  # or whatever self.days-based calculation
    
class feedback(models.Model):
    feedback=models.TextField()
    person=models.EmailField()
    datetime_update=models.DateTimeField(default=datetime.datetime.now)