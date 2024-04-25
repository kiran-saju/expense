from django.shortcuts import render,redirect,render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from app.models import Customuser, Installment, PurchaseDetails, Staff,Client,Bill, Supplier, RowMaterials
from app.forms import BillForm,BillPaidStatusForm,SupplierForm,RowMaterialForm,PurchaseForm

@login_required
def STAFF_HOME(request):
    
    return render(request,'STAFF/staff_home.html')

@login_required
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

@login_required
def CLIENT_VIEW(request):
    client = Client.objects.all()
    context={
        'client': client
    }
    return render(request,'STAFF/view_client.html',context)


@login_required
def CLIENT_EDIT(request,id):
    client = Client.objects.filter(id=id)
    context={
        'client': client
    }
    return render(request,'STAFF/edit_client.html',context)


@login_required
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


@login_required
def DELETE_CLIENT(request,id):
     client=Client.objects.get(id=id)
     client.delete()
     messages.success(request,"Record updated successfully")
     return redirect('view_client')



@login_required
def create_bill(request, id):
    client = get_object_or_404(Client, id=id)
    client_name = f"{client.admin.first_name} {client.admin.last_name}" if client.admin else "No Client Assigned"
    staff_name = f"{request.user.first_name} {request.user.last_name}" if request.user else "No Staff Logged In"

    all_installments = Installment.objects.all()

    used_installments = Bill.objects.filter(client=client).values_list('installment_number__id', flat=True)

    # Exclude used installment numbers from all_installments
    available_installments = all_installments.exclude(id__in=used_installments)

    # Construct choices list
    choices = [(inst.id, inst.installment_number) for inst in available_installments]

    if request.method == 'POST':
        form = BillForm(request.POST)
        if form.is_valid():
            bill = form.save(commit=False)
            bill.client = client
            # Automatically set staff name to logged-in user
            bill.save()
            return redirect('view_client')  # Redirect to client detail page
        else:
            logger.error("Form is not valid: %s" % form.errors)
    else:
        form = BillForm()
        form.fields['installment_number'].choices = choices

    return render(request, 'STAFF/add_bill.html', {'client_name': client_name, 'staff_name': staff_name, 'form': form})




@login_required
def view_bills_staff(request, client_id):
    client = Client.objects.get(id=client_id)
    bills = Bill.objects.filter(client=client)
    return render(request, 'STAFF/view_bill_staff.html', {'bills': bills})



logger = logging.getLogger(__name__)
@login_required
def change_paid_status(request,bill_id):
    bill = get_object_or_404(Bill,id=bill_id)
    if request.method == 'POST':
        form = BillPaidStatusForm(request.POST, instance=bill)
        if form.is_valid():
            form.save()
            return redirect('view_client') 
    else:
        form = BillPaidStatusForm(instance=bill)
    return render(request, 'STAFF/change_paid_status.html', {'form': form, 'bill_id': bill_id})


@login_required
def DELETE_BILL(request,id):
     bill=Bill.objects.get(id=id)
     bill.delete()
     messages.success(request,"Record updated successfully")
     return redirect('view_bills_staff')

@login_required
def supplier_form(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_suppliers')
    else:
        form = SupplierForm()
    return render(request, 'STAFF/supplier_form.html', {'form': form})

@login_required
def view_suppliers(request):
    suppliers = Supplier.objects.all()
    context={
        'suppliers': suppliers
    }
    return render(request, 'STAFF/view_suppliers.html',context)

@login_required
def delete_supplier(request,id):
    supplier=Supplier.objects.get(id=id)
    supplier.delete()
    messages.success(request,"Successfully Deleted an item")
    return redirect("view_suppliers")

@login_required
def row_materials_form(request):
    if request.method == 'POST':
        form = RowMaterialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_row_materials')
    else:
            form= RowMaterialForm()
    return render(request,'STAFF/rowmaterial_form.html', {'form': form})

@login_required
def view_row_materials(request):
    rowmaterials= RowMaterials.objects.all()
    context={
        'rowmaterials':rowmaterials
    }
    return render(request,"STAFF/view_row_materials.html",context)

@login_required
def delete_row_materials(request,id):
    rowmaterials=RowMaterials.objects.get(id=id)
    rowmaterials.delete()
    messages.success(request,"Successfully Deleted an item")
    return redirect("view_row_materials")

#for purchase pannel

@login_required
def purchase_details_create(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            purchase = form.save(commit=False)
            purchase.staff_name = request.user.staff  # Associate purchase with logged-in staff
            purchase.save()
            return redirect('purchase_details_list')
    else:
        form = PurchaseForm()
    return render(request, 'STAFF/purchase_details_form.html', {'form': form})

@login_required
def purchase_details_list(request):
    staff = request.user.staff  # Get the staff associated with the logged-in user
    purchases = PurchaseDetails.objects.filter(staff_name=staff)  # Filter purchases by staff
    return render(request, 'STAFF/purchase_details_list.html', {'purchases': purchases})

@login_required
def purchase_details_update(request,id):
    purchase = get_object_or_404(PurchaseDetails,id=id)
    if request.method == 'POST':
        form = PurchaseForm(request.POST, instance=purchase)
        if form.is_valid():
            form.save()
            return redirect('purchase_details_list')
    else:
        form = PurchaseForm(instance=purchase)
    return render(request, 'STAFF/purchase_details_form.html', {'form': form})


@login_required
def purchase_details_delete(request,id):
    purchase = RowMaterials.objects.get(id=id)
    purchase.delete()
    messages.success(request,"Successfully Deleted an item")
    return redirect('purchase_details_list')


def total_clients_created_by_staff(request):


    return render(request, 'total_clients_created_by_staff.html')

def view_clients_by_staff(request, staff_id):
    try:
        # Retrieve the staff member based on the provided ID
        staff = Staff.objects.get(id=staff_id)
        
        # Filter clients based on the staff member
        clients = Client.objects.filter(created_by=staff)
        
        context = {
            'staff': staff,
            'clients': clients
        }
        return render(request, 'STAFF/view_clients_by_staff.html', context)
    except Staff.DoesNotExist:
        # Handle the case where the staff member does not exist
        return redirect('error_page')  # Redirect to an error page or handle it as needed
