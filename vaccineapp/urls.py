from .  import views
from django.urls import path

urlpatterns = [
    path('',views.login,name="login"),
    path('login',views.login,name="login"),
    path('logout',views.logout1,name="logout"),
    path('hselectdistrict',views.hselect_district,name="hselectdistrict"),
    path('hselecttaluk/<str:id>',views.hselect_taluk,name="hselecttaluk"),


    # admin
    # --------------------------------------------------------------------------------------
    path('adminhome',views.admin_home,name="adminhome"),
    path('selectdistrict',views.select_district,name="selectdistrict"),
    path('selecttaluk/<str:id>',views.select_taluk,name="selecttaluk"),
    path('addhospital/<str:id>',views.add_hospital,name="addhospital"),
    path('newhospital',views.new_hospital,name="newhospital"),
    path('approvehospital/<str:id>',views.approve_hospital,name="approvehospital"),
    path('deletehospital1/<str:id>',views.delete_newhospital,name="deletehospital1"),
    path('viewhospital',views.view_hospital,name="viewhospital"),
    path('edithospital/<str:id>', views.edit_hospital, name="edithospital"),
    path('deletehospital/<str:id>',views.delete_hospital,name="deletehospital"),
    path('addvaccine',views.add_vaccine,name="addvaccine"),
    path('addmedicine/<str:id>',views.add_medicine,name="addmedicine"),
    path('viewvaccine',views.view_vaccine,name="viewvaccine"),
    path('editvaccinetype/<str:id>',views.edit_vaccine_type,name="editvaccinetype"),
    path('deletevaccinetype/<int:id>',views.delete_vaccine_type,name="deletevaccinetype"),
    path('adddistrict',views.add_district,name="adddistrict"),
    path("viewdistrict",views.view_district,name="viewdistrict"),
    path('deletedistrict/<str:id>',views.delete_district,name="deletedistrict"),
    path("addtaluk/<str:id>",views.add_taluk,name="addtaluk"),
    path('viewvaccinetype',views.view_vaccine_type,name="viewvaccinetype" ),
    path('viewmedicine1/<str:id>',views.view_medicine1,name="viewmedicine1"),
    path('deletemedicine/<str:id>',views.delete_medicine,name="deletemedicine"),


    # user
    # --------------------------------------------------------------------------------------
    path('userhome',views.user_home,name="userhome"),
    path('userregisteration',views.user_registration,name="userregistration"),
    path('userviewhospital',views.user_view_hospital,name="userviewhospital"),
    path('userviewvaccine',views.user_view_vaccine,name="userviewvaccine"),
    path('userviewmedicine/<str:id>',views.user_view_medicine,name="userviewmedicine"),
    path('medicinehospital/<str:id>',views.medicine_hospital,name="medicinehospital"),
    path('bookslot/<str:id>',views.book_slot,name="bookslot"),
    path('viewbookinguser',views.user_view_booking,name="viewbookinguser"),

    # hospital
    # -----------------------------------------------------------------------------------------
    path('hospitalhome',views.hospital_home,name="hospitalhome"),
    path('hviewvaccine',views.hospital_view_vaccine,name="hviewvaccine"),
    path('hviewmedicine/<str:id>',views.hospital_view_medicine,name="hviewmedicine"),
    path('addcount',views.add_count,name="addcount"),
    path('updatecount',views.update_count,name="updatecount"),
    path('viewbooking',views.view_booking,name="viewbooking")


]