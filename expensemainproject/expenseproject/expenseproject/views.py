from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from app.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from app.models import Customuser

def BASE(request):
    return render(request,'base.html')

def LOGIN(request):
    return render(request,'login.html')

@login_required
def Logout(request):
    logout(request)
    return redirect('/')

def doLogin(request):
    if request.method == "POST":
       user = EmailBackEnd.authenticate(request,
                                        username=request.POST.get('email'),
                                        password=request.POST.get('password'),)
       if user!=None:
           login(request,user)
           user_type = user.user_type
           if user_type == '1':
               return redirect('owner_home')
           elif user_type == '2':
               return redirect('staff_home')
           elif user_type == '3':
                return redirect('client_home')
           else:
               messages.error(request,'Email and Password Are Invalid !')
               return redirect('login')
       else:
           messages.error(request,'Email and Password Are Invalid !')
           return redirect('login')

def Profile(request):
    user= Customuser.objects.get(id= request.user.id)
    context ={
        "user":user
    }
    return render(request,'profile.html',context)

def Profile_Update(request):
    if request.method == 'POST':
        profile_pic= request.FILES.get('profile_pic')
        first_name= request.POST.get('first_name')
        last_name= request.POST.get('last_name')
        password= request.POST.get('password')

    try:
        customuser = Customuser.objects.get(id=request.user.id)
        customuser.first_name=first_name
        customuser.last_name = last_name

        if password!=None and password !="":
            customuser.set_password(password)
        if profile_pic !=None and profile_pic !="":
            customuser.profile_pic = profile_pic
        customuser.save()
        messages.success(request,"Your profile updated Successfully")
        redirect('profile')

    except:
        messages.error(request,"failed to update your message")

    return render(request,'profile.html')


from app.forms import InstallmentForm
def installment_form(request):
    if request.method == 'POST':
        form = InstallmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff_home')  # Assuming you have a URL named 'success'
    else:
        form = InstallmentForm()
    return render(request, 'installment_form.html', {'form': form})
