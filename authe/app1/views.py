from datetime import datetime, timedelta
from django.shortcuts import render ,HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from . models import blood_details,hospital_details,FriendRequest, FriendList,notification,UserLocation,distance_list,eligible_hospitals,request_list
from django.views.generic.list import ListView
import json
from .utils import get_friend_request_or_false
import requests
from math import  radians, sin, cos, sqrt, atan2

# Create your views here.
def FirstPage(request):
    return render(request, 'FirstPage.html')

@login_required(login_url='login')
def blood_view(request):
    all_blood=blood_details.objects.filter(hospital=request.user)
    print(all_blood)
    noti_blood=blood_details.objects.filter(hospital=request.user)
    for blood in noti_blood:
        for_threshold=hospital_details.objects.get(hospital_id=request.user)
        if blood.amount<=for_threshold.threshold:
            blood_type_exists=notification.objects.filter(hospital=request.user, blood_type=blood.blood_type).exists()
            if blood_type_exists:
                pass
            else:
                notification.objects.create(
                    hospital=request.user,
                    blood_type=blood.blood_type,
                    amount=blood.amount,
                    remaining_days=blood.remaining_days,
                    reason="shortage"
                )
    for blood1 in noti_blood:
        if blood1.remaining_days<5:
            blood_type_exists=notification.objects.filter(hospital=request.user, blood_type=blood.blood_type).exists()
            if blood_type_exists:
                pass
            else:
                notification.objects.create(
                    hospital=request.user,
                    blood_type=blood.blood_type,
                    amount=blood.amount,
                    remaining_days=blood.remaining_days,
                    reason="expiry"
                )
    noti1=notification.objects.filter(hospital=request.user, reason="shortage")
    noti2=notification.objects.filter(hospital=request.user, reason="expiry")
    threshold=hospital_details.objects.get(hospital_id=request.user)
    renoti=notification.objects.filter(hospital=request.user, reason="shortage")
    renoti1=notification.objects.filter(hospital=request.user, reason="expiry")
    for d in renoti:
        if d.amount>=threshold.threshold:
            noti_remove=notification.objects.filter(hospital=request.user, blood_type=d.blood_type,reason="shortage")
            noti_remove.delete()
    for d1 in renoti1:
        if d1.remaining_days>5:
            noti_remove1=notification.objects.filter(hospital=request.user, blood_type=d1.blood_type,reason="expiry")
            noti_remove1.delete()
    blood_requests=request_list.objects.filter(donating_hospital=request.user)
    return render(request, 'Dashboard.html', {'all_blood': all_blood,'noti1':noti1,'noti2':noti2,'blood_requests':blood_requests})

def SignupPage(request):
    if request.method == 'POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        cpassword=request.POST.get('cpassword')
        if password != cpassword:
            return HttpResponse("password and confirm password must be same")
        else:
            my_user=User.objects.create_user(email,email,password)
            my_user.save()
            return redirect('Firstpage')
        
    return render (request,'Signup.html')


def LoginPage(request):
    if request.method == 'POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        user=authenticate(request,username=email,password=password)
        if user is not None:
            login(request,user)
            email_exists=hospital_details.objects.filter(hospital_id=request.user).exists()
            if email_exists:
                return redirect('Dashboard')
            else:
                return redirect('signup2')
        else:
            return HttpResponse("Your username or password is incorrect")
    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')

def Signup2Page(request):
    if request.method == 'POST':
        org_name = request.POST.get('org_name')
        org_state = request.POST.get('org_state')
        size=request.POST.get('sizes')
        if size=='Small':
            threshold=5
        elif size=='Medium':
            threshold=10
        elif size=='Large':
            threshold=15
        hospital_details.objects.create(
            hospital_id=request.user,
            org_name=org_name,
            org_state=org_state,
            size=size,
            threshold=threshold
        )
    
    return render (request,'Signup2.html')

