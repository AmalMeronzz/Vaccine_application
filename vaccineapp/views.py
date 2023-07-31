from django.contrib.auth import logout
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage

# Create your views here.

def hselect_district(request):
    cursor = connection.cursor()
    cursor.execute("select * from district")
    district = cursor.fetchall()
    return render(request,'select_district.html',{'data':district})

def hselect_taluk(request,id):
    cursor = connection.cursor()
    cursor.execute("select * from taluk where iddistrict = '"+str(id)+"'")
    taluk = cursor.fetchall()
    return render(request,'select_taluk.html',{'data':taluk})


def login(request):
    if request.method == 'POST':
        username = request.POST['name']
        password = request.POST['password']
        cursor = connection.cursor()
        cursor.execute("select * from login where admin_id = '"+str(username)+"' and password = '"+str(password)+"'")
        admin = cursor.fetchone()

        if admin == None:
            cursor.execute("select * from user_register where user_id = '" + str(username) + "' and password = '"+str(password)+"'")
            user = cursor.fetchone()
            if user == None:
                cursor.execute("select * from hospital where hospital_id = '" + str(username) + "' and password = '"+str(password)+"' and status = 'approved'")
                hospital = cursor.fetchone()
                if hospital == None:
                    return redirect('login')
                else:
                    request.session['hospitalid'] = username
                    return redirect('hospitalhome')
            else:
                request.session['userid'] = username
                return redirect('userhome')
        else:
            print("admin side +++++++++++++++++++++++++")
            request.session['adminid'] = username
            return redirect('adminhome')
    else:
        print("_______________________________")
        return render(request,'login.html')

def logout1(request):
    logout(request)
    return redirect('login')

def admin_home(request):
    return render(request,'admin/index.html')

def select_district(request):
    cursor = connection.cursor()
    cursor.execute("select * from district")
    district = cursor.fetchall()
    return render(request,'admin/select_district.html',{'data':district})

def select_taluk(request,id):
    cursor = connection.cursor()
    # cursor = cursor.execute("select * from district where iddistrict = '"+str(id)+"'")
    # district = cursor.fetchone()

    cursor.execute("select * from taluk where iddistrict = '"+str(id)+"'")
    taluk = cursor.fetchall()
    return render(request,'admin/select_taluk.html',{'data':taluk})

def add_hospital(request,id):
    cursor = connection.cursor()
    if request.method == 'POST':

        hospitalid = request.POST['name']
        name = request.POST['name']
        address = request.POST['address']
        phone = request.POST['phone']
        email = request.POST['email']
        pincode = request.POST['pincode']
        district = request.POST['district']
        taluk = request.POST['taluk']
        password = request.POST['password']
        image = request.FILES['hospital_image']
        fss = FileSystemStorage()
        file = fss.save(image.name, image)
        file_url = fss.url(file)

        cursor.execute("select * from user_register where user_id = '"+str(hospitalid)+"'")
        user = cursor.fetchone()
        if user == None:
            cursor.execute("select * from hospital where hospital_id = '"+str(hospitalid)+"'")
            hospital = cursor.fetchone()
            if hospital == None:
                cursor.execute("insert into hospital values('"+str(hospitalid)+"','"+str(name)+"','"+str(address)+"','"+str(phone)+"','"+str(pincode)+"','"+str(email)+"','"+str(password)+"','"+str(district)+"','"+str(taluk)+"','"+str(image)+"','pending')")
                return redirect('login')
            else:
                return HttpResponse("<script>alert('Hospital already exists');window.location='../addhospital';</script>")
        else:
            return HttpResponse("<script>alert('Hospital already exists');window.location='../addhospital';</script>")
    else:
        cursor.execute("select * from taluk where idtaluk = '"+str(id)+"'")
        taluk = cursor.fetchone()
        return render(request,'add_hospital.html',{'data':taluk})

def new_hospital(request):
    cursor = connection.cursor()
    # cursor.execute("select * from hospital where status = 'pending'")
    cursor.execute("select hospital.*,district.name as d,taluk.name as t from hospital join district join taluk where hospital.iddistrict = district.iddistrict and hospital.idtaluk = taluk.idtaluk and hospital.status = 'pending'")
    pending = cursor.fetchall()
    return render(request,'admin/new_hospital.html',{'data':pending})

def approve_hospital(request,id):
    cursor = connection.cursor()
    cursor.execute("update hospital  set status = 'approved' where hospital_id = '"+str(id)+"' ")
    connection.close()
    return redirect('newhospital')

