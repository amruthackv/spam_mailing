from django.shortcuts import render,redirect
from site_user.models import *
from site_admin.models import *
from django.contrib import messages
from  django.http import JsonResponse
import datetime
from django.views.decorators.cache import never_cache,cache_control

# Create your views here.
def index(request):
    return render(request,'index.html')

def register(request):
    country=country_tb.objects.all()
    hobby=hobby_tb.objects.all()
    return render(request,'register.html',{'data1':country,'data3':hobby})

def getState(request):
    countryid=request.GET['country']
    state=state_tb.objects.filter(countryid=countryid)
    return render(request,'getState.html',{'data':state})

def registerAction(request):
    name=request.POST['name']
    dob=request.POST['dob']
    gender=request.POST['gender']
    address=request.POST['address']
    country=request.POST['country']
    countryObj=country_tb.objects.get(id=country)
    state=request.POST['state']
    stateObj=state_tb.objects.get(id=state)
    phone=request.POST['phone']
    username=request.POST['username']
    password=request.POST['password']
    secQstn=request.POST['secQstn']
    secAnswr=request.POST['secAnswr']
    uname=username.split('@')[0].lower()
    submitBtn= request.POST['submitButton'].lower()
    print(submitBtn)
    if submitBtn == 'register':
        user=register_tb(name=name,dob=dob,gender=gender,address=address,countryid=countryObj,stateid=stateObj,phone=phone,username=uname+'@mymail.com',password=password,security_question=secQstn,security_answer=secAnswr.lower())
        user.save()
        hobbies=request.POST.getlist('chooseHobby')
        for v in hobbies:
            if v != 'none':
                hby=hobby_tb.objects.get(id=v)
                user=register_tb.objects.get(username=uname+'@mymail.com')
                hobby=user_hobby_tb(hobbyid=hby,userid=user)
                hobby.save()
        messages.add_message(request,messages.INFO,'Registration Successfull!!!')
        return redirect('index')
    elif submitBtn == 'update':
        userid=request.session['userid']
        user=register_tb.objects.filter(id=userid).update(name=name,dob=dob,gender=gender,address=address,countryid=countryObj,stateid=stateObj,phone=phone,username=uname+'@mymail.com',password=password,security_question=secQstn,security_answer=secAnswr.lower())
        delHobby=user_hobby_tb.objects.filter(userid=userid).delete()
        hobbies=request.POST.getlist('chooseHobby')
        for v in hobbies:
            if v != 'none':
                hby=hobby_tb.objects.get(id=v)
                user=register_tb.objects.get(username=uname+'@mymail.com')
                hobby=user_hobby_tb(hobbyid=hby,userid=user)
                hobby.save()
        messages.add_message(request,messages.INFO,'Updated Successfully!!!')
        return redirect('userHome')
    

def checkUsername(request):
    username=request.GET['username']
    uname=username.split('@')[0].lower()
    user=register_tb.objects.filter(username=uname+'@mymail.com')
    if len(user)>0:
        msg='exist';
    else:
        msg='do not exist'
    return JsonResponse({'valid':msg})

@never_cache
def login(request):
    return render(request,'login.html')

@never_cache
def loginAction(request):
    #userType=request.POST['userType']
    username=request.POST['username']
    password=request.POST['password']
    uname=username.split('@')[0].lower()
    secQstn=request.POST['secQstn']
    secAns=request.POST['secAns']
    user=register_tb.objects.filter(username=uname+'@mymail.com',password=password,security_question=secQstn,security_answer=secAns.lower())
    
    admin=admin_tb.objects.filter(username=uname,password=password)
    if len(admin)>0:
        request.session['userid']=admin[0].id
        return render(request,'admin/adminHome.html',{'data':admin})
    elif len(user)>0:
        request.session['userid']=user[0].id
        return render(request,'user/userHome.html',{'data':user})
    else:
        messages.add_message(request,messages.INFO,'Incorrect Details')
        return redirect('login')
    

def composeMessage(request):
    uid=request.session['userid']
    user=register_tb.objects.filter(id=uid)
    return render(request,'user/composeMessage.html',{'data':user})

def checkReceiver(request):
    receiver=request.GET['receiver']
    user=register_tb.objects.filter(username=receiver)
    if len(user)>0:
        msg='exist'
    else:
        msg='do not exist'
    return JsonResponse({'valid':msg})

