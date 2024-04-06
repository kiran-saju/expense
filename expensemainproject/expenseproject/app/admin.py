from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

class UserModel(UserAdmin):
    list_display= ['username', 'user_type']
admin.site.register(Customuser,UserModel)
admin.site.register(Staff)
admin.site.register(Client)
# admin.site.register(PaymentInstallment)
admin.site.register(Bill)
admin.site.register(Installment)