def delete_newhospital(request,id):
    cursor = connection.cursor()
    cursor.execute("delete from hospital where hospital_id = '"+str(id)+"'")
    connection.close()
    return redirect('newhospital')


def view_hospital(request):
    cursor = connection.cursor()
    cursor.execute("select hospital.*,district.name as d,taluk.name as t from hospital join district join taluk where hospital.iddistrict = district.iddistrict and hospital.idtaluk = taluk.idtaluk and hospital.status = 'approved'")

    hospital = cursor.fetchall()
    return render(request,'admin/view_hospital.html',{'data':hospital})

def edit_hospital(request,id):
    cursor = connection.cursor()
    if request.method == 'POST':
        print("hello ___________________________________1 ")
        name = request.POST['name']
        address = request.POST['address']
        phone = request.POST['phone']
        email = request.POST['email']
        pincode = request.POST['pincode']
        # district = request.POST['district']
        # taluk = request.POST['taluk']
        password = request.POST['password']
        # iddistrict = '"+str(district)+"', idtaluk = '"+str(taluk)+"',
        cursor.execute("update hospital set name='"+str(name)+"',address='"+str(address)+"',phone='"+str(phone)+"',email='"+str(email)+"',pincode='"+str(pincode)+"',password='"+str(password)+"' where hospital_id = '"+id+"'")
        print("hello ___________________________________2 ")
        return redirect('viewhospital')
    else:
        cursor.execute("select * from hospital where hospital_id = '"+id+"'")
        hospital = cursor.fetchone()
        return render(request,'admin/edit_hospital.html',{'i':hospital})



def delete_hospital(request,id):
    cursor = connection.cursor()
    cursor.execute("delete from hospital where hospital_id = '"+id+"'")
    return redirect('viewhospital')


def add_vaccine(request):
    if request.method == 'POST':
        vaccinetype = request.POST['name']
        cursor = connection.cursor()
        cursor.execute("insert into vaccine_type values(null,'"+vaccinetype+"')")
        return redirect('addvaccine')

    else:
        return render(request,'admin/add_vaccine.html')

def add_medicine(request,id):
    cursor = connection.cursor()
    if request.method == 'POST':
        medicine = request.POST['name']

        cursor.execute("select * from vaccine_medicines where name = '"+str(medicine)+"'")
        Taluk = cursor.fetchone()
        if Taluk == None:
            cursor.execute("insert into vaccine_medicines values(null,'"+str(medicine)+"','"+str(id)+"')")
            return redirect('addmedicine',id)
        else:
            return HttpResponse("<script>alert('Taluk name already exists');window.location='../addmedicine/<str:id>';</script>")
    else:
        return render(request,'admin/add_medicine.html')


def view_vaccine(request):
    cursor = connection.cursor()
    cursor.execute("select * from vaccine_type")
    vaccine = cursor.fetchall()
    return render(request,'admin/view_vaccine.html',{'data':vaccine})

def edit_vaccine_type(request,id):
    cursor = connection.cursor()
    if request.method == 'POST':
        vaccine = request.POST['name']
        cursor.execute("update vaccine_type set name = '"+str(vaccine)+"' where idvaccine_type = '"+id+"'")
        return redirect('viewvaccine')
    else:
        cursor.execute("select * from vaccine_type where idvaccine_type = '"+str(id)+"'")
        vaccine_type = cursor.fetchone()
        return render(request,'admin/edit_vaccine.html',{'data':vaccine_type})




def delete_vaccine_type(request,id):
    cursor = connection.cursor()
    cursor.execute("delete from vaccine_type where idvaccine_type = '"+str(id)+"'")
    return redirect('viewvaccine')

def add_district(request):
    if request.method == 'POST':
        district_name = request.POST['name']

        cursor = connection.cursor()
        cursor.execute("select * from district where name = '"+str(district_name)+"'")
        district = cursor.fetchone()
        if district == None:
            cursor.execute("insert into district values(null,'"+str(district_name)+"')")
            return redirect('adddistrict')
        else:
            return HttpResponse("<script>alert('District name already exists');window.location='../adddistrict';</script>")
    else:
        return render(request,'admin/add_district.html')

def view_district(request):
    cursor = connection.cursor()
    cursor.execute("select * from district")
    district = cursor.fetchall()
    connection.close()
    return render(request,'admin/view_district.html',{'data':district})

def delete_district(request,id):
    cursor = connection.cursor()
    cursor.execute("delete from district where iddistrict = '"+id+"'")
    return redirect('viewdistrict')


