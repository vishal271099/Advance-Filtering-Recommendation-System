from django.urls import path
from .views import LoginUserView, RegisterUSerView, Add_Listing, AllListView, ProfileView, IndexView,search,ContactView,AboutView,booking,showorder
from .views import deleteorder,alreadybooked ,allorder,Process_payment,Handlerequest,Checkout,flatsdata,bunglowsdata,villsdata,EmailCall,forgotpass,changepass,otp,logout

urlpatterns = [
    path('login/',LoginUserView,name = 'login'),
    path('register/',RegisterUSerView,name = 'register'),
    path('add-list/',Add_Listing,name = 'addlist'),
    path('all-list/',AllListView,name = 'alllist'),
    path('profile/<int:id>/',ProfileView,name = 'profile'),
    path('',IndexView,name = 'index'),
    path('sear/',search,name="search"),
    path('about/',AboutView,name='about'),
    path('contact/',ContactView,name='contact'),
    path('booking/<int:id>/',booking,name='booking'),
    path('showorder/',showorder,name='showorder'),
    path('deleteorder/<int:id>/',deleteorder,name='deleteorder'),
    path('allorder/',allorder,name='allorder'),
    path('check/<str:mode>/',Checkout,name='check'),
    path('emailcall/',EmailCall,name='emailcall'),
    path('payment_process/',Process_payment,name='process_payment'),
    path("handlerequest/",Handlerequest, name="handlerequest"),
    path("bunglowdata/",bunglowsdata, name="bunglowdata"),
    path("villadata/",villsdata, name="villadata"),
    path("booked/", alreadybooked, name="booked"),
    path('flatdata/',flatsdata,name='flatdata'),
    path("changepass/",changepass,name="changepass"),
    path("otp/",otp, name="otp"),
    path('forgotpass/',forgotpass,name='forgotpass'),
    path('logout/',logout,name='logout')
]
