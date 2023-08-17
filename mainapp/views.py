from django.shortcuts import render, redirect, HttpResponse
from .models import UserRegistration, ListingModel,ContactModel,BookingModel
from .forms import UserForm, ListForm
from django.db.models import Q
import smtplib, ssl
from django.views.decorators.csrf import csrf_exempt
from Pay import Checksum
from django.urls import reverse
import time
from datetime import datetime, timezone
import pytz
import email.message
import random
from datetime import datetime
from .filters import FilterDemo


MERCHANT_KEY = 'ZEE_g%6OOZ%bHuph'
MERCHANT_ID = 'LBTtPg05681367923553'

def RegisterUSerView(request):
    form = UserForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('login')
    return render(request, 'registration.html')

def search(request):
    try:
        serch = request.GET.get('query')
    except:
        serch = None
    if  serch:
        med = ListingModel.objects.all().filter(Q(title__icontains= serch) | Q(description__icontains = serch) | Q(apartment_type__icontains = serch)|
        Q(beds_qty__icontains = serch)|Q(baths_qty__icontains = serch)|Q(price__icontains = serch)|Q(sqrft__icontains = serch) )
        data = {
            'med':med
        }
    else:
        data={}
    return render(request,'sear.html',data)


def LoginUserView(request):
    if request.POST:
        try:
            model = UserRegistration.objects.get(email_id=request.POST['email_id'])
            if model.password == request.POST['password']:
                request.session['email'] = model.email_id
                return redirect('index')
            else:
                return HttpResponse("<a href = ''>Incorrect details</a>")
        except:
            return HttpResponse("<a href = ''>Incorrect details</a>")
    return render(request, 'login.html')


def Add_Listing(request):
    if 'email' in request.session.keys():
        user_model = UserRegistration.objects.get(email_id=request.session['email'])

        
        if request.POST:
            form = ListForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                list_model = ListingModel.objects.latest('id')
                list_model.email_id = user_model.email_id
                list_model.save()
                return redirect('alllist')
            
        return render(request, 'add_list.html')
    else:
        return redirect('login')

def villsdata(request):
    if 'email' in request.session:
        model=ListingModel.objects.filter(apartment_type='Villas')
        return render(request,'villas.html',{'model':model})
    else:
        model=ListingModel.objects.filter(apartment_type='Villas')
        return render(request,'villas.html',{'model':model})

def bunglowsdata(request):
    if 'email' in request.session:
        model=ListingModel.objects.filter(apartment_type='Bunglows')
        return render(request,'bunglows.html',{'model':model})
    else:
        model=ListingModel.objects.filter(apartment_type='Bunglows')
        return render(request,'bunglows.html',{'model':model})
    
def flatsdata(request):
    if 'email' in request.session:
        model=ListingModel.objects.filter(apartment_type='Flats')
        return render(request,'flats.html',{'model':model}) 
    else:
        model=ListingModel.objects.filter(apartment_type='Flats')
        return render(request,'flats.html',{'model':model})  

def AllListView(request):
    if request.GET:
        try:
            q = request.GET.get('search_data')
            print(q)
            print("Q Call")
        except:
            q = None
            print("No Q")
        
        if q != None and request.GET['search_data'] != None:
            apartmenttype = ListingModel.objects.all()[:3]
            apartment = ListingModel.objects.filter(Q(title__icontains=q) | Q(address__icontains=q) | Q(description__icontains=q))
            print("Q Collect")
            return render(request, 'listing.html', {'apartment1':apartment,'apartment':apartmenttype})
        else: 
            search = request.GET.get('text')
            pricefilter = request.GET.get('pricefilter')
            apartmenttype = ListingModel.objects.all()[:3]
            print("Q other Data")
            apartment = request.GET.get('apartment_type')
            if apartment != '':
                list_model = ListingModel.objects.filter(apartment_type=apartment).order_by('price').filter(verified=True)
                user_filter = FilterDemo(request.GET, queryset=list_model)

            if pricefilter == 'low':
                list_model = ListingModel.objects.all().order_by('price').filter(verified=True)
                user_filter = FilterDemo(request.GET, queryset=list_model)
            elif pricefilter == 'high':
                list_model = ListingModel.objects.all().order_by('-price').filter(verified=True)
                user_filter = FilterDemo(request.GET, queryset=list_model)
            else:

                list_model = ListingModel.objects.all().filter(verified=True)
                user_filter = FilterDemo(request.GET, queryset=list_model)

    else:
        print("Q POST")
        apartmenttype = ListingModel.objects.all()[:3]
        print("Q POst DAta")
        list_model = ListingModel.objects.all().filter(verified=True)
        user_filter = FilterDemo(request.GET, queryset=list_model)

    return render(request, 'listing.html', {'all_list': user_filter,'apartment':apartmenttype})

def IndexView(request):
    if 'email' in request.session.keys():
        return render(request,'index.html')
    else:
        return render(request,'index.html')


def AboutView(request):
    if 'email' in request.session:
        return render(request,'about.html')
    else:
        return render(request,'about.html')


def ContactView(request):
    if 'email' in request.session:
        if request.POST:
            model=ContactModel()
            model.Name=request.POST['Name']
            model.Email=request.POST['Email']
            model.Phone=request.POST['Phone']
            model.Message=request.POST['Message']
            model.save()
            subject ="Thanks for getting in touch. We are on it."
            body = ("Thanks {} for the email !!!.\n\n We will response you within 24 hr.".format(model.Name))
            msg = ("Subject : {} \n\n {}".format(subject,body))
            mail = smtplib.SMTP('smtp.gmail.com', 587)
            mail.ehlo()
            mail.starttls()
            mail.login('panchalvishal2710@gmail.com', 'vs150379')
            mail.sendmail('panchalvishal2710@gmail.com',model.Email, msg)
            mail.close()
            return redirect('index')
    return render(request,'contact.html')


