from django.db import models
from site_admin.models import *

# Create your models here.
class country_tb(models.Model):
    country=models.CharField(max_length=20)

class state_tb(models.Model):
    state=models.CharField(max_length=20)
    countryid=models.ForeignKey(country_tb,on_delete=models.CASCADE)

class register_tb(models.Model):
    name=models.CharField(max_length=20)
    dob=models.CharField(max_length=20)
    gender=models.CharField(max_length=20)
    address=models.CharField(max_length=80)
    countryid=models.ForeignKey(country_tb,on_delete=models.CASCADE)
    stateid=models.ForeignKey(state_tb,on_delete=models.CASCADE)
    phone=models.CharField(max_length=20)
    username=models.CharField(max_length=30)
    password=models.CharField(max_length=20)
    security_question=models.CharField(max_length=50,default='no data')
    security_answer=models.CharField(max_length=30,default='no data')

class user_hobby_tb(models.Model):
    userid=models.ForeignKey(register_tb,on_delete=models.CASCADE)
    hobbyid=models.ForeignKey('site_admin.hobby_tb',on_delete=models.CASCADE)

class message_tb(models.Model):
    senderid=models.ForeignKey(register_tb,on_delete=models.CASCADE,related_name='sender')
    receiverid=models.ForeignKey(register_tb,on_delete=models.CASCADE,related_name='receiver')
    subject=models.CharField(max_length=50)
    message=models.CharField(max_length=200)
    date=models.CharField(max_length=20)
    time=models.CharField(max_length=20)
    status=models.CharField(max_length=20,default='pending')
    filter_status=models.CharField(max_length=20,default='pending')

class trash_tb(models.Model):
    messageid=models.ForeignKey(message_tb,on_delete=models.CASCADE)
    receiverid=models.ForeignKey(register_tb,on_delete=models.CASCADE)
    date=models.CharField(max_length=20)
    time=models.CharField(max_length=20)

class contact_tb(models.Model):
    contactid=models.ForeignKey(register_tb,on_delete=models.CASCADE,related_name='contact')
    userid=models.ForeignKey(register_tb,on_delete=models.CASCADE,related_name='user')
    name=models.CharField(max_length=20)
    remarks=models.CharField(max_length=100)
    date=models.CharField(max_length=20)
    time=models.CharField(max_length=20)

class blacklist_tb(models.Model):
    blackedid=models.ForeignKey(register_tb,on_delete=models.CASCADE,related_name='blackedid')
    userid=models.ForeignKey(register_tb,on_delete=models.CASCADE,related_name='userid')
    name=models.CharField(max_length=20)
    remarks=models.CharField(max_length=100)
    date=models.CharField(max_length=20)
    time=models.CharField(max_length=20)

class customer_hobby_tb(models.Model):
    userid=models.ForeignKey(register_tb,on_delete=models.CASCADE)
    hobbyid=models.ForeignKey(user_hobby_tb,on_delete=models.CASCADE)
    factorid=models.ForeignKey('site_admin.hobby_factor_tb',on_delete=models.CASCADE)

class customer_age_factor_tb(models.Model):
    userid=models.ForeignKey(register_tb,on_delete=models.CASCADE)
    factorid=models.ForeignKey(age_factor_tb,on_delete=models.CASCADE)

class customer_season_country_tb(models.Model):
    userid=models.ForeignKey(register_tb,on_delete=models.CASCADE)
    factorid=models.ForeignKey(season_country_tb,on_delete=models.CASCADE)



    
    
    
