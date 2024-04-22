from django.db import models
from django.contrib.auth.models import AbstractUser
class Customuser(AbstractUser):
    USER=(
        (1,'Owner'),
        (2,'Staff'),
        (3,'Client'),
    )
    user_type=models.CharField(choices=USER,max_length=50,default=1)
    profile_pic=models.ImageField(upload_to='media/profile_pic')

class Staff(models.Model):
   
    admin=models.OneToOneField(Customuser, on_delete=models.CASCADE,null=True, blank=True)
    address=models.TextField()
    gender=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.admin.first_name + " " + self.admin.last_name

class Client(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE,null=True, blank=True)
    address=models.TextField()
    gender=models.CharField(max_length=100)
    project_name=models.CharField(max_length=100,null=True, blank=True)
    project_description=models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_clients')

    def __str__(self):
        return self.admin.first_name + " " + self.admin.last_name



#common installment table to store installments from clients

class Installment(models.Model):
    installment_number= models.CharField(max_length=100)

    def __str__(self):
        return self.installment_number
    
#for bill generation for client
class Bill(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE,blank=True, null=True)
    installment_number= models.ForeignKey(Installment,on_delete=models.CASCADE, blank=True, null=True)
    payment_amount=models.DecimalField(max_digits=10,decimal_places=2)
    due_date= models.DateField(auto_now_add=True,blank=True, null=True)
    paid_date= models.DateField(auto_now=True,blank=True, null=True)

    staff_name=models.ForeignKey(Staff,on_delete=models.CASCADE,blank=True, null=True)
    paid_status= models.BooleanField(default=False)

    def __str__(self):
        return f"Client Bill {self.client}"
    

class Supplier(models.Model):
     supplier= models.CharField(max_length=100)

     def __str__(self):
        return self.supplier
     
class RowMaterials(models.Model):
    item_name=models.CharField(max_length=200)

    def __str__(self):
        return self.item_name


class PurchaseDetails(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE,blank=True, null=True)
    staff_name=models.ForeignKey(Staff,on_delete=models.CASCADE,blank=True, null=True)
    # row_materials= models.ForeignKey(RowMaterials,on_delete=models.CASCADE, blank=True, null=True)
    items=models.CharField(max_length=500,blank=True, null=True)
    billno=models.CharField(max_length=200,blank=True, null=True)
    # quantity=models.DecimalField(max_digits=10,decimal_places=2)
    payment_amount=models.DecimalField(max_digits=10,decimal_places=2)
    due_date= models.DateTimeField(auto_now_add=True)
    paid_date= models.DateTimeField(auto_now=True)
    paid_status= models.BooleanField(default=False)

    # def __str__(self):
    #     return self.item_name

