from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from app.models import Customuser, Staff,Bill
from django.db.models import Sum, F

@login_required
def CLIENT_HOME(request):
    return render(request,'CLIENT/client_home.html')

@login_required
def client_bills(request):
    client = request.user.client 
    bills = Bill.objects.filter(client=client)
    total_payment = bills.filter(paid_status=True).aggregate(total_payment=Sum('payment_amount'))['total_payment']
    total_balance = bills.filter(paid_status=False).aggregate(total_balance=Sum('payment_amount'))['total_balance']
    print(total_balance)
    print(total_payment )
    return render(request, 'CLIENT/client_bills.html', {'bills': bills,'total_payment':total_payment,'total_balance':total_balance})