@never_cache
def composeMessageAction(request):
    sender=request.session['userid']
    receiver=request.POST['receiver']
    subject=request.POST['subject']
    message=request.POST['message']
    date=datetime.date.today()
    time=datetime.datetime.now().strftime('%H:%M')
    senderObj=register_tb.objects.get(id=sender)
    receiverObj=register_tb.objects.get(username=receiver)
    mail=message_tb(senderid=senderObj,receiverid=receiverObj,subject=subject,message=message,date=date,time=time,status='pending')
    mail.save()
    #return redirect('composeMessage')
    user=register_tb.objects.filter(id=sender)
    #return redirect('loginAction')
    return render(request,'user/userHome.html',{'data':user})

@never_cache
def viewSentItems(request):
    userid=request.session['userid']
    statusList=['pending','deleted by receiver','sent']
    sentItems=message_tb.objects.filter(status__in=statusList,senderid=userid)
    return render(request,'user/viewSentItems.html',{'data':sentItems})

@never_cache
def deletedBySender(request,uid):
    dlt=message_tb.objects.filter(id=uid)
    if dlt[0].status != 'deleted by receiver':
        mail=message_tb.objects.filter(id=uid).update(status='deleted by sender')
    else:
        mail=message_tb.objects.filter(id=uid).delete()
    messages.add_message(request,messages.INFO,'message deleted successfully')
    return redirect('viewSentItems')

@never_cache
def inbox(request):
    userid=request.session['userid']
    ageFactor=customer_age_factor_tb.objects.filter(userid=userid)
    statusList=['pending','deleted by sender']
    for v in ageFactor:
        msg=message_tb.objects.filter(receiverid=userid,filter_status='pending',message__icontains=v.factorid.factor).exclude(senderid__in=blacklist_tb.objects.filter(userid=userid).values('blackedid_id')).update(filter_status='filtered')
    hobbyFactor=customer_hobby_tb.objects.filter(userid=userid)
    for h in hobbyFactor:
        hobby=message_tb.objects.filter(receiverid=userid,filter_status='pending',message__icontains=h.factorid.factor).exclude(senderid__in=blacklist_tb.objects.filter(userid=userid).values('blackedid_id')).update(filter_status='filtered')
    seasonFactor=customer_season_country_tb.objects.filter(userid=userid)
    for s in seasonFactor:
        season=message_tb.objects.filter(receiverid=userid,filter_status='pending',message__icontains=s.factorid.factorid.factor).exclude(senderid__in=blacklist_tb.objects.filter(userid=userid).values('blackedid_id')).update(filter_status='filtered')
    contact=contact_tb.objects.filter(userid=userid)
    for c in contact:
        contactMail=message_tb.objects.filter(receiverid=userid,senderid=c.contactid,filter_status='pending').update(filter_status='filtered')
    mail=message_tb.objects.filter(receiverid=userid,status__in=statusList,filter_status='filtered').exclude(id__in=trash_tb.objects.filter(receiverid=userid).values('messageid_id'))
    return render(request,'user/inbox.html',{'data':mail})

@never_cache
def viewSpam(request):
    userid=request.session['userid']
    factors=[]
    ageFactor=customer_age_factor_tb.objects.filter(userid=userid)
    hobbyFactor=customer_hobby_tb.objects.filter(userid=userid)
    seasonFactor=customer_season_country_tb.objects.filter(userid=userid)
    for a in ageFactor:
        factors.append(a.factorid.factor)
    for h in hobbyFactor:
        factors.append(h.factorid.factor)
    for s in seasonFactor:
        factors.append(s.factorid.factorid.factor)
    statusList=['pending','deleted by sender']
    print(factors)
    if factors:
        for fact in factors:
            spam=message_tb.objects.filter(receiverid=userid,filter_status='pending',status__in=statusList).exclude(message__icontains=fact[0])
        if len(spam)>0:
            return render(request,'user/spam.html',{'data':spam})
        else:
            messages.add_message(request,messages.INFO,'No spam messages to show')
            return redirect('userHome')
    else:
        messages.add_message(request,messages.INFO,'No spam messages to show')
        return redirect('userHome')

