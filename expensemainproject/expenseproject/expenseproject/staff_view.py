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

from django.shortcuts import render, get_object_or_404
from app.forms import BillForm

'''
def create_bill(request,id):
    client = get_object_or_404(Client, id=id)
    if request.method == 'POST':
        form = BillForm(request.POST)
        if form.is_valid():
            bill = form.save(commit=False)
            bill.client = client
            # Set initial value for staff name field
            bill.staff_name = client.created_by if client.created_by else None
            bill.save()
            return redirect('view_clients')  # Redirect to view clients page after adding bill
    else:
        initial_staff = client.created_by if client.created_by else None
        form = BillForm(initial={'staff_name': initial_staff})  # Set initial value for staff name field
    return render(request, 'STAFF/add_bill.html', {'form': form, 'client': client})
'''



from django.shortcuts import render, get_object_or_404
from app.forms import BillForm
import logging

logger = logging.getLogger(__name__)

def create_bill(request, id):
    client = get_object_or_404(Client, id=id)
    
    # Query the Installment table to get all installment numbers
    all_installments = Installment.objects.all()
    
    # Get the used installment numbers for this client
    used_installments = Bill.objects.filter(client=client).values_list('installment_number__id', flat=True)
    
    # Exclude used installment numbers from all_installments
    available_installments = all_installments.exclude(id__in=used_installments)

    # Construct choices list
    choices = [(inst.id, inst.installment_number) for inst in available_installments]
    
    if request.method == 'POST':
        # Process form submission
        form = BillForm(request.POST)
        if form.is_valid():
            bill = form.save(commit=False)
            bill.client = client
            bill.save()
            return redirect('view_client') 
    else:
        # Create the form with choices for installment_number field
        form = BillForm()
        form.fields['installment_number'].choices = choices
        
    return render(request, 'STAFF/add_bill.html', {'client': client, 'form': form})

def view_bills_staff(request):
    bills = Bill.objects.all()
    return render(request, 'bills.html', {'bills': bills})