def add_taluk(request,id):
    cursor = connection.cursor()
    if request.method == 'POST':
        taluk = request.POST['name']

        cursor.execute("select * from taluk where name = '"+str(taluk)+"'")
        Taluk = cursor.fetchone()
        if Taluk == None:
            cursor.execute("insert into taluk values(null,'"+str(id)+"','"+str(taluk)+"')")
            return redirect('addtaluk',id)
        else:
            return HttpResponse("<script>alert('Taluk name already exists');window.location='../addtaluk/<str:id>';</script>")
    else:
        cursor.execute("select * from district where iddistrict = '"+str(id)+"'")
        district = cursor.fetchone()
        return render(request,'admin/add_taluk.html',{'data':district})

def view_vaccine_type(request):
    cursor = connection.cursor()
    cursor.execute("select * from vaccine_type")
    vaccine = cursor.fetchall()
    return render(request,'admin/view_vaccine1.html',{'data':vaccine})

def view_medicine1(request,id):
    cursor = connection.cursor()
    cursor.execute("select * from vaccine_medicines where idvaccine_type = '"+id+"'")
    medicine = cursor.fetchall()
    return render(request,'admin/view_medicine.html',{'data':medicine})

def delete_medicine(request,id):
    cursor = connection.cursor()
    cursor.execute("delete from vaccine_medicines where idmedicines = '"+id+"'")
    return redirect('viewvaccinetype')

# user
# -------------------------------------------------------------------------------------------------------

def user_home(request):
    return render(request,'user/index.html')

def user_registration(request):
    if request.method == 'POST':
        userid = request.POST['name']
        name = request.POST['name']
        address = request.POST['address']
        phone = request.POST['phone']
        email = request.POST['email']
        pincode = request.POST['pincode']
        password = request.POST['password']

        cursor =  connection.cursor()
        cursor.execute("select * from hospital where hospital_id = '"+str(userid)+"'")
        hospital = cursor.fetchone()
        if hospital == None:
            cursor.execute("select * from user_register where user_id = '"+str(userid)+"'")
            user = cursor.fetchone()
            if user == None:
                print("if working")
                cursor.execute("insert into user_register values('"+str(userid)+"','"+str(name)+"','"+str(address)+"','"+str(phone)+"','"+str(email)+"','"+str(pincode)+"','"+str(password)+"')")
                request.session["userid"] = userid
                return render(request,'user/index.html')
            else:
                return HttpResponse("<script>alert('User Name already exists');window.location='../userregisteration';</script>")
        else:
            return HttpResponse("<script>alert('User Name already exists');window.location='../userregisteration';</script>")
    else:
        return render(request,'user/user_register.html')

def user_view_hospital(request):
    cursor = connection.cursor()
    cursor.execute("select * from hospital where status = 'approved'")
    hospital = cursor.fetchall()
    print("--------------------------------",hospital)
    return render(request,'user/view_hospital.html',{'data':hospital})

def user_view_vaccine(request):
    cursor = connection.cursor()
    cursor.execute("select * from vaccine_type")
    vaccine = cursor.fetchall()
    return render(request, 'user/view_vaccine_type.html', {'data':vaccine})

    # cursor.execute("select vaccine_type.idvaccine_type from vaccine_type join vaccine_medicines where vaccine_type.idvaccine_type = vaccine_medicines.idvaccine_type")
    # vaccine = cursor.fetchall()
    # vaccine = list(vaccine)
    # l = []
    # for i in vaccine:
    #     m = list(i)
    #     n = m[0]
    #     l.append(n)
    # l = set(l)
    # li = list(l)
    # print(vaccine)
    # l1 = []
    # for i in li:
    #     cursor.execute("select name from vaccine_type where idvaccine_type = '"+str(i)+"'")
    #     vac = cursor.fetchone()
    #     vac = list(vac)
    #     l1.append(vac[0])
    #
    # return render(request, 'user/view_vaccine_type.html', {'data': li,'data1':l1})

def user_view_medicine(request,id):
    cursor = connection.cursor()
    cursor.execute("select * from vaccine_medicines where idvaccine_type = '"+str(id)+"'")
    medicine = cursor.fetchall()
    return render(request,'user/view_medicine.html',{'data':medicine})


def medicine_hospital(request,id):
    request.session['id_medicine_book']=id
    cursor = connection.cursor()
    cursor.execute("select hospital.*, daily_count.daily_count from hospital join daily_count where hospital.hospital_id = daily_count.hospital_id")
    hospital = cursor.fetchall()
    return render(request,'user/view_select_hospital.html',{'data':hospital})

