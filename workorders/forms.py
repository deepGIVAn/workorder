from django import forms
from django.forms import ModelForm
from .models import work_order, bill, rejection_list


class WorkForm(ModelForm):
    class Meta:
        model = work_order
        fields = (
            "wo_number",
            "wo_date",
            "comp_date",
            "company_name",
            "billing_address",
            "shipping_address",
            "person_name",
            "contact",
            "email",
            "requirements",
        )

        widgets = {
            "wo_number": forms.TextInput(attrs={"class": "form-control","placeholder": "Work Order Number"}),
            "wo_date": forms.DateInput(attrs={"type": "date", "class": "form-control",}),
            "comp_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "company_name": forms.TextInput(attrs={"class": "form-control","placeholder": "Company Name"}),
            "billing_address": forms.TextInput(attrs={"class": "form-control","placeholder": "Billing Address"}),
            "shipping_address": forms.TextInput(attrs={"class": "form-control","placeholder": "Shipping Address"}),
            "person_name": forms.TextInput(attrs={"class": "form-control","placeholder": "Person Name"}),
            "contact": forms.NumberInput(attrs={"class": "form-control","placeholder": "Contact Details"}),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "name@example.com"}
            ),
            "requirements": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Desciption of your products..",
                    "style":"resize:none; overflow:auto; ",            # 'auto' for scroll bars
                }
            ),
        }


class MakeBill(ModelForm):
    class Meta:
        model = bill
        fields = ("bill_no", "bill_date", "basic_amount", "tax")

        widgets = {
            "bill_no": forms.TextInput(attrs={"class": "form-control","placeholder": "INV-***"}),
            "bill_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "basic_amount": forms.NumberInput(attrs={"class": "form-control","placeholder": "0.00"}),
            "tax": forms.NumberInput(attrs={"class": "form-control","placeholder": "0.00"}),
        }

class RejectForm(ModelForm):
    class Meta:
        model = rejection_list
        fields = ("reason",)

        widgets = {
            "reason": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Put Some Reasons here ..",
                    "style":"resize:none; overflow:auto; ",    
                }
            )
        }