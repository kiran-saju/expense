from django import forms
from .models import Installment,Bill

class InstallmentForm(forms.ModelForm):
    class Meta:
        model = Installment
        fields ='__all__'


class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['installment_number', 'payment_amount', 'staff_name', 'paid_status']
