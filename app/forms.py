from django import forms
from .models import Installment,Bill,Supplier,RowMaterials,PurchaseDetails

class InstallmentForm(forms.ModelForm):
    class Meta:
        model = Installment
        fields ='__all__'


class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        # fields = ['installment_number', 'payment_amount', 'staff_name', 'paid_status']
        fields = '__all__'

class BillPaidStatusForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['paid_status']


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier  # Specify the model class
        fields = '__all__'

class RowMaterialForm(forms.ModelForm):
    class Meta:
        model= RowMaterials
        fields= '__all__'

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = PurchaseDetails
        # fields = ['installment_number', 'payment_amount', 'staff_name', 'paid_status']
        fields = '__all__'