def moveToTrash(request):
    receiver=request.session['userid']
    date=datetime.date.today()
    time=datetime.datetime.now().strftime('%H:%M')
    messages=request.POST.getlist('trashCheck')
    for v in messages:
        trash=trash_tb(messageid_id=v,receiverid_id=receiver,date=date,time=time)
        trash.save()
    return redirect('inbox')

@never_cache
def viewTrash(request):
    userid=request.session['userid']
    trash=trash_tb.objects.filter(receiverid=userid)
    if len(trash)>0:
        return render(request,'user/viewTrash.html',{'data':trash})
    else:
        messages.add_message(request,messages.INFO,'No trash messages to show')
        return redirect('userHome')

def deleteFromTrash(request,uid):
    status=message_tb.objects.filter(id=uid)
    if status[0].status == 'deleted by sender':
        trash=trash_tb.objects.filter(messageid=uid).delete()
        mail=message_tb.objects.filter(id=uid).delete()
    else:
        trash=trash_tb.objects.filter(messageid=uid).delete()
        mail=message_tb.objects.filter(id=uid).update(status='deleted by receiver')
    messages.add_message(request,messages.INFO,'Message Deleted From Trash')
    return redirect('viewTrash')

def viewMail(request):
    msgId=request.GET['msgid']
    message=message_tb.objects.filter(id=msgId)
    print(message[0].message)
    return JsonResponse({'subject':message[0].subject,'message':message[0].message,'username':message[0].senderid.username,'date':message[0].date,'time':message[0].time,'senderid':message[0].senderid.id,'msgId':msgId})

@never_cache
def replyToMail(request,uid):
    userid=request.session['userid']
    user=register_tb.objects.filter(id=userid)
    msgid=message_tb.object.filter(id=uid)
    senderid=msgid[0].senderid.id
    receiver=register_tb.objects.filter(id=senderid)
    return render(request,'user/composeMessage.html',{'data':user,'receiver':receiver[0].username})

def forwardMail(request,uid):
    userid=request.session['userid']
    user=register_tb.objects.filter(id=userid)
    mail=message_tb.objects.filter(id=uid)
    return render(request,'user/composeMessage.html',{'data':user,'subject':mail[0].subject,'message':mail[0].message})

def addContact(request):
    return render(request,'user/addContact.html')

def checkContactId(request):
    userid=request.session['userid']
    contact=request.GET['contact']
    user=register_tb.objects.filter(username=contact)    
    if len(user)>0:
        addContact=contact_tb.objects.filter(contactid=user[0].id,userid=userid)
        if len(addContact)>0:
            msg='exist'
        else:
            blacklist=blacklist_tb.objects.filter(blackedid=user[0].id,userid=userid)
            if len(blacklist)>0:
                msg='blacked'
            else:
                msg='valid'
    else:
        msg='do not exist'
    return JsonResponse({'valid':msg})

@never_cache
def addContactAction(request):
    user=request.session['userid']
    contact=request.POST['contactid']
    name=request.POST['name']
    remarks=request.POST['remarks']
    contactid=register_tb.objects.get(username=contact)
    userid=register_tb.objects.get(id=user)
    date=datetime.date.today()
    time=datetime.datetime.now().strftime('%H:%M')
    addContact=contact_tb(contactid=contactid,userid=userid,name=name,remarks=remarks,date=date,time=time)
    addContact.save()
    messages.add_message(request,messages.INFO,'Contact Added Successfully!')
    return redirect('addContact')

@never_cache
def userHome(request):
    userid=request.session['userid']
    user=register_tb.objects.filter(id=userid)
    return render(request,'user/userHome.html',{'data':user})

@never_cache
def addToBlacklist(request):
    return render(request,'user/addToBlacklist.html')

def checkBlackedId(request):
    userid=request.session['userid']
    blacked=request.GET['blacked']
    user=register_tb.objects.filter(username=blacked)
    if len(user)>0:
        addToBlack=blacklist_tb.objects.filter(blackedid=user[0].id,userid=userid)
        if len(addToBlack)>0:
            msg='exist'
        else:
            msg='valid'
    else:
        msg='do not exist'
    return JsonResponse({'valid':msg})

