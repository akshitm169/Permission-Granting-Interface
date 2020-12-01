from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from datetime import datetime
from .models import *

rooms_dict={'Lecture Hall-1':'New Academic Block','Lecture Hall-2':'New Academic Block','Lecture Hall-3':'New Academic Block','Lecture Hall-4':'Computer Science Department','Lecture Hall-5':'Computer Science Department','Lecture Hall-6':'Computer Science Department','Lecture Hall-7':'Electronics Department','Lecture Hall-8':'Electronics Department','Lecture Hall-9':'Electronics Department','Lecture Hall-10':'Electronics Department'}

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


# Create your views here.
def index(request):
    return render(request,'pgi_app/index.html')


def user_login(request):
    if request.method=='POST':
        curr_username=request.POST.get('username')
        curr_password=request.POST.get('password')
        curr_designation=request.POST.get('designation')
        user=authenticate(username=curr_username,password=curr_password)

        if user:
            curr_user=authority_db.objects.get(user=user)
            if curr_designation==curr_user.designation:
                if user.is_active:
                    login(request,user)
                    if curr_designation=='Club secretary':
                        return student_profile(request)
                    elif curr_designation=='Club Office In-charge':
                        return oi_profile(request)
                    elif curr_designation=='Security In-charge':
                        return si_profile(request)
                    elif curr_designation=='Guard In-charge':
                        return guard_profile(request)
                else:
                    return HttpResponse("ACCOUNT NOT ACTIVE!!")
            else:
                messages.error(request,'username or password not correct')
                return HttpResponseRedirect(request.path_info)
        else:
            messages.error(request,'username or password not correct')
            return HttpResponseRedirect(request.path_info)



    return render(request,'pgi_app/user_login.html')



@login_required
def si_profile(request):
    curr_user=authority_db.objects.get(user=request.user)
    curr_mail=request.user.email
    curr_fn=request.user.first_name
    curr_ln=request.user.last_name
    #print(curr_mail,curr_club,curr_fn,curr_ln)
    my_dict={'si':curr_fn,'mail':curr_mail,'ln':curr_ln}
    return render(request,'pgi_app/si_profile.html',my_dict)






@login_required
def oi_profile(request):
    curr_user=authority_db.objects.get(user=request.user)
    curr_mail=request.user.email
    curr_fn=request.user.first_name
    curr_ln=request.user.last_name
    curr_club=curr_user.club
    #print(curr_mail,curr_club,curr_fn,curr_ln)
    my_dict={'oi':curr_fn,'club':curr_club,'mail':curr_mail,'ln':curr_ln}
    return render(request,'pgi_app/oi_profile.html',my_dict)




@login_required
def guard_profile(request):
    curr_user=authority_db.objects.get(user=request.user)
    curr_mail=request.user.email
    curr_fn=request.user.first_name
    curr_ln=request.user.last_name
    #print(curr_mail,curr_club,curr_fn,curr_ln)
    my_dict={'guard':curr_fn,'mail':curr_mail,'ln':curr_ln}
    return render(request,'pgi_app/guard_profile.html',my_dict)






@login_required
def student_profile(request):
    curr_user=authority_db.objects.get(user=request.user)
    curr_mail=request.user.email
    curr_fn=request.user.first_name
    curr_ln=request.user.last_name
    curr_club=curr_user.club
    #print(curr_mail,curr_club,curr_fn,curr_ln)
    my_dict={'secy':curr_fn,'club':curr_club,'mail':curr_mail,'ln':curr_ln,'imagee':curr_user}
    return render(request,'pgi_app/student_profile.html',my_dict)




@login_required
def check_status(request):
    curr_username=request.user.username
    requests_by_user=request_db.objects.filter(authority=request.user).exclude(status='-1')
    # if len(requests_by_user)==0:
    #     return HttpResponse('oops,you haven\'t made any bookings')
    req_dict={'requests':requests_by_user}
    if request.method=='POST':
        req_id=request.POST.get('cancel')
        req_to_cancel=request_db.objects.get(request_id=req_id)
        req_to_cancel.status='-1'
        req_to_cancel.save()
        return HttpResponseRedirect(request.path_info)
    # curr_user=authority_db.objects.get(user=request.user)
    # curr_mail=request.user.email
    # curr_fn=request.user.first_name
    # curr_ln=request.user.last_name
    # curr_club=curr_user.club
    # #print(curr_mail,curr_club,curr_fn,curr_ln)
    # my_dict={'secy':curr_fn,'club':curr_club,'mail':curr_mail,'ln':curr_ln}
    return render(request,'pgi_app/check_status.html',context=req_dict)