def Signup3Page(request):
    if request.method == 'POST':
        blood_type = request.POST.get('blood_type')
        amount = request.POST.get('amount')
        donation_date = request.POST.get('days') 
        donation_date = datetime.strptime(donation_date, '%Y-%m-%d').date() # Assuming you calculate days elsewhere
        valid_till=donation_date+timedelta(days=42)
        remaining_days = (valid_till - datetime.now().date()).days
        # days=(today-date).days
        # days=5
        # Save the blood details with the current user's hospital
        blood_details.objects.create(
            hospital=request.user,
            blood_type=blood_type,
            amount=amount,
            donation_date=donation_date,
            valid_till=valid_till,
            remaining_days=remaining_days,
        )
    
    blood_list=blood_details.objects.filter(hospital=request.user)
    # Filter blood details associated with the current user's hospital
    user_list = UserLocation.objects.all()
    current_user_location = UserLocation.objects.get( user=request.user)
        
        # Now you can access the data of the current user in the UserLocation table
    lat1 = current_user_location.lat
    lon1 = current_user_location.lon
    distances = []  # Initialize a list to store distances
    
    for f in user_list:
        distance_exists=distance_list.objects.filter(user=request.user, donating_hospital=f.user).exists()
        if distance_exists:
            pass
        else:
            lat1_radians, lon1_radians = radians(lat1), radians(lon1)
            lat2_radians, lon2_radians = radians(f.lat), radians(f.lon)
            # Haversine formula
            dlat = lat2_radians - lat1_radians
            dlon = lon2_radians - lon1_radians
            a = sin(dlat / 2) ** 2 + cos(lat1_radians) * cos(lat2_radians) * sin(dlon / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            radius_of_earth = 6371  # Radius of Earth in kilometers
            distance = radius_of_earth * c
            distance_list.objects.create(user=request.user, donating_hospital=f.user,distance=distance)
            distances.append(distance)
    return render(request,'signup3.html',{'blood_list':blood_list})

def user_list(request):
    current_user = request.user
    user_list = User.objects.exclude(username=current_user.username)
    return render(request, 'user_list.html', {'user_list': user_list})

# def send_request(request, *args, **kwargs):
#     user=request.user
#     payload={}
#     if request.method == 'POST':
#         user_id=request.POST.get("receiver_user_id")
#         if user_id:
#             receiver=User.objects.get(pk=user_id)
#             try:
#                 friend_request=bloodrequest(sender=user,receiver=receiver)
#                 friend_request.save()
#                 # payload['result']="success"
#                 payload['response']="request sent."
#             except Exception as e:
#                 # payload['result']="error"
#                 payload['response']=str(e)
#             if payload['response']==None:
#                 payload['response']="Something went wrong."
#         else:
#             payload['response']="Unable to send friend request"
    
#     return HttpResponse(json.dumps(payload),content_type="application/json")

def register(request):
    ip=requests.get('https://api.ipify.org?format=json')
    ip_data=json.loads(ip.text)
    res=requests.get('http://ip-api.com/json/'+ip_data["ip"])
    location_data_one=res.text
    location_data=json.loads(location_data_one)
    UserLocation.objects.create(user=request.user, country=location_data['country'], city=location_data['city'],lat=location_data['lat'],lon=location_data['lon'],query=location_data['query'])
    return render(request, 'register.html',{'location_data':location_data})
    
def distance(request):
    user_list = UserLocation.objects.all()
    current_user_location = UserLocation.objects.get( user=request.user)
        
        # Now you can access the data of the current user in the UserLocation table
    lat1 = current_user_location.lat
    lon1 = current_user_location.lon
    distances = []  # Initialize a list to store distances

    for f in user_list:
        lat1_radians, lon1_radians = radians(lat1), radians(lon1)
        lat2_radians, lon2_radians = radians(f.lat), radians(f.lon)
        # Haversine formula
        dlat = lat2_radians - lat1_radians
        dlon = lon2_radians - lon1_radians
        a = sin(dlat / 2) ** 2 + cos(lat1_radians) * cos(lat2_radians) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        radius_of_earth = 6371  # Radius of Earth in kilometers
        distance = radius_of_earth * c
        distance_list.objects.create(user=request.user, donating_hospital=f.user,distance=distance)
        distances.append(distance)  # Append the calculated distance to the list
        
    return render(request, 'distance.html', {'distances': distances})

def request_form(request):
    my_dict={'A+':{'A+','A-','O+','O-'},
             'A-':{'A-','O-'},
             'B+':{'B+','B-','O+','O-'},
             'B-':{'B-','O-'},
             'AB+':{'A+','A-','B+','B-','AB+','AB-','O+','O-'},
             'AB-':{'AB-','A-','B-','O-'},
             'O+':{'O+','O-'},
             'O-':{'O-'}}
    if request.method == 'POST':
        blood_type = request.POST.get('blood_type')
        amount1 = int(request.POST.get('amount'))
        selected_option=request.POST.get('restocking')
        blood_types = my_dict.get(blood_type, set())
        blood_type_list = blood_details.objects.filter(blood_type__in=blood_types)
        threshold=hospital_details.objects.get(hospital_id=request.user)

        wt=0
        if selected_option == "1":
            wt=1
        elif selected_option=="2":
            wt=2
        elif selected_option=="3":
            wt=3
        elif selected_option=="4":
            wt=4
        
        detail_exists=eligible_hospitals.objects.filter(user=request.user,blood_type=blood_type).exists()
        if detail_exists:
            detail1=eligible_hospitals.objects.filter(user=request.user,blood_type=blood_type)
            detail1.delete()
        else:
            pass
        if 'emergency' in request.POST:
            for stock in blood_type_list:
                if (stock.amount)>amount1 :
                    distance_exist=distance_list.objects.filter(user=request.user,donating_hospital=stock.hospital).exists()
                    if distance_exist :
                        distance1=distance_list.objects.get(user=request.user,donating_hospital=stock.hospital)
                        if distance1.distance == 0.0:
                            pass
                        else:
                            total_wt=wt+(2.0/distance1.distance)
                            eligible_hospitals.objects.create(user=request.user,donating_hospital=stock.hospital,available_blood_type=stock.blood_type,amount=stock.amount,distance=distance1.distance,blood_type=blood_type,requested_amount=amount1,total_wt=total_wt)
                    else:
                        distance2=distance_list.objects.get(user=stock.hospital,donating_hospital=request.user)
                        if distance2.distance ==0.0:
                            pass
                        else:
                            total_wt=wt+(2.0/distance2.distance)
                            eligible_hospitals.objects.create(user=request.user,donating_hospital=stock.hospital,available_blood_type=stock.blood_type,amount=stock.amount,distance=distance2.distance,blood_type=blood_type,requested_amount=amount1,total_wt=total_wt)
        else:
            for stock in blood_type_list:
                if (stock.amount)>amount1 and (stock.amount-amount1)>threshold.threshold:
                    distance_exist=distance_list.objects.filter(user=request.user,donating_hospital=stock.hospital).exists()
                    if distance_exist :
                        distance1=distance_list.objects.get(user=request.user,donating_hospital=stock.hospital)
                        if distance1.distance==0.0:
                            pass
                        else:
                            total_wt=wt+(2.0/distance1.distance)
                            eligible_hospitals.objects.create(user=request.user,donating_hospital=stock.hospital,available_blood_type=stock.blood_type,amount=stock.amount,distance=distance1.distance,blood_type=blood_type,requested_amount=amount1,total_wt=total_wt)
                    else:
                        distance2=distance_list.objects.get(user=stock.hospital,donating_hospital=request.user)
                        if distance2.distance==0.0:
                            pass
                        else:
                            total_wt=wt+(2.0/distance2.distance)
                            eligible_hospitals.objects.create(user=request.user,donating_hospital=stock.hospital,available_blood_type=stock.blood_type,amount=stock.amount,distance=distance2.distance,blood_type=blood_type,requested_amount=amount1,total_wt=total_wt)
        
        hospital_list=eligible_hospitals.objects.filter(user=request.user,blood_type=blood_type)
        list_of_requests=eligible_hospitals.objects.filter(user__in=request_list.objects.values('requesting_hospital'),
                                                           blood_type__in=request_list.objects.values('blood_type'))    
        return render(request,'RequestForm.html',{'hospital_list':hospital_list, 'list_of_requests':list_of_requests})
    return render(request,'RequestForm.html')


# def hospital_list(request):
#     hospital_list=eligible_hospitals.objects.filter(user=request.user)    
#     return render(request,'HospitalList.html',{'hospital_list':hospital_list})
def update(request):
    all_blood=blood_details.objects.filter(hospital=request.user)
    return render(request,'UpdateDetails1.html',{'all_blood':all_blood})

def delete_bld(request,id):
    bl=blood_details.objects.get(id=id)
    bl.delete()
    return redirect('update')

def update_bld(request,id):
    blood=blood_details.objects.get(id=id)
    if request.method == 'POST':
        blood_type = request.POST.get('blood_type')
        amount = request.POST.get('amount')
        days = 5  # Assuming you calculate days elsewhere

        # Save the blood details with the current user's hospital
        blood=blood_details(
            id=id,
            hospital=request.user,
            blood_type=blood_type,
            amount=amount,
            days=days
        )
        blood.save()
        return redirect('update')
    return render(request, 'UpdatePage.html',{'blood':blood})

def AddBlood(request):
    all_blood=blood_details.objects.filter(hospital=request.user)
    if request.method == 'POST':
        blood_type = request.POST.get('blood_type')
        amount = request.POST.get('amount')
        donation_date = request.POST.get('days') 
        donation_date = datetime.strptime(donation_date, '%Y-%m-%d').date() # Assuming you calculate days elsewhere
        valid_till=donation_date+timedelta(days=42)
        remaining_days = (valid_till - datetime.now().date()).days
        # days=(today-date).days
        # days=5
        # Save the blood details with the current user's hospital
        blood_details.objects.create(
            hospital=request.user,
            blood_type=blood_type,
            amount=amount,
            donation_date=donation_date,
            valid_till=valid_till,
            remaining_days=remaining_days,
        )
        
        return redirect('update')
    return render(request, 'AddPage.html')

def send_request(request,id):
    hs=eligible_hospitals.objects.get(id=id)
    # rem=request_list.get(requesting_hospital=request.user,donating_hospital=hs.donating_hospital,blood_type=hs.blood_type)
    # rem.delete()
    request_list.objects.create(
        requesting_hospital=request.user,
        donating_hospital=hs.donating_hospital,
        blood_type=hs.blood_type,
        amount=hs.requested_amount,
        message="hii",
        is_accepted=0,
        is_confirmed=0
    )
    
    return redirect('request_form')

def is_accepted(request,id):
    ok=request_list.objects.get(id=id)
    ok.is_accepted=1
    ok.save()
    return redirect('Dashboard')

def declined(request,id):
    notok=request_list.objects.get(id=id)
    notok.delete()
    return redirect('Dashboard')