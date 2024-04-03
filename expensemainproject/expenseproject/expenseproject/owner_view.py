from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from app.models import Customuser, Staff

@login_required
def HOME(request):
    return render(request,'OWNER/owner_home.html')

@login_required
def ADD_STAFF(request):
    if request.method=="POST":
        profile_pic= request.FILES.get('profile_pic')
        first_name= request.POST.get('first_name') 
        last_name= request.POST.get('last_name')
        email= request.POST.get('email')
        username= request.POST.get('username')
        password= request.POST.get('password')
        address= request.POST.get('address')
        gender= request.POST.get('gender')

        if Customuser.objects.filter(email=email).exists():
            messages.warning(request,'Email Already exists')
            return redirect('add_staff')
        if Customuser.objects.filter(username=username).exists():
            messages.warning(request,"Username Already exists")
            return redirect('add_staff')
        else:
            user= Customuser(
                first_name=first_name,
                last_name=last_name,
                username = username,
                email=email,
                profile_pic = profile_pic,
                user_type= 2
            )
            user.set_password(password)
            user.save()

            staff= Staff(
                admin=user,
                address=address,
                gender=gender
            )
            staff.save()
            messages.success(request,'New staff is successfully added')
            return redirect('add_staff')
    return render(request,'OWNER/add_staff.html')

def  STAFF_VIEW(request):
    staff = Staff.objects.all()
    context={
        'staff':staff
    }
    return render(request,"OWNER/view_staff.html",context)

def STAFF_EDIT(request,id):
    staff = Staff.objects.filter(id=id)
    context={
        'staff':staff,
    }
    return render(request,'OWNER/edit_staff.html',context)

def STAFF_UPDATE(request):
    if request.method =='POST':
        staff_id= request.POST.get('staff_id')
        profile_pic= request.FILES.get('profile_pic')
        first_name= request.POST.get('first_name') 
        last_name= request.POST.get('last_name')
        email= request.POST.get('email')
        username= request.POST.get('username')
        password= request.POST.get('password')
        address= request.POST.get('address')
        gender= request.POST.get('gender')

        user= Customuser.objects.get(id= staff_id)
        user.username= username
        user.first_name= first_name
        user.last_name= last_name
        user.email = email

        if password !=None and password!= "":
                user.set_password(password)
        if profile_pic != None and profile_pic!="":
                user.profile_pic=profile_pic
        user.save()

        staff= Staff.objects.get(admin=staff_id)
        staff.gender = gender
        staff.address = address
        staff.save()

        messages.success(request,"Record updated successfully")
        return redirect('view_staff')

    return render(request,'OWNER/edit_staff.html')

def DELETE_STAFF(request,id):
     staff=Staff.objects.get(id=id)
     staff.delete()
     messages.success(request,"Record updated successfully")
     return redirect('view_staff')

     
        

        
        

        
        


 
    