@login_required
def oi_request(request):
    curr_username=request.user.username
    oi_name=request.user.first_name +" "+request.user.last_name
    curr_club=authority_db.objects.get(user=request.user).club
    user_name=str(authority_db.objects.get(club=curr_club,designation='Club secretary'))
    user_obj=User.objects.get(username=user_name)
    secy_email=user_obj.email
    secy_name=user_obj.first_name+" " +user_obj.last_name
    requests_by_user=request_db.objects.filter(authority=user_obj,status='0')
    req_dict={'requests':requests_by_user}
    if request.method=='POST':
        request_id_for_oi_acc=request.POST.get('accept_verdict')
        request_id_for_oi_dec=request.POST.get('decline_verdict')
        if request_id_for_oi_dec==None:
            req_for_oi=request_db.objects.get(request_id=request_id_for_oi_acc)
            curr_date=str(req_for_oi.date)
            curr_slot=str(req_for_oi.slot)
            curr_room=str(req_for_oi.room)
            req_for_oi.status=1
            req_for_oi.save()

            si_user_name=str(authority_db.objects.get(designation='Security In-charge'))
            si_user_obj=User.objects.get(username=si_user_name)
            si_email=si_user_obj.email
            si_name=si_user_obj.first_name+" "+si_user_obj.last_name


            message1='This is automated generated message. Please Don\'t reply to this.'+'\n'+'\n'+ 'Dear '+ secy_name+',\n'+'Your Club Office In-charge has accepted your room booking request for meeting/workshop and it has been forwarded to Security In-charge. You can login to PGI website to view it. Details of request are below. \n'+'\n'+'Club Office Incharge: '+ oi_name +'\n' + 'Club: '+curr_club +'\n' +'Date of booking: '+curr_date+'\n'+  'Slot of booking: '+curr_slot+'\n'+  'Venue of booking: '+curr_room+'\n'+ '\n'+ 'Thank You.'


            message2='This is automated generated message. Please Don\'t reply to this.'+'\n'+'\n'+ 'Dear '+ si_name+',\n'+'You have got a request for a room booking by one of the club secretaries for meeting/workshop. You can login to PGI website to either accept or decline it. Details of request are below. \n'+'\n'+ 'Club Secretary: '+ secy_name +'\n'   +'Club Office Incharge: '+ oi_name +'\n' + 'Club: '+curr_club +'\n' +'Date of booking: '+curr_date+'\n'+  'Slot of booking: '+curr_slot+'\n'+  'Venue of booking: '+curr_room+'\n'+ '\n'+ 'Thank You.'

            try:
                send_mail(
                'PGI Notification',
                message1,
                'akshitmonga6@gmail.com',
                [secy_email],
                fail_silently=False,
            )
            except:
                pass

            try:
                send_mail(
                'PGI Notification',
                message2,
                'akshitmonga6@gmail.com',
                [si_email],
                fail_silently=False,
            )
            except:
                pass





        else:
            req_for_oi=request_db.objects.get(request_id=request_id_for_oi_dec)
            req_for_oi.status=2
            req_for_oi.save()

            curr_date=str(req_for_oi.date)
            curr_slot=str(req_for_oi.slot)
            curr_room=str(req_for_oi.room)


            message3='This is automated generated message. Please Don\'t reply to this.'+'\n'+'\n'+ 'Dear '+ secy_name+',\n'+'Your Club Office In-charge has declined your room booking request for meeting/workshop. You can login to PGI website to view it. Details of request are below. \n'+'\n'+'Club Office Incharge: '+ oi_name +'\n' + 'Club: '+curr_club +'\n' +'Date of booking: '+curr_date+'\n'+  'Slot of booking: '+curr_slot+'\n'+  'Venue of booking: '+curr_room+'\n'+ '\n'+ 'Thank You.'


            try:
                send_mail(
                'PGI Notification',
                message3,
                'akshitmonga6@gmail.com',
                [secy_email],
                fail_silently=False,
            )
            except:
                pass






        return HttpResponseRedirect(request.path_info)
    return render(request,'pgi_app/oi_request.html',req_dict)




