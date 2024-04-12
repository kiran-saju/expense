from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from app import models
from app.models import Bill, Customuser, PurchaseDetails, Staff,Client, Supplier
from django.db.models import Sum, F

@login_required
def OWNER_HOME(request):
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

     
#client view

def get_total_balance_per_client():
    total_bills_per_client = Bill.objects.values('client__admin__first_name', 'client__admin__last_name', 'client').annotate(total_amount=Sum('payment_amount'))
    paid_bills_per_client = Bill.objects.filter(paid_status=True).values('client').annotate(paid_amount=Sum('payment_amount'))
    balance_bills_per_client = Bill.objects.filter(paid_status=False).values('client').annotate(balance_amount=Sum('payment_amount'))
    
    # Preprocess paid and balance bills data into dictionaries for efficient lookup
    paid_amounts = {item['client']: item['paid_amount'] for item in paid_bills_per_client}
    balance_amounts = {item['client']: item['balance_amount'] for item in balance_bills_per_client}

    client_balances = {}
    for client_bill in total_bills_per_client:
        client_id = client_bill['client']
        client_name = f"{client_bill['client__admin__first_name']} {client_bill['client__admin__last_name']}"
        total_amount = client_bill['total_amount']
        
        # Use preprocessed dictionaries for efficient lookup
        balance_amount = balance_amounts.get(client_id, 0)
        paid_amount = paid_amounts.get(client_id, 0)

        client_balances[client_id] = {'client_name': client_name, 'total_amount': total_amount, 'balance_amount': balance_amount,'paid_amount':paid_amount}
    return client_balances


def view_total_balance_per_client(request):
     client_balances= get_total_balance_per_client()
     return render(request,'OWNER/view_total_balance_per_client.html',{'client_balances':client_balances})


def CLIENT_ALL_DETAILS(request):
     client=Client.objects.all()
     context={
          'client':client
     }
     return render(request,'OWNER/client_all_details.html',context)

def view_bills_owner(request):
    client = Client.objects.all()
    bills = Bill.objects.all()
    return render(request, 'OWNER/view_bill_owner.html', {'bills': bills,'client':client})     

#supplier
def OWNER_VIEW_SUPPLIER(request,id):
    supplier = Supplier.objects.get(id=id)
    purchase = PurchaseDetails.objects.all()
    total_payment = PurchaseDetails.objects.filter(paid_status=True).aggregate(total_payment=Sum('payment_amount'))['total_payment']
    total_balance = PurchaseDetails.objects.filter(paid_status=False).aggregate(total_balance=Sum('payment_amount'))['total_balance']
    context={
        'supplier': supplier,
        'purchase': purchase,
        'total_payment': total_payment,
        'total_balance': total_balance
    }
    return render(request, "OWNER/owner_view_supplier.html", context)

def SUPPLIER_DETAILS(request,id):
    supplier = get_object_or_404(Supplier,id=id)
    purchase = PurchaseDetails.objects.filter(supplier=supplier)
    return render(request, 'OWNER/supplier_details.html',{'supplier':supplier,'purchase':purchase})
    

def SUPPLIER_ALL_DETAILS(request):
     purchase=PurchaseDetails.objects.all()
     context={
          "purchase":purchase
     }
     return render(request,'OWNER/supplier_all_details.html',context)
     
    