@never_cache
def addToBlacklistAction(request):
    user=request.session['userid']
    blacked=request.POST['blackedid']
    name=request.POST['name']
    remarks=request.POST['remarks']
    date=datetime.date.today()
    time=datetime.datetime.now().strftime('%H:%M')
    userid=register_tb.objects.get(id=user)
    blackedid=register_tb.objects.get(username=blacked)
    addToBlack=blacklist_tb(blackedid=blackedid,userid=userid,name=name,remarks=remarks,date=date,time=time)
    addToBlack.save()
    contact=contact_tb.objects.filter(contactid=blackedid)
    if len(contact)>0:
        contact.delete()
        print('deleted from contact')
    messages.add_message(request,messages.INFO,'Added to Blacklist Successfully!!!')
    return redirect('addToBlacklist')

@never_cache
def viewContacts(request):
    userid=request.session['userid']
    contacts=contact_tb.objects.filter(userid=userid)
    if len(contacts)>0:
        return render(request,'user/viewContacts.html',{'data':contacts})
    else:
        messages.add_message(request,messages.INFO,'No contacts in the list')
        return redirect('userHome')

def deleteFromContacts(request,uid):
    contact=contact_tb.objects.filter(id=uid).delete()
    messages.add_message(request,messages.INFO,'Deleted from contact successfully!!!')
    return redirect('viewContacts')

def addToBlacklistLink(request,uid):
    user=request.session['userid']
    userid=register_tb.objects.get(id=user)
    contact=contact_tb.objects.get(id=uid)
    date=datetime.date.today()
    time=datetime.datetime.now().strftime('%H:%M')
    blacklist=blacklist_tb(blackedid=contact.contactid,userid=userid,name=contact.name,remarks=contact.remarks,date=date,time=time)
    blacklist.save()
    contact.delete()
    messages.add_message(request,messages.INFO,'Contact added to blacklist successfully!!!')
    return redirect('viewContacts')

@never_cache
def viewBlacklist(request):
    userid=request.session['userid']
    blacklist=blacklist_tb.objects.filter(userid=userid)
    if len(blacklist)>0:
        return render(request,'user/viewBlacklist.html',{'data':blacklist})
    else:
        messages.add_message(request,messages.INFO,'No contacts in the blacklist')
        return redirect('userHome')

def removeFromBlacklist(request,uid):
    blacklist=blacklist_tb.objects.filter(id=uid).delete()
    messages.add_message(request,messages.INFO,'Contact removed from blacklist successfully!!!')
    return redirect('viewBlacklist')

def addCustomerHobbyFactor(request):
    userid=request.session['userid']
    hobby=user_hobby_tb.objects.filter(userid=userid)
    return render(request,'user/addCustomerHobbyFactor.html',{'hobby':hobby})

def getHobbyFactor(request):
    hobby=request.GET['hobby']
    factor=hobby_factor_tb.objects.filter(hobbyid=hobby)
    return render(request,'user/getHobbyFactor.html',{'data':factor})

def AddCustomerHobbyFactorAction(request):
    user=request.session['userid']
    hobby=request.POST['hobby']
    factor=request.POST['factor']
    userid=register_tb.objects.get(id=user)
    hobbyid=user_hobby_tb.objects.get(hobbyid=hobby,userid=user)
    factorid=hobby_factor_tb.objects.get(id=factor)
    custHobby=customer_hobby_tb(userid=userid,hobbyid=hobbyid,factorid=factorid)
    custHobby.save()
    messages.add_message(request,messages.INFO,'Customer Hobby Factor Added Successfully!!!')
    return redirect('addCustomerHobbyFactor')

def addCustomerAgeFactor(request):
    #currYear=str(datetime.date.today()).split('-')[0]
    currYear=datetime.date.today().year
    userid=request.session['userid']
    birthYear=register_tb.objects.filter(id=userid)[0].dob.split('-')[0]
    age=int(currYear)-int(birthYear)
    factor=age_factor_tb.objects.filter(minAge__lte=age,maxAge__gte=age)
    return render(request,'user/addCustomerAgeFactor.html',{'data':factor})

def addCustomerAgeFactorAction(request):
    userid=request.session['userid']
    factor=request.POST['factor']
    userObj=register_tb.objects.get(id=userid)
    factorObj=age_factor_tb.objects.get(id=factor)
    ageFactor=customer_age_factor_tb(userid=userObj,factorid=factorObj)
    ageFactor.save()
    messages.add_message(request,messages.INFO,'User Age Factor Added Successfully!!!')
    return redirect('addCustomerAgeFactor')

def addCustomerSeasonFactor(request):
    userid=request.session['userid']
    user=register_tb.objects.filter(id=userid)
    #month=str(datetime.date.today()).split('-')[1]
    month=datetime.date.today().month
    factors=season_country_tb.objects.filter(countryid=user[0].countryid,stateid=user[0].stateid,month=month)
    print(factors[0].id,'->',factors[0].countryid.id,' ')
    return render(request,'user/addCustomerSeasonFactor.html',{'data':factors})

def addCustomerSeasonFactorAction(request):
    userid=request.session['userid']
    userObj=register_tb.objects.get(id=userid)
    factor=request.POST['factor']
    factorObj=season_country_tb.objects.get(id=factor)
    seasonFactor=customer_season_country_tb(userid=userObj,factorid=factorObj)
    seasonFactor.save()
    messages.add_message(request,messages.INFO,'Season Factor Added Successfully!!!')
    return redirect('addCustomerSeasonFactor')

def checkCustSeasonFactor(request):
    userid=request.session['userid']
    factor=request.GET['factor']
    seasonFactor=customer_season_country_tb.objects.filter(factorid=factor,userid=userid)
    if len(seasonFactor)>0:
        msg='exist';
    else:
        msg='do not exist'
    return JsonResponse({'valid':msg})


@cache_control(no_cache=True,must_revalidate=False)
def logout(request):
    request.session.flush()
    return redirect('login')

def forgotPassword(request):
    return render(request,'user/forgotPassword.html')

def forgotPasswordAction(request):
    username=request.POST['username']
    uname=username.split('@')[0]
    user=register_tb.objects.filter(username=uname+'@mymail.com')
    if len(user)>0:
        country=country_tb.objects.all()
        return render(request,'user/forgotPswdDetail.html',{'data1':user,'data2':country})
    else:
        messages.add_message(request,messages.INFO,'Username do not exist')
        return redirect('forgotPassword')

def forgotPswdDetailAction(request):
    username=request.POST['username']
    dob=request.POST['dob']
    country=request.POST['country']
    phone=request.POST['phone']
    secQstn=request.POST['secQstn']
    secAns=request.POST['secAns']
    user=register_tb.objects.filter(dob=dob,countryid=country,phone=phone,security_question=secQstn,security_answer=secAns,username=username)
    print(user)
    if len(user)>0:
        return render(request,'user/newPassword.html',{'uname':username})
    else:
        messages.add_message(request,messages.INFO,'Details given incorrectly!!!')
        return redirect('forgotPassword')

def newPasswordAction(request):
    newPswd=request.POST['newPswd']
    confirmPswd=request.POST['confirmPswd']
    username=request.POST['username']
    if newPswd == confirmPswd:
        user=register_tb.objects.filter(username=username).update(password=confirmPswd)
        messages.add_message(request,messages.INFO,'Password Updated Successfully!!!')
        return redirect('login')
    else:
        messages.add_message(request,messages.INFO,'Both  Fields Need to be Equal')
        return redirect('forgotPassword')

@never_cache
def deleteSpam(request,uid):
    status=message_tb.objects.filter(id=uid)
    if status[0].status == 'deleted by sender':
        mail=message_tb.objects.filter(id=uid).delete()
    else:
        mail=message_tb.objects.filter(id=uid).update(status='deleted by receiver')
    messages.add_message(request,messages.INFO,'Message Deleted From Spam')
    return redirect('viewSpam')

@never_cache
def removeFromSpam(request,uid):
    mail=message_tb.objects.filter(id=uid).update(filter_status='filtered')
    messages.add_message(request,messages.INFO,'Message removed from spam')
    return redirect('viewSpam')

@never_cache
def editProfile(request):
    userid=request.session['userid']
    user=register_tb.objects.filter(id=userid)
    username=user[0].username.split('@')[0]
    country=country_tb.objects.all()
    hobby=hobby_tb.objects.all()
    userHobby=user_hobby_tb.objects.filter(userid=userid)
    print(len(userHobby))        
    states=state_tb.objects.filter(countryid=user[0].countryid)
    return render(request,'register.html',{'data1':country,'data2':user,'uname':username,'data3':hobby,'userHobby':userHobby,'states':states})
    

    







