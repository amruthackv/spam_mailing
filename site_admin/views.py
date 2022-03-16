from django.shortcuts import render,redirect
from site_admin.models import *
from site_user.models import *
from django.contrib import messages
from django.http import JsonResponse

# Create your views here.
def addHobbies(request):
    return render(request,'admin/addHobbies.html')

def addHobbiesAction(request):
    hobby=request.POST['hobby']
    hobbies=hobby_tb(hobby=hobby.lower())
    hobbies.save()
    messages.add_message(request,messages.INFO,'Hobby Added Successfully!!!')
    return redirect('addHobbies')

def checkHobby(request):
    hobby=request.GET['hobby']
    hobbies=hobby_tb.objects.filter(hobby=hobby.lower())
    if len(hobbies)>0:
        msg="exist";
    else:
        msg="do not exist"
    return JsonResponse({'valid':msg})

def addHobbyFactor(request):
    hobby=hobby_tb.objects.all()
    return render(request,'admin/addHobbyFactor.html',{'data':hobby})

def checkHobbyFactor(request):
    hobby=request.GET['hobby']
    factor=request.GET['factor'].lower()
    hobbyFactor=hobby_factor_tb.objects.filter(hobbyid=hobby,factor=factor)
    if len(hobbyFactor)>0:
        msg='exist'
    else:
        msg='do not exist'
    return JsonResponse({'valid':msg})

def addHobbyFactorAction(request):
    hobby=request.POST['hobby']
    hobbyObj=hobby_tb.objects.get(id=hobby)
    factor=request.POST['factor'].lower()
    hobbyFactor=hobby_factor_tb(hobbyid=hobbyObj,factor=factor)
    hobbyFactor.save()
    messages.add_message(request,messages.INFO,'Factor Added Successfully')
    return redirect('addHobbyFactor')

def addAgeFactor(request):
    return render(request,'admin/addAgeFactor.html')

def checkAgeFactor(request):
    minAge=request.GET['minimmumAge']
    maxAge=request.GET['maxAge']
    factor=request.GET['factor']
    print(minAge,' -> ',maxAge,' -> ',factor)
    ageFactor=age_factor_tb.objects.filter(minAge=minAge,maxAge=maxAge,factor=factor.lower())
    if len(ageFactor)>0:
        msg='exist'
    else:
        msg='do not exist'
    return JsonResponse({'valid':msg})

def addAgeFactorAction(request):
    minAge=request.POST['minAge']
    maxAge=request.POST['maxAge']
    factor=request.POST['factor']
    if int(minAge)<int(maxAge):
        ageFactor=age_factor_tb(minAge=minAge,maxAge=maxAge,factor=factor.lower())
        ageFactor.save()
        messages.add_message(request,messages.INFO,'Factor Added Successfully')
        return redirect('addAgeFactor')
    else:
        messages.add_message(request,messages.INFO,'Max age less than min age')
        return redirect('addAgeFactor')

def addSeasons(request):
    return render(request,'admin/addSeasons.html')

def checkSeason(request):
    season=request.GET['season']
    seasons=season_tb.objects.filter(season=season.lower())
    if len(seasons)>0:
        msg='exist'
    else:
        msg='do not exist'
    return JsonResponse({'valid':msg})

def addSeasonsAction(request):
    season=request.POST['season']
    seasons=season_tb(season=season.lower())
    seasons.save()
    messages.add_message(request,messages.INFO,'Season Added Successfully!!!')
    return redirect('addSeasons')

def addSeasonFactor(request):
    season=season_tb.objects.all()
    return render(request,'admin/addSeasonFactor.html',{'data':season})

def checkSeasonFactor(request):
    season=request.GET['season']
    factor=request.GET['factor']
    seasonFactor=season_factor_tb.objects.filter(seasonid=season,factor=factor.lower())
    if len(seasonFactor)>0:
        msg='exist'
    else:
        msg='do not exist'
    return JsonResponse({'valid':msg})

def addSeasonFactorAction(request):
    season=request.POST['season']
    factor=request.POST['factor']
    seasonObj=season_tb.objects.get(id=season)
    seasonFactor=season_factor_tb(seasonid=seasonObj,factor=factor.lower())
    seasonFactor.save()
    messages.add_message(request,messages.INFO,'Season factor added successfully')
    return redirect('addSeasonFactor')

def addSeasonCountry(request):
    season=season_tb.objects.all()
    country=country_tb.objects.all()
    return render(request,'admin/addSeasonCountry.html',{'season':season,'country':country})

def getSeasonFactor(request):
    season=request.GET['sesn']
    seasonFactor=season_factor_tb.objects.filter(seasonid=season)
    return render(request,'admin/getSeasonFactor.html',{'data':seasonFactor})

def checkSeasonCountry(request):
    season=request.GET['season']
    factor=request.GET['factor']
    country=request.GET['country']
    state=request.GET['state']
    month=request.GET['month']
    seasonCountry=season_country_tb.objects.filter(seasonid=season,factorid=factor,countryid=country,stateid=state,month=month)
    if len(seasonCountry)>0:
        msg='exist'
    else:
        msg='do not exist'
    return JsonResponse({'valid':msg})

def addSeasonCountryAction(request):
    season=request.POST['season']
    factor=request.POST['factor']
    country=request.POST['country']
    state=request.POST['state']
    month=request.POST['month']
    seasonObj=season_tb.objects.get(id=season)
    factorObj=season_factor_tb.objects.get(id=factor)
    countryObj=country_tb.objects.get(id=country)
    stateObj=state_tb.objects.get(id=state)
    seasonCountry=season_country_tb(seasonid=seasonObj,factorid=factorObj,countryid=countryObj,stateid=stateObj,month=month)
    seasonCountry.save()
    messages.add_message(request,messages.INFO,'Data saved successfully')
    return redirect('addSeasonCountry')
    









