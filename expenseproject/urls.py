"""
URL configuration for expenseproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views,owner_view,staff_view,client_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/',views.BASE,name="base"),

    #login path
    path('',views.LOGIN,name="login"),
    path('doLogin',views.doLogin,name='doLogin'),
    path('logout',views.Logout,name="logout"),

    #Owner pannel
    path('Owner/Home',owner_view.OWNER_HOME,name="owner_home"),

    path('Owner/Staff/Add',owner_view.ADD_STAFF,name="add_staff"),
    path('Owner/Staff/View',owner_view.STAFF_VIEW,name="view_staff"),
    path('Owner/Staff/Edit/<str:id>/',owner_view.STAFF_EDIT,name='edit_staff'),
    path('Owner/Staff/Update',owner_view.STAFF_UPDATE,name='update_staff'),
    path('Owner/Staff/Delete/<str:id>/',owner_view.DELETE_STAFF,name='delete_staff'),

    path('Owner/Client/All/Details/',owner_view.CLIENT_ALL_DETAILS,name="client_all_details"),
    path('Owner/view/client/bills/',owner_view.view_bills_owner,name='view_bills_owner'),
    path('Owner/view/client//bills/totalbalance/',owner_view.get_total_balance_per_client,name="get_total_balance_per_client"),
    path('Owner/view/client//bills/view/totalbalance/',owner_view.view_total_balance_per_client,name="view_total_balance_per_client"),
    path('client/<int:client_id>/', owner_view.client_bills, name='client_bills'),

 
    path('Owner/Supplier/All/Details/',owner_view.SUPPLIER_ALL_DETAILS,name="supplier_all_details"),
    path('Owner/view/supplier//bills/totalbalance/',owner_view.get_total_balance_per_supplier,name="get_total_balance_per_supplier"),
    path('Owner/view/supplier//bills/view/totalbalance/',owner_view.view_total_balance_per_supplier,name="view_total_balance_per_supplier"),
    path('supplier/<int:supplier_id>/', owner_view.supplier_bills, name='supplier_bills'),
    path('total-clients/', owner_view.total_clients, name='total_clients'),
    # path('total-clients-bills-charge/', owner_view.total_clients_bills_charge, name='total_clients_bills_charge'),
    path('total-payment-to-suppliers/', owner_view.total_payment_to_suppliers, name='total_payment_to_suppliers'),
    path('total-balance-to-supplier/',owner_view.total_balance_to_supplier,name='total_balance_to_supplier'),
    path('client-total-paid_-mount/',owner_view.client_total_paid_amount,name='client_total_paid_amount'),
    path('client-total-balance-payment/',owner_view.client_total_balance_payment,name='client_total_balance_payment'),

    

    #Staff pannel
    path('Staff/Home',staff_view.STAFF_HOME,name="staff_home"),
    path('Staff/Add/client',staff_view.ADD_CLIENT,name="add_client"),
    path('Staff/Client/View',staff_view.CLIENT_VIEW,name="view_client"),
    path('Staff/Client/Edit/<str:id>/',staff_view.CLIENT_EDIT,name='edit_client'),
    path('Staff/Client/Update',staff_view.CLIENT_UPDATE,name='update_client'),
    path('Staff/Client/Delete/<str:id>/',staff_view.DELETE_CLIENT,name='delete_client'),
    path('Staff/Client/Bill/Delete/<str:id>/',staff_view.DELETE_BILL,name='delete_bill'),
    path('staff/supplier/form/', staff_view.supplier_form, name='supplier_form'),
    path('staff/view/suppliers/', staff_view.view_suppliers, name='view_suppliers'), 
    path('staff/view/suppliers/delete/<str:id>/', staff_view.delete_supplier, name='delete_supplier'),
    path('staff/rowmaterials/form/', staff_view.row_materials_form, name='add_row_materials'),
    path('staff/view/rowmaterials/', staff_view.view_row_materials, name='view_row_materials'),
    path('staff/view/rowmaterials/delete/<str:id>/', staff_view.delete_row_materials, name='delete_row_materials'),
    path('total/clients/created-by-staff',staff_view.total_clients_created_by_staff,name="total_clients_created_by_staff"),
 
    
    #client pannel
    path('Client/Home',client_view.CLIENT_HOME,name='client_home'),
    path('clients/view/bills/', client_view.client_bills, name='client_bills'),
    # path('client/home/bills/',client_view.client_total_balance,name="client_total_balance"),
     


    #Installment details in staff pannel
    # path('Staff/Client/Installmentdetails',staff_view.INSTALLMENTS,name='installments'),
    # path('Staff/Client/Add/Installments',staff_view.ADD_INSTALLMENT,name="add_installment"),

    #profile update
    path('profile/',views.Profile,name='profile'),
    path('profileupdate/',views.Profile_Update,name='profile_update'),

    #installment table
    path('Staff/Add/installment/',views.installment_form, name='installment_form'), 

    #Bill table create_bill
    path('Staff/Add/Bills/<str:id>/',staff_view.create_bill, name='create_bill'),
    #path('Staff/View/Bills/<int:client_id',staff_view.view_bills_staff, name='view_bills_staff'),
    path('Staff/View/Bills/<int:client_id>',staff_view.view_bills_staff, name='view_bills_staff'),
    path('Staff/View/Bills/paystatus/<int:bill_id>/', staff_view.change_paid_status, name='change_paid_status'),


    #purchase
    path('staff/purchase/details/create/',staff_view.purchase_details_create, name='purchase_details_create'),
    path('staff/purchase/details/list', staff_view.purchase_details_list, name='purchase_details_list'),
    path('staff/purchase/details/update/<int:id>/', staff_view.purchase_details_update, name='purchase_details_update'),
    path('staff/purchase/details/delete/<int:id>/', staff_view.purchase_details_delete, name='purchase_details_delete'),

    
    


]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
