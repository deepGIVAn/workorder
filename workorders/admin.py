from django.contrib import admin
from .models import work_order, bill,rejection_list


@admin.register(work_order)
class work_orderadmin(admin.ModelAdmin):
    list_display = ("wo_number", "company_name", "wo_date", "person_name", "contact")
    ordering = ("-wo_date",)  # ascending order
    search_fields = ("wo_number", "company_name", "wo_date")


@admin.register(bill)
class billadmin(admin.ModelAdmin):
    list_display = ("bill_no", "bill_date", "total_amount", "created_by")
    ordering = ("-bill_date",)
    search_fields = ("bill_no", "bill_date", "created_by")

@admin.register(rejection_list)
class reject_listadmin(admin.ModelAdmin):
    list_display = ("order", "reason", "rejected_by",) 
    search_fields = ("order", "reason")