def book_slot(request,id):
    if request.method == 'POST':
        userid = request.session['userid']
        idmed = request.session['id_medicine_book']
        date = request.POST['date']
        time = request.POST['time']
        total = int(request.POST['slot'])
        cursor = connection.cursor()
        cursor.execute("select daily_count from daily_count where hospital_id = '"+id+"'")
        data = cursor.fetchone()
        data = list(data)
        daily_count = int(data[0])
        print(daily_count)
        cursor.execute("select * from time_slot where hospital_id = '"+id+"' and booking_date = '"+date+"' and slot_time = '"+time+"' ")
        details = cursor.fetchone()


        if details == None:
            if total <= daily_count:
                cursor.execute("insert into time_slot values(null,'"+str(id)+"','"+str(date)+"','"+str(total)+"','"+str(idmed)+"','"+str(time)+"','"+str(userid)+"')")
                cursor.execute("insert into time_slot_counter values(null,'"+str(date)+"','"+str(time)+"','"+str(total)+"','"+str(id)+"')")
                return render(request,'user/success_page.html')
            else:
                print('slot full')
                return redirect('bookslot',id)
        else:
            cursor.execute("select slot_count,idtime_slot_counter from time_slot_counter where hospital_id = '" + id + "' and booking_date = '" + date + "' and slot_time = '" + time + "'")
            data = cursor.fetchone()
            data = list(data)
            slot_count = int(data[0])
            idtime_slot_counter = int(data[1])
            av = daily_count - slot_count
            if total <= av:
                cursor.execute("insert into time_slot values(null,'"+str(id)+"','"+str(date)+"','"+str(total)+"','"+str(idmed)+"','"+str(time)+"','"+str(userid)+"')")
                slot_count = slot_count + total
                cursor.execute("update time_slot_counter set slot_count = '"+str(slot_count)+"' where idtime_slot_counter = '"+str(idtime_slot_counter)+"'")
                return redirect('bookslot', id)
            else:
                print('slot full')
                return redirect('bookslot', id)
    else:
        return render(request,'user/book_vaccine.html')

def user_view_booking(request):
    userid = request.session['userid']
    cursor = connection.cursor()
    cursor.execute("select * from time_slot where userid = '"+str(userid)+"'")
    booking = cursor.fetchall()
    return render(request,'user/view_booking.html',{'data':booking})


# hospital
# ----------------------------------------------------------------------------------------------------

def hospital_home(request):
    return render(request,'hospital/index.html')

def add_count(request):
    if request.method == 'POST':
        daily_count = request.POST['count']
        hospitalid = request.session['hospitalid']

        cursor = connection.cursor()
        cursor.execute("select * from daily_count where hospital_id = '"+hospitalid+"'")
        hospital = cursor.fetchone()
        if hospital == None:
            cursor.execute("insert into daily_count values(null,'"+str(hospitalid)+"','"+str(daily_count)+"')")
            print("count inserted")
            return redirect('hospitalhome')
        else:
            return HttpResponse("<script>alert('daily count already added');window.location='../addcount';</script>")
    else:
        return render(request,'hospital/add_count.html')

def update_count(request):
    cursor = connection.cursor()
    hospitalid = request.session['hospitalid']
    if request.method == 'POST':
        count = request.POST['count']
        cursor.execute("update daily_count set daily_count = '"+str(count)+"' where hospital_id = '"+str(hospitalid)+"'")
        connection.close()
        return redirect('updatecount')
    else:
        cursor.execute("select * from daily_count where hospital_id = '"+hospitalid+"'")
        count = cursor.fetchone()
        return render(request,'hospital/view_daily_count.html',{'data':count})


def view_booking(request):
    hospital_id = request.session['hospitalid']
    cursor = connection.cursor()
    # cursor.execute("select * from time_slot where hospital_id = '"+hospital_id+"'")
    cursor.execute("select time_slot.*,vaccine_medicines.name from time_slot join vaccine_medicines where time_slot.idmedicines = vaccine_medicines.idmedicines and time_slot. hospital_id = '"+hospital_id+"' ")
    booking = cursor.fetchall()
    return render(request,'hospital/view_booking.html',{'data':booking})

def hospital_view_vaccine(request):
    cursor = connection.cursor()
    cursor.execute("select * from vaccine_type")
    vaccine = cursor.fetchall()
    return render(request, 'hospital/view_vaccine_type.html', {'data':vaccine})


def hospital_view_medicine(request,id):
    cursor = connection.cursor()
    cursor.execute("select * from vaccine_medicines where idvaccine_type = '"+str(id)+"'")
    medicine = cursor.fetchall()
    return render(request,'hospital/view_medicine.html',{'data':medicine})

