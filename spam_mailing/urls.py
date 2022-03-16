"""spam_mailing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import url
from site_user import views as userview
from site_admin import views as adminview

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$',userview.index,name='index'),
    url(r'^register/$',userview.register,name='register'),
    url(r'^getState/$',userview.getState,name='getState'),
    url(r'^registerAction/$',userview.registerAction,name='registerAction'),
    url(r'^checkUsername/$',userview.checkUsername,name='checkUsername'),
    url(r'^login/$',userview.login,name='login'),
    url(r'^loginAction/$',userview.loginAction,name='loginAction'),
    url(r'^addHobbies/$',adminview.addHobbies,name='addHobbies'),
    url(r'^addHobbiesAction/$',adminview.addHobbiesAction,name='addHobbiesAction'),
    url(r'^checkHobby/$',adminview.checkHobby,name='checkHobby'),
    url(r'^addHobbyFactor/$',adminview.addHobbyFactor,name='addHobbyFactor'),
    url(r'^addHobbyFactorAction/$',adminview.addHobbyFactorAction,name='addHobbyFactorAction'),
    url(r'^checkHobbyFactor/$',adminview.checkHobbyFactor,name='checkHobbyFactor'),
    url(r'^addAgeFactor/$',adminview.addAgeFactor,name='addAgeFactor'),
    url(r'^checkAgeFactor/$',adminview.checkAgeFactor,name='checkAgeFactor'),
    url(r'^addAgeFactorAction$',adminview.addAgeFactorAction,name='addAgeFactorAction'),
    url(r'^addSeasons/$',adminview.addSeasons,name='addSeasons'),
    url(r'^checkSeason/$',adminview.checkSeason,name='checkSeason'),
    url(r'^addSeasonsAction/$',adminview.addSeasonsAction,name='addSeasonsAction'),
    url(r'^addSeasonFactor/$',adminview.addSeasonFactor,name='addSeasonFactor'),
    url(r'^checkSeasonFactor/$',adminview.checkSeasonFactor,name='checkSeasonFactor'),
    url(r'^addSeasonFactorAction/$',adminview.addSeasonFactorAction,name='addSeasonFactorAction'),
    url(r'^addSeasonCountry/$',adminview.addSeasonCountry,name='addSeasonCountry'),
    url(r'^getSeasonFactor/$',adminview.getSeasonFactor,name='getSeasonFactor'),
    url(r'^addSeasonCountryAction/$',adminview.addSeasonCountryAction,name='addSeasonCountryAction'),
    url(r'^checkSeasonCountry/$',adminview.checkSeasonCountry,name='checkSeasonCountry'),
    url(r'^composeMessage/$',userview.composeMessage,name='composeMessage'),
    url(r'^checkReceiver/$',userview.checkReceiver,name='checkReceiver'),
    url(r'^composeMessageAction/$',userview.composeMessageAction,name='composeMessageAction'),
    url(r'^viewSentItems/$',userview.viewSentItems,name='viewSentItems'),
    url(r'^deletedBySender/(?P<uid>\d+)/$',userview.deletedBySender,name='deletedBySender'),
    url(r'^inbox/$',userview.inbox,name='inbox'),
    url(r'^viewSpam/$',userview.viewSpam,name='viewSpam'),
    url(r'^moveToTrash/$',userview.moveToTrash,name='moveToTrash'),
    url(r'^viewTrash/$',userview.viewTrash,name='viewTrash'),
    url(r'^deleteFromTrash/(?P<uid>\d+)/$',userview.deleteFromTrash,name='deleteFromTrash'),
    url(r'^viewMail/$',userview.viewMail,name='viewMail'),
    url(r'^replyToMail/(?P<uid>\d+)/$',userview.replyToMail,name='replyToMail'),
    url(r'^forwardMail/(?P<uid>\d+)/$',userview.forwardMail,name='forwardMail'),
    url(r'^addContact/$',userview.addContact,name='addContact'),
    url(r'^checkContactId/$',userview.checkContactId,name='checkContactId'),
    url(r'^addContactAction/$',userview.addContactAction,name='addContactAction'),
    url(r'^userHome/$',userview.userHome,name='userHome'),
    url(r'^addToBlacklist/$',userview.addToBlacklist,name='addToBlacklist'),
    url(r'^checkBlackedId/$',userview.checkBlackedId,name='checkBlackedId'),
    url(r'^addToBlacklistAction/$',userview.addToBlacklistAction,name='addToBlacklistAction'),
    url(r'^viewContacts/$',userview.viewContacts,name='viewContacts'),
    url(r'^deleteFromContacts/(?P<uid>\d+)/$',userview.deleteFromContacts,name='deleteFromContacts'),
    url(r'^addToBlacklistLink/(?P<uid>\d+)/$',userview.addToBlacklistLink,name='addToBlacklistLink'),
    url(r'^viewBlacklist/$',userview.viewBlacklist,name='viewBlacklist'),
    url(r'^removeFromBlacklist/(?P<uid>\d+)/$',userview.removeFromBlacklist,name='removeFromBlacklist'),
    url(r'^addCustomerHobbyFactor/$',userview.addCustomerHobbyFactor,name='addCustomerHobbyFactor'),
    url(r'^getHobbyFactor/$',userview.getHobbyFactor,name='getHobbyFactor'),
    url(r'^AddCustomerHobbyFactorAction/$',userview.AddCustomerHobbyFactorAction,name='AddCustomerHobbyFactorAction'),
    url(r'^addCustomerAgeFactor/$',userview.addCustomerAgeFactor,name='addCustomerAgeFactor'),
    url(r'^addCustomerAgeFactorAction/$',userview.addCustomerAgeFactorAction,name='addCustomerAgeFactorAction'),
    url(r'^addCustomerSeasonFactor/$',userview.addCustomerSeasonFactor,name='addCustomerSeasonFactor'),
    url(r'^addCustomerSeasonFactorAction/$',userview.addCustomerSeasonFactorAction,name='addCustomerSeasonFactorAction'),
    url(r'^checkCustSeasonFactor/$',userview.checkCustSeasonFactor,name='checkCustSeasonFactor'),
    url(r'^logout/$',userview.logout,name='logout'),
    url(r'^forgotPassword/$',userview.forgotPassword,name='forgotPassword'),
    url(r'^forgotPasswordAction/$',userview.forgotPasswordAction,name='forgotPasswordAction'),
    url(r'^forgotPswdDetailAction/$',userview.forgotPswdDetailAction,name='forgotPswdDetailAction'),
    url(r'^newPasswordAction/$',userview.newPasswordAction,name='newPasswordAction'),
    url(r'^deleteSpam/(?P<uid>\d+)/$',userview.deleteSpam,name='deleteSpam'),
    url('^removeFromSpam/(?P<uid>\d+)/$',userview.removeFromSpam,name='removeFromSpam'),
    url('^editProfile/$',userview.editProfile,name='editProfile'),
]











