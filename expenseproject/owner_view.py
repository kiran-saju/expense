from django.http import JsonResponse
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from app import models
from app.models import Bill, Customuser, PurchaseDetails, Staff,Client, Supplier
from django.db.models import Sum, F
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
@login_required
def OWNER_HOME(request):
    total_payment_amount = Bill.objects.aggregate(total_payment=Sum('payment_amount'))['total_payment']
    
    client_total_paid_amount = Bill.objects.filter(paid_status=True).aggregate(total_sum=Sum('payment_amount'))['total_sum']
    
    client_total_balance_payment= Bill.objects.filter(paid_status=False).aggregate(total_sum=Sum('payment_amount'))['total_sum']
    
    total_suppliers_charge = PurchaseDetails.objects.aggregate(total_sum=Sum('payment_amount'))['total_sum']

    
    total_balance_to_supplier =  PurchaseDetails.objects.filter(paid_status=False).aggregate(total_sum=Sum('payment_amount'))['total_sum']

    total_payment_supplier = PurchaseDetails.objects.filter(paid_status=True).aggregate(total_sum=Sum('payment_amount'))['total_sum']

    context={
        'client_total_paid_amount':client_total_paid_amount,
        'client_total_balance_payment':client_total_balance_payment,
        "total_payment_amount":total_payment_amount,
        'total_suppliers_charge':total_suppliers_charge,
        'total_payment_supplier':total_payment_supplier,
        'total_balance_to_supplier':total_balance_to_supplier,
    }
    
    return render(request,'OWNER/owner_home.html',context)