def ProfileView(request,id):
    if 'email' in request.session:
        model = ListingModel.objects.get(id=id)
        model.view_count += 1
        model.save()
    return render(request,'property-single.html',{'data':model})


def booking(request,id):
    if 'email' in request.session:
        user=UserRegistration.objects.get(email_id=request.session['email'])
        pro=ListingModel.objects.get(id=id)
        print(pro)
        if pro.is_avaliable==True:
            model=BookingModel.objects.create(user=user,estate=pro,Cost=pro.price)
            model.save()
            pro.is_avaliable=False
            pro.save()
            return redirect('showorder')
        else:
            return redirect("booked")
    else:
        return redirect('login')

def showorder(request):
    if 'email' in request.session:
        tot=0
        user = UserRegistration.objects.get(email_id=request.session['email'])
        show_data = BookingModel.objects.all().filter(user=user)
        for i in show_data:
            tot+=i.Cost
        print(tot)
        request.session['Total']=tot
        return render(request,'showorder.html',{'data':show_data})
    else:
        return redirect('login')
    

def deleteorder(request,id):
    if request.session.has_key('email'):
        model=BookingModel.objects.get(id=id)
        model.delete()
        return redirect('alllist')
    return render(request,'showorder.html')

def allorder(request):
    if 'email' in request.session:
        model=BookingModel.objects.all()
        model.delete()
    return render(request,'showorder.html',)

def Checkout(request,mode):
    tz= pytz.timezone('Asia/Kolkata')
    time_now = datetime.now(timezone.utc).astimezone(tz)
    millis = int(time.mktime(time_now.timetuple()))
    order_id = "Order"+str(millis)
    request.session['Order_id'] = order_id
    
    if mode == 'pytm':
        return redirect('process_payment')
    else:
        return redirect('paycash')
    
def Process_payment(request):
    email_id=UserRegistration.objects.get(email_id=request.session['email'])
    show_data = BookingModel.objects.all().filter(user=email_id)
    amo = request.session['Total']
    host = request.get_host()
    param_dict = {
        'MID': MERCHANT_ID,
        'ORDER_ID': str(email_id),
        'TXN_AMOUNT': str(amo),
        'CUST_ID': 'panchal_rahul',
        'INDUSTRY_TYPE_ID': 'Retail',
        'WEBSITE': 'WEBSTAGING',
        'CHANNEL_ID': 'WEB',
        'CALLBACK_URL':'http://{}{}'.format(host,reverse('handlerequest')),
    }
    param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
    return render(request, 'paytm.html', {'param_dict': param_dict})


def EmailCall(request):
    user = UserRegistration.objects.get(email_id=request.session['email'])
    show_data = BookingModel.objects.all().filter(user=user)
    amo = request.session['Total']
    print(amo)
    order_id = request.session['Order_id']
    
    my_email = "panchalvishal2710@gmail.com"
    my_pass = "vs150379"
    fr_email = user
    
    server = smtplib.SMTP('smtp.gmail.com',587)
    mead_data = ""
    front = """
    <!DOCTYPE html>
    <html>
        <body><center>
            <div>
                <h2>Name : """ + user.full_name + """</h2>
                <h2>Email : """ + user.email_id + """</h2>
                <h2>Order No: """ + order_id + """</h2>
            </div>
            <div>"""
    for i in show_data: 
        mead_data += """<tr>
        <p>Hi,"""+ user.full_name + """ you had booked """ + str(i.estate.title) + """ on rent today. </p>
        </tr> """
    ended="""
    </center>
        <p>Thank you for using Rental system...</p>
        </body>
    </html>
    """
    email_content = front + mead_data + ended
    print(email_content)
    
    msg = email.message.Message()
    msg['Subject'] = 'Booking the property confirmation!!' 
    msg['From'] = my_email
    msg['To'] = fr_email
    password = my_pass
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(email_content)
    s = smtplib.SMTP('smtp.gmail.com',587)
    s.starttls()
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string())

    show_data.delete()
        
    return redirect('index')

@csrf_exempt
def Handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
            return redirect('emailcall')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'paymentstatus.html', {'response': response_dict})

        
def forgotpass(request):
    Email=request.POST.get('Email')
    request.session['Email']=Email
    if Email == None:
        return render(request,'email.html')

    otp=''
    rand1=random.choice('1234567890')
    rand2=random.choice('1234567890')
    rand3=random.choice('1234567890')
    rand4=random.choice('1234567890')

    otp=rand1+rand2+rand3+rand4
    print(otp)
    request.session['otp']=otp

    port = 465
    password = "vs150379"
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL("smtp.gmail.com",port,context=context)
    server.login("panchalvishal2710@gmail.com",password)
    server.sendmail("panchalvishal2710@gmail.com",Email,otp)
    server.quit()
    return redirect('otp')
    return render(request,'email.html')

def otp(request):
    if 'email' in request.session:
        otp=request.session['otp']
        try:
            obj=request.POST.get('otp')
            if obj==None:
                return render(request,'otp.html')
            if obj == request.POST.get('otp'):
                return redirect('changepass')
            else:
                return HttpResponse('<a href="">Wrong Otp Entered.</a>')
        except:
            return redirect('login')
    return render(request,'otp.html')

def changepass(request):
    new=request.POST.get('password')
    if new==None:
        return render(request,'change.html')
    user = UserRegistration.objects.get(email_id=request.session['email'])
    user.password=new
    user.save()
    return redirect('login')
    return render(request,'change.html')


def logout(request):
    if 'email' in request.session:
        del request.session['email']
        return redirect('login')
    else:
        return redirect('login')

def alreadybooked(request):

    return render(request, "booked.html") 