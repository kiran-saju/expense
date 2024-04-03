from django import forms
from .models import Installment

class InstallmentForm(forms.ModelForm):
    class Meta:
        model = Installment
        fields ='__all__'