@login_required
def si_request(request):
    all_req=request_db.objects.filter(status='1')
    my_dict={}
    for i in all_req:
        user_obj=User.objects.get(username=str(i.authority))
        full_name=str(user_obj.first_name) + " " + str(user_obj.last_name)
        curr_club=authority_db.objects.get(user=user_obj).club
        my_dict[i]=(full_name,curr_club)

        guard_user_name=str(authority_db.objects.get(designation='Guard In-charge'))
        guard_user_obj=User.objects.get(username=guard_user_name)
        guard_email=guard_user_obj.email
        guard_name=guard_user_obj.first_name+" "+guard_user_obj.last_name

    req_dict={'requests':my_dict}
    if request.method=='POST':
        request_id_for_si_acc=request.POST.get('accept_verdict')
        request_id_for_si_dec=request.POST.get('decline_verdict')



        if request_id_for_si_dec==None:
            req_for_si=request_db.objects.get(request_id=request_id_for_si_acc)
            req_for_si.status=3
            req_for_si.save()
            curr_date=str(req_for_si.date)
            curr_slot=str(req_for_si.slot)
            curr_room=str(req_for_si.room)
            secy_obj=req_for_si.authority
            secy_name=str(secy_obj.first_name)+" "+str(secy_obj.last_name)
            secy_email=str(secy_obj.email)
            curr_club=authority_db.objects.get(user=secy_obj).club

            oi_user_name=str(authority_db.objects.get(club=curr_club,designation='Club Office In-charge'))
            oi_obj=User.objects.get(username=oi_user_name)
            oi_name=str(oi_obj.first_name)+" "+str(oi_obj.last_name)
            oi_email=str(oi_obj.email)


            message1='This is automated generated message. Please Don\'t reply to this.'+'\n'+'\n'+ 'Dear '+ secy_name+',\n'+'The Security In-charge has accepted your room booking request for meeting/workshop. You can use that room and you will be responsible for any happenings there. You can login to PGI website to view it. Details of request are below. \n'+'\n'+'Club Office Incharge: '+ oi_name +'\n' + 'Club: '+curr_club +'\n' +'Date of booking: '+curr_date+'\n'+  'Slot of booking: '+curr_slot+'\n'+  'Venue of booking: '+curr_room+'\n'+ '\n'+ 'Thank You.'

            message2='This is automated generated message. Please Don\'t reply to this.'+'\n'+'\n'+ 'Dear '+ oi_name+',\n'+'The Security In-charge has accepted the room booking request you put forward in behalf of your club secretary. You can login to PGI website to view it. Details of request are below. \n'+'\n'+'Club Secretary: '+ secy_name +'\n' + 'Club: '+curr_club +'\n' +'Date of booking: '+curr_date+'\n'+  'Slot of booking: '+curr_slot+'\n'+  'Venue of booking: '+curr_room+'\n'+ '\n'+ 'Thank You.'

            message3='This is automated generated message. Please Don\'t reply to this.'+'\n'+'\n'+ 'Dear '+ guard_name+',\n'+'The Security In-charge has accepted a room booking request put forward by one of the club secretaries. You can login to PGI website to view it. Details of request are below. \n'+'\n'+'Club Secretary: '+ secy_name +'\n' + 'Club: '+curr_club +'\n' +'Date of booking: '+curr_date+'\n'+  'Slot of booking: '+curr_slot+'\n'+  'Venue of booking: '+curr_room+'\n'+ '\n'+ 'Thank You.'

            try:
                send_mail(
                'PGI Notification',
                message1,
                'akshitmonga6@gmail.com',
                [secy_email],
                fail_silently=False,
            )
            except:
                pass

            try:
                send_mail(
                'PGI Notification',
                message2,
                'akshitmonga6@gmail.com',
                [oi_email],
                fail_silently=False,
            )
            except:
                pass

            try:
                send_mail(
                'PGI Notification',
                message3,
                'akshitmonga6@gmail.com',
                [guard_email],
                fail_silently=False,
            )
            except:
                pass










        else:
            req_for_si=request_db.objects.get(request_id=request_id_for_si_dec)
            req_for_si.status=4
            req_for_si.save()

            curr_date=str(req_for_si.date)
            curr_slot=str(req_for_si.slot)
            curr_room=str(req_for_si.room)

            secy_obj=req_for_si.authority
            secy_name=str(secy_obj.first_name)+" "+str(secy_obj.last_name)
            secy_email=str(secy_obj.email)
            curr_club=authority_db.objects.get(user=secy_obj).club

            oi_user_name=str(authority_db.objects.get(club=curr_club,designation='Club Office In-charge'))
            oi_obj=User.objects.get(username=oi_user_name)
            oi_name=str(oi_obj.first_name)+" "+str(oi_obj.last_name)
            oi_email=str(oi_obj.email)


            message1='This is automated generated message. Please Don\'t reply to this.'+'\n'+'\n'+ 'Dear '+ secy_name+',\n'+'The Security In-charge has declined your room booking request for meeting/workshop. You can login to PGI website to view it. Details of request are below. \n'+'\n'+'Club Office Incharge: '+ oi_name +'\n' + 'Club: '+curr_club +'\n' +'Date of booking: '+curr_date+'\n'+  'Slot of booking: '+curr_slot+'\n'+  'Venue of booking: '+curr_room+'\n'+ '\n'+ 'Thank You.'

            message2='This is automated generated message. Please Don\'t reply to this.'+'\n'+'\n'+ 'Dear '+ oi_name+',\n'+'The Security In-charge has declined the room booking request you put forward in behalf of your club secretary. You can login to PGI website to view it. Details of request are below. \n'+'\n'+'Club Secretary: '+ secy_name +'\n' + 'Club: '+curr_club +'\n' +'Date of booking: '+curr_date+'\n'+  'Slot of booking: '+curr_slot+'\n'+  'Venue of booking: '+curr_room+'\n'+ '\n'+ 'Thank You.'



            try:
                send_mail(
                'PGI Notification',
                message1,
                'akshitmonga6@gmail.com',
                [secy_email],
                fail_silently=False,
            )
            except:
                pass


            try:
                send_mail(
                'PGI Notification',
                message2,
                'akshitmonga6@gmail.com',
                [oi_email],
                fail_silently=False,
            )
            except:
                pass










        return HttpResponseRedirect(request.path_info)
    return render(request,'pgi_app/si_request.html',req_dict)




