from django.shortcuts import render, redirect, HttpResponseRedirect,HttpResponse
from django.contrib import messages
from .models import work_order, bill,rejection_list

# for Users in this app
from django.contrib.auth.models import User

from .forms import WorkForm, MakeBill,RejectForm

# for pagination
from django.core.paginator import Paginator

import csv     #comma separated values

def download_order(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=work_orders.csv'    # comma separated values files

    # create a csv writer
    writer = csv.writer(response)

    #Desiging the model
    if request.user.is_superuser:
        work_orders = work_order.objects.all().order_by("-wo_date")

        # add coloumns heading to the csv files..
        writer.writerow(['Work Order Number','Work Order Date','Completion Date','Company Name','Billing Address','Shipping Address','Concern Person','Contact','Email Address','Requirements','Status',"Ordered By"])

        #Loop thru the works :
        for work in work_orders:
            Owner = User.objects.get(pk=work.owner)
            writer.writerow([work.wo_number,work.wo_date,work.comp_date,work.company_name,work.billing_address,work.shipping_address,work.person_name,work.contact,work.email,work.requirements,work.status,Owner])
        return response

    
    elif not request.user.is_superuser and request.user.is_authenticated:
        me = request.user.id
        work_orders = work_order.objects.filter(owner=me).order_by("-wo_date")
    
        # add coloumns heading to the csv files..
        writer.writerow(['Work Order Number','Work Order Date','Completion Date','Company Name','Billing Address','Shipping Address','Concern Person','Contact','Email Address','Requirements','Status'])

        #Loop thru the works :
        for work in work_orders:
            writer.writerow([work.wo_number,work.wo_date,work.comp_date,work.company_name,work.billing_address,work.shipping_address,work.person_name,work.contact,work.email,work.requirements,work.status])
        return response

    messages.success(request, ("First Login here .."))
    return redirect("login")

def download_bill(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=all_bill.csv'    # comma separated values files

    # create a csv writer
    writer = csv.writer(response)

    #Desiging the model
    if request.user.is_superuser:
        all = bill.objects.all().order_by("-bill_date")
        creater = User.objects.filter(is_superuser=True)

        # add coloumns heading to the csv files..
        writer.writerow(['Bill Number','Bill Date','Company Name','Billing Address','Shipping Address','Concern Person','Contact','Requirements','Basic Amount','Tax','Total Amount','Created By'])

        for Bil in all:
            Actual_Creator=None

            for user in creater:
                if user.id == Bil.created_by:
                    Actual_Creator = user.username       #every bill can have different creater..

            writer.writerow([Bil.bill_no,Bil.bill_date,Bil.order.company_name,Bil.order.billing_address,Bil.order.shipping_address,Bil.order.person_name,Bil.order.contact,Bil.order.requirements,Bil.basic_amount,Bil.tax,Bil.total_amount,Actual_Creator])
        
        return response
    
    messages.success(request, ("First Login as Admin.."))
    return redirect("logout")



def admin_home(request):
    # messages.success(request,("Welcome! Admins"))
    if request.user.is_superuser:
        work_orders = work_order.objects.all().order_by("-wo_date")

        # Set Up Pagination
        p = Paginator(work_orders, 3)  # here 2 means that there will be 2 pages in every page
        page = request.GET.get("page")
        work = p.get_page(page)

        nums = work.paginator.num_pages * "a"  # a is just for reference , to get the strings of length

        return render(request, "workorders/admin/admin_home.html", {"work_orders": work, "nums": nums})
    else:
        messages.success(request, ("First Login as Admin .."))
        return redirect("logout")


def client_home(request):
    if request.user.is_authenticated:
        # messages.success(request,("A great Welcome you to the Work Orders.."))
        me = request.user.id
        work_orders = work_order.objects.filter(owner=me).order_by("-wo_date")

        # Set Up Pagination
        p = Paginator(work_orders, 3)  # here 2 means that there will be 2 pages in every page
        page = request.GET.get("page")
        work = p.get_page(page)

        nums = work.paginator.num_pages * "a"  # a is just for reference , to get the strings of length

        return render(request, "workorders/client/client_home.html", {"work_orders": work, "nums": nums})
    else:
        messages.success(request, ("First Login here .."))
        return redirect("login")


def show_order(request, work_order_id):
    Work_order = work_order.objects.get(pk=work_order_id)  # for client and admin
    Owner = User.objects.get(pk=Work_order.owner)  # only for admin and here we are accessing the owner by in form of integers value so it also act as primary key..
    Bill = None
    Reject = None
    Rejected_by = None
    if Work_order.status=="Completed":
        Bill = bill.objects.get(order=Work_order)     # for getting the amount

    if Work_order.status=="Rejected":
        Reject = rejection_list.objects.get(order=Work_order)
        Rejected_by = User.objects.get(pk=Reject.rejected_by)
    return render(request, "workorders/show_order.html", {"work": Work_order, "owner": Owner,"Bill":Bill,"Reject":Reject,"Rejected_by":Rejected_by})


def add_order(request):
    submitted = False
    if request.method == "POST":
        form = WorkForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.owner = request.user.id
            order.save()
            return HttpResponseRedirect("?submitted=True")
    else:
        form = WorkForm
        if "submitted" in request.GET:
            submitted = True
    return render(request, "workorders/client/add_order.html", {"form": form, "submitted": submitted})


def delete_order(request, work_order_id):
    work = work_order.objects.get(pk=work_order_id)

    if request.user.id == work.owner:
        work.delete()
        messages.success(request, ("Deleted Successfully!!"))
    else:
        messages.success(request, ("Access Denied!! Only the real Owner can delete it .."))

    if request.user.is_superuser:
        return redirect("admin_home")
    else:
        return redirect("client_home")


def update_order(request, work_order_id):
    work = work_order.objects.get(pk=work_order_id)
    Owner = User.objects.get(pk=work.owner)
    form = WorkForm(request.POST or None, instance=work)  # at the same time it is giving me tha page with old data and taking the new data page
    if form.is_valid():
        form.save()
        # return redirect("show_order",args=work_order_id)
        return render(request,"workorders/show_order.html",{"work": work, "owner": Owner})
    return render(request, "workorders/client/update_order.html", {"form": form, "work": work})


def search_order(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        search = request.POST["search"]

        valid_field_names = {
            "wo_number": "Work Order Number",
            "company_name": "Company Name",
            "billing_address": "Billing Address",
            "requirements": "Requirements",
            "email": "Email Address",
            "contact": "Contact",
            "person_name": "Person Name",
            "shipping_address": "Shipping Address",
            "status":"Status"
        }
        if search in valid_field_names:
            actual_field_name = valid_field_names[search]

        if not request.user.is_superuser:
            work = work_order.objects.filter(owner=request.user.id)  # for accessing only your orders..
            result = work.filter(**{search + "__contains": searched})

        else:
            result = work_order.objects.filter(**{search + "__contains": searched})  # for getting all the search results for admins

        return render(
            request,
            "workorders/search_order.html",
            {"searched": searched, "result": result, "actual_field_name": actual_field_name},
        )
    else:
        return render(request, "workorders/search_order.html", {})


def make_bill(request, work_order_id):
    if request.user.is_superuser:
        Work_order = work_order.objects.get(pk=work_order_id)
        Owner = User.objects.get(pk=Work_order.owner)
        submitted = False
        if request.method == "POST":
            form = MakeBill(request.POST)
            if form.is_valid():
                bill = form.save(commit=False)
                bill.order = Work_order
                bill.created_by = request.user.id
                bill.save()
                return HttpResponseRedirect("?submitted=True")
        else:
            form = MakeBill()
            if "submitted" in request.GET:
                submitted = True
        return render(
            request,
            "workorders/admin/make_bill.html",
            {"work": Work_order, "owner": Owner, "submitted": submitted, "form": form},
        )
    else:
        messages.success(request, ("Access Denied!! Only Company staff can create the Bills"))
        return redirect("logout")


def all_bill(request):
    if request.user.is_superuser:
        all = bill.objects.all().order_by("-bill_date")
        creater = User.objects.filter(is_superuser=True)

        # Set Up Pagination
        p = Paginator(all, 2)
        page = request.GET.get("page")
        all_bills = p.get_page(page)

        nums = all_bills.paginator.num_pages * "a"  # a is just for reference , to get the strings of length

        return render(
            request,
            "workorders/admin/all_bill.html",
            {"all_bills": all_bills, "creater": creater, "nums": nums},
        )
    else:
        messages.success(request, ("Access Denied!! Only Company staff can access the Bills"))
        return redirect("logout")


def delete_bill(request, bill_id):
    if request.user.is_superuser:
        Bill = bill.objects.get(pk=bill_id)
        Bill.delete()
        messages.success(request, ("Deleted Successfully!!"))
        return redirect("all_bill")
    else:
        messages.success(request, ("Access Denied!! Only Company staff can delete the Bills"))
        return redirect("logout")


def update_bill(request, bill_id):
    if request.user.is_superuser:
        Bill = bill.objects.get(pk=bill_id)
        form = MakeBill(request.POST or None, instance=Bill)
        work_order = Bill.order
        Owner = User.objects.get(pk=Bill.order.owner)
        if form.is_valid():
            new = form.save(commit=False)
            new.created_by = request.user.id
            new.save()
            return redirect("all_bill")
        return render(request, "workorders/admin/update_bill.html", {"work": work_order, "form": form, "owner": Owner})
    else:
        messages.success(request, ("Access Denied!! Only Company staff can delete the Bills"))
        return redirect("logout")

def reject_order(request,work_order_id):
    if request.user.is_superuser:
        Work_order = work_order.objects.get(pk=work_order_id)
        Owner = User.objects.get(pk=Work_order.owner)
        submitted = False
        if request.method == "POST":
            form = RejectForm(request.POST)
            if form.is_valid():
                reject = form.save(commit=False)
                reject.order = Work_order
                reject.rejected_by = request.user.id
                reject.save()
                return HttpResponseRedirect("?submitted=True")
        else:
            form = RejectForm()
            if "submitted" in request.GET:
                submitted=True

        return render(request,"workorders/admin/reject_order.html",{"work": Work_order, "owner": Owner, "submitted": submitted, "form": form})
    else:
        messages.success(request,("Access Denied!! Only Company staff can reject the Orders"))
        return redirect("logout")

def unreject_order(request,work_order_id):
    if request.user.is_superuser:
        Work_order = work_order.objects.get(pk=work_order_id)
        rejected = rejection_list.objects.get(order=Work_order)
        rejected.delete()
        messages.success(request,("Rejection Removed Successfully!!"))
        return redirect("admin_home")
    else:
        messages.success(request,("Access Denied!! Only Company staff can Unreject the Orders"))
        return redirect("logout")