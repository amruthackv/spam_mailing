from django.db import models

# Create your models here.
class admin_tb(models.Model):
    username=models.CharField(max_length=20)
    password=models.CharField(max_length=20)

class hobby_tb(models.Model):
    hobby=models.CharField(max_length=30)

class hobby_factor_tb(models.Model):
    hobbyid=models.ForeignKey(hobby_tb,on_delete=models.CASCADE)
    factor=models.CharField(max_length=30)

class age_factor_tb(models.Model):
    minAge=models.IntegerField()
    maxAge=models.IntegerField()
    factor=models.CharField(max_length=30)

class season_tb(models.Model):
    season=models.CharField(max_length=20)

class season_factor_tb(models.Model):
    seasonid=models.ForeignKey(season_tb,on_delete=models.CASCADE)
    factor=models.CharField(max_length=20)

class season_country_tb(models.Model):
    seasonid=models.ForeignKey(season_tb,on_delete=models.CASCADE)
    factorid=models.ForeignKey(season_factor_tb,on_delete=models.CASCADE)
    countryid=models.ForeignKey('site_user.country_tb',on_delete=models.CASCADE)
    stateid=models.ForeignKey('site_user.state_tb',on_delete=models.CASCADE)
    month=models.CharField(max_length=20)