@login_required
def guard_request(request):
    all_req=request_db.objects.filter(status='3')
    my_dict={}
    for i in all_req:
        user_obj=User.objects.get(username=str(i.authority))
        full_name=str(user_obj.first_name) + " " + str(user_obj.last_name)
        curr_club=authority_db.objects.get(user=user_obj).club
        my_dict[i]=(curr_club,full_name)
        # print(my_dict)
    req_dict={'requests':my_dict}
    return render(request,'pgi_app/guard_request.html',req_dict)





@login_required
def available_rooms(request):
    curr_username=request.user.username
    curr_club=authority_db.objects.get(user=request.user).club
    if request.method=='POST':
        if 'check' in request.POST:
            curr_date=request.POST.get('date')
            if curr_date<=datetime.today().strftime('%Y-%m-%d'):
                messages.error(request,'Enter a Valid Date')
                return HttpResponseRedirect(request.path_info)
            curr_slot=request.POST.get('slot')
            rooms_obj=request_db.objects.filter(date=curr_date,slot=curr_slot).exclude(status='-1').exclude(status='1').exclude(status='4')
            rooms_to_exclude=[]
            # print(rooms_obj)
            for i in rooms_obj:
                # print(i.room)
                # print(type(i.room))
                rooms_to_exclude.append(str(i.room))
                # print(rooms_to_exclude)
            all_rooms=[]
            all_rooms_obj=room_db.objects.all()
            for i in all_rooms_obj:
                all_rooms.append(i.room_number)
            available_room=list(set(all_rooms)-set(rooms_to_exclude))
            available_room=sorted(available_room,key=lambda x: int(x[13:]))
            rooms_show_dict={}
            for i in available_room:
                rooms_show_dict[i]=rooms_dict[i]
            Every_dict={'date':curr_date,'slot':curr_slot,'rooms_show':rooms_show_dict}
            return render(request,'pgi_app/available_rooms.html',context=Every_dict)
        else:
            curr_date=request.POST.get('date_hid')
            curr_slot=request.POST.get('slot_hid')
            curr_room=request.POST.get('room_booked')
            oi_user_name=str(authority_db.objects.get(club=curr_club,designation='Club Office In-charge'))
            oi_user_obj=User.objects.get(username=oi_user_name)
            to_email=oi_user_obj.email
            to_name=oi_user_obj.first_name+" " +oi_user_obj.last_name
            print(curr_date,curr_room,curr_slot)
            max_count=0
            all_req=request_db.objects.all()
            for i in all_req:
                if i.request_id>max_count:
                    max_count=i.request_id
            max_count+=1
            user_foreign_obj=User.objects.get(username=curr_username)
            print(user_foreign_obj.first_name)
            room_foreign=room_db.objects.get(room_number=curr_room)
            new_req_obj=request_db(request_id=max_count,authority=user_foreign_obj,date=curr_date,slot=curr_slot,room=room_foreign,status=0)
            new_req_obj.save()


            try:
                message='This is automated generated message. Please Don\'t reply to this.'+'\n'+'\n'+ 'Dear '+ to_name+',\n'+'Your Club Secretary has requested a room booking for meeting/workshop. You can login to PGI website to accept or decline it. Details of request are below. \n'+'\n'+'Club Secretary: '+ user_foreign_obj.first_name +' '+ user_foreign_obj.last_name +'\n' + 'Club: '+curr_club +'\n' +'Date of booking: '+curr_date+'\n'+  'Slot of booking: '+curr_slot+'\n'+  'Venue of booking: '+curr_room+'\n'+ '\n'+ 'Thank You.'
                send_mail(
                'PGI Notification',
                message,
                'akshitmonga6@gmail.com',
                [to_email],
                fail_silently=False,
            )
            except:
                pass






            rooms_obj=request_db.objects.filter(date=curr_date,slot=curr_slot).exclude(status='-1')
            rooms_to_exclude=[]
            # print(rooms_obj)
            for i in rooms_obj:
                # print(i.room)
                # print(type(i.room))
                rooms_to_exclude.append(str(i.room))
                # print(rooms_to_exclude)
            all_rooms=[]
            all_rooms_obj=room_db.objects.all()
            for i in all_rooms_obj:
                all_rooms.append(i.room_number)
            available_rooms=list(set(all_rooms)-set(rooms_to_exclude))
            available_rooms=sorted(available_rooms,key=lambda x: int(x[13:]))
            rooms_show_dict={}
            for i in available_rooms:
                rooms_show_dict[i]=rooms_dict[i]
            Every_dict={'date':curr_date,'slot':curr_slot,'rooms_show':rooms_show_dict}
            return render(request,'pgi_app/available_rooms.html',context=Every_dict)









@login_required
def make_request(request):
    curr_username=request.user.username
    if request.method =='POST':
        # curr_date=request.POST.get('date')
        # curr_slot=request.POST.get('slot')
        # rooms_obj=request_db.objects.filter(date=curr_date,slot=curr_slot).exclude(status='-1')
        # rooms_to_exclude=[]
        # # print(rooms_obj)
        # for i in rooms_obj:
        #     # print(i.room)
        #     # print(type(i.room))
        #     rooms_to_exclude.append(str(i.room))
        #     # print(rooms_to_exclude)
        # all_rooms=[]
        # all_rooms_obj=room_db.objects.all()
        # for i in all_rooms_obj:
        #     all_rooms.append(i.room_number)
        # available_room=list(set(all_rooms)-set(rooms_to_exclude))
        # available_room=sorted(available_room,key=lambda x: int(x[13:]))
        # rooms_show_dict={}
        # for i in available_room:
        #     rooms_show_dict[i]=rooms_dict[i]
        # Every_dict={'date':curr_date,'slot':curr_slot,'rooms_show':rooms_show_dict}
        return available_rooms(request)
    return render(request,'pgi_app/make_request.html')
