from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from app.models import Customuser, Installment, Staff,Client,Bill

def STAFF_HOME(request):
    return render(request,'STAFF/staff_home.html')

def ADD_CLIENT(request):

    if request.method=="POST":
        profile_pic= request.FILES.get('profile_pic')
        first_name= request.POST.get('first_name') 
        last_name= request.POST.get('last_name')
        email= request.POST.get('email')
        username= request.POST.get('username')
        password= request.POST.get('password')
        address= request.POST.get('address')
        gender= request.POST.get('gender')
        project_name=request.POST.get('project_name')
        project_description=request.POST.get('project_description')

        if Customuser.objects.filter(email=email).exists():
            messages.warning(request,'Email Already exists')
            return redirect('add_client')
        if Customuser.objects.filter(username=username).exists():
            messages.warning(request,"Username Already exists")
            return redirect('add_client')
        else:
            user= Customuser(
                first_name=first_name,
                last_name=last_name,
                username = username,
                email=email,
                profile_pic = profile_pic,
                user_type= 3
            )
            user.set_password(password)
            user.save()

            client= Client(
                admin=user,
                address=address,
                gender=gender,
                project_name=project_name,
                project_description= project_description,
            )
            client.save()
            messages.success(request,'New client is successfully added')
            return redirect('add_client')
    return render(request,'STAFF/add_client.html')

def CLIENT_VIEW(request):
    client = Client.objects.all()
    context={
        'client': client
    }
    return render(request,'STAFF/view_client.html',context)

def CLIENT_EDIT(request,id):
    client = Client.objects.filter(id=id)
    context={
        'client': client
    }
    return render(request,'STAFF/edit_client.html',context)

def CLIENT_UPDATE(request):
    if request.method =='POST':
        client_id= request.POST.get('client_id')
        profile_pic= request.FILES.get('profile_pic')
        first_name= request.POST.get('first_name') 
        last_name= request.POST.get('last_name')
        email= request.POST.get('email')
        username= request.POST.get('username')
        password= request.POST.get('password')
        address= request.POST.get('address')
        gender= request.POST.get('gender')
        project_name= request.POST.get('project_name')
        project_description=request.POST.get('project_description')

        user2= Customuser.objects.get(id=client_id)
        user2.username= username
        user2.first_name= first_name
        user2.last_name= last_name
        user2.email = email
        

        if password !=None and password!= "":
                user2.set_password(password)
        if profile_pic != None and profile_pic!="":
                user2.profile_pic=profile_pic
        user2.save()

        client= Client.objects.get(admin=client_id)
        client.gender = gender
        client.address = address
        client.project_name=project_name
        client.project_description=project_description
        client.save()

        messages.success(request,"Record updated successfully")
        return redirect('view_client')

    return render(request,'STAFF/edit_client.html')


  
def DELETE_CLIENT(request,id):
     client=Client.objects.get(id=id)
     client.delete()
     messages.success(request,"Record updated successfully")
     return redirect('view_client')

def create_bill(request,id):
    bill = Bill.objects.filter(id=id)
    context={
        'bill': bill
    }
    return render(request,'STAFF/add_bill.html',context)

def generate_bill(request,id=id):
    if request.method == 'POST':
        client_name = request.POST.get('client')
        installment_number = request.POST.get('installment_number')
        payment_amount = request.POST.get('payment_amount')
        due_date = request.POST.get('due_date')
        staff_name = request.POST.get('staff_name')
        paid_status = request.POST.get('paid_status')

        # Create a new Bill object and save it
        new_bill = Bill(
            payment_amount=payment_amount,
            due_date=due_date,
            paid_status=paid_status
        )
        new_bill.save()

        new_installment= Installment(
           installment_number = installment_number  
        )
        new_installment.save()

        new_staff = Staff(
             staff_name = staff_name
        )
        new_staff.save()

        new_client = Staff(
             client_name = client_name 
        )
        new_client.save()
        return redirect('add_bill') 
   
    return render(request,'STAFF/add_bill.html')

    