@login_required
def ADD_STAFF(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name') 
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')

        # Validate email
        try:
            validate_email(email)
        except ValidationError:
            messages.warning(request, 'Invalid email format')
            return redirect('add_staff')

        # Check password length
        if len(password) < 8:
            messages.warning(request, 'Password must be at least 8 characters long')
            return redirect('add_staff')

        if Customuser.objects.filter(email=email).exists():
            messages.warning(request, 'Email Already exists')
            return redirect('add_staff')
        if Customuser.objects.filter(username=username).exists():
            messages.warning(request, "Username Already exists")
            return redirect('add_staff')
        else:
            user = Customuser(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                profile_pic=profile_pic,
                user_type=2
            )
            user.set_password(password)
            user.save()

            staff = Staff(
                admin=user,
                address=address,
                gender=gender
            )
            staff.save()
            messages.success(request, 'New staff is successfully added')
            return redirect('add_staff')
    return render(request, 'OWNER/add_staff.html')

@login_required
def  STAFF_VIEW(request):
    staff = Staff.objects.all()
    context={
        'staff':staff
    }
    return render(request,"OWNER/view_staff.html",context)

@login_required
def STAFF_EDIT(request,id):
    staff = Staff.objects.filter(id=id)
    context={
        'staff':staff,
    }
    return render(request,'OWNER/edit_staff.html',context)

@login_required
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

@login_required
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
    
    
    paid_amounts = {item['client']: item['paid_amount'] for item in paid_bills_per_client}
    balance_amounts = {item['client']: item['balance_amount'] for item in balance_bills_per_client}

    client_balances = {}
    for client_bill in total_bills_per_client:
        client_id = client_bill['client']
        client_name = f"{client_bill['client__admin__first_name']} {client_bill['client__admin__last_name']}"
        total_amount = client_bill['total_amount']
        
      
        balance_amount = balance_amounts.get(client_id, 0)
        paid_amount = paid_amounts.get(client_id, 0)

        client_balances[client_id] = {'client_name': client_name, 'total_amount': total_amount, 'balance_amount': balance_amount,'paid_amount':paid_amount}
    return client_balances

@login_required
def view_total_balance_per_client(request):
     client_balances= get_total_balance_per_client()
     return render(request,'OWNER/view_total_balance_per_client.html',{'client_balances':client_balances})

# views.py



@login_required
def CLIENT_ALL_DETAILS(request):
     client=Client.objects.all()
     context={
          'client':client
     }
     return render(request,'OWNER/client_all_details.html',context)

@login_required
def view_bills_owner(request):
    client = Client.objects.all()
    bills = Bill.objects.all()
    return render(request, 'OWNER/view_bill_owner.html', {'bills': bills,'client':client})     

def client_bills(request, client_id):
    bills = Bill.objects.filter(client_id=client_id)
    return render(request, 'OWNER/view_bill_owner.html', {'bills': bills})

#supplier

@login_required   
def SUPPLIER_ALL_DETAILS(request):
     purchase=PurchaseDetails.objects.all()
     context={
          "purchase":purchase
     }
     return render(request,'OWNER/supplier_all_details.html',context)

   
def get_total_balance_per_supplier():
    total_bills_per_supplier = PurchaseDetails.objects.values('supplier').annotate(total_amount=Sum('payment_amount'))
    paid_bills_per_supplier = PurchaseDetails.objects.filter(paid_status=True).values('supplier').annotate(paid_amount=Sum('payment_amount'))

    # Calculate the total amount paid per supplier
    paid_amounts = {item['supplier']: item['paid_amount'] for item in paid_bills_per_supplier}

    supplier_balances = {}
    for supplier_bill in total_bills_per_supplier:
        supplier_id = supplier_bill['supplier']
        supplier_name = Supplier.objects.get(pk=supplier_id).supplier  # Get supplier name using the ID
        total_amount = supplier_bill['total_amount']

        # Calculate the total amount paid by the supplier
        paid_amount = paid_amounts.get(supplier_id, 0)

        # Calculate the balance amount
        balance_amount = total_amount - paid_amount

        supplier_balances[supplier_id] = {'supplier_name': supplier_name, 'total_amount': total_amount, 'balance_amount': balance_amount, 'paid_amount': paid_amount}

    return supplier_balances


@login_required
def view_total_balance_per_supplier(request):
     supplier_balances= get_total_balance_per_supplier()
     return render(request,'OWNER/view_total_balance_per_supplier.html',{'supplier_balances':supplier_balances})

@login_required
def supplier_bills(request, supplier_id):
    purchase = PurchaseDetails.objects.filter(supplier_id=supplier_id)
    return render(request, 'OWNER/supplier_all_details.html', {'purchase': purchase})



def total_clients(request):
    total_clients_count = Client.objects.count()
    print(total_clients_count)
    return render(request,'total_clients.html',{'total_clients': total_clients_count})


# def total_clients_bills_charge(request):
#     total_payment_amount = Bill.objects.aggregate(total_payment=Sum('payment_amount'))['total_payment']

#     if total_payment_amount is not None:
#         print("Total payment amount from all clients:", total_payment_amount)
#     else:
#         print("There are no records.")

#     return render(request, "total_clients_bills_charge.html", {'total_payment_amount': total_payment_amount})

def client_total_paid_amount(request):
    client_total_paid_amount = Bill.objects.filter(paid_status=True).aggregate(total_sum=Sum('payment_amount'))['total_sum']
    return render(request,'client_total_paid_amount.html',{'client_total_paid_amount':client_total_paid_amount})

def client_total_balance_payment(request):
    client_total_balance_payment= Bill.objects.filter(paid_status=False).aggregate(total_sum=Sum('payment_amount'))['total_sum']
    return render(request,'client_total_balance_payment.html',{'client_total_balance_payment':client_total_balance_payment})


def total_payment_to_suppliers(request):
    total_payment_supplier = PurchaseDetails.objects.aggregate(total_sum=Sum('payment_amount'))['total_sum']
    print("Total sum of payments for all suppliers:", total_payment_supplier)
    return render(request,'total_payment_to_suppliers.html',{'total_payment_supplier': total_payment_supplier})

def total_balance_to_supplier(request):
    total_balance_to_supplier =  PurchaseDetails.objects.filter(paid_status=False).aggregate(total_sum=Sum('payment_amount'))['total_sum']
    return render(request,'total_balance_to_supplier.html',{'total_balance_to_supplier':total_balance_to_supplier})
