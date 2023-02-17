from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver


class work_order(models.Model):
    # it is mandatory to give max_length to charfield..
    wo_number = models.CharField("Work Order Number", max_length=50, blank=False, unique=True)
    wo_date = models.DateField("Work Order Date", blank=False)
    comp_date = models.DateField("Completion Date", blank=False)
    company_name = models.CharField("Company Name", blank=False, max_length=100)
    billing_address = models.CharField("Billing Address", max_length=200, blank=False)
    shipping_address = models.CharField("Shipping Address", max_length=200, blank=True, null=True)
    person_name = models.CharField("Concern Person", blank=True, null=True, max_length=50)
    contact = models.CharField("Contact", max_length=20, blank=False)
    # i was facing the error after doing certain maigrations that was saved files in megaraitons folder that contains some issues in them about phonenumber that can't be compiled successfully..``
    email = models.EmailField("Email Address", blank=False)
    requirements = models.TextField("Requirements", blank=False)
    status = models.CharField(max_length=50, default="Pending")
    owner = models.IntegerField("Work Owner", blank=False, default=1)

    def __str__(self):
        return self.wo_number + " - " + self.company_name


class bill(models.Model):
    order = models.OneToOneField(work_order, on_delete=models.CASCADE, unique=True)
    bill_no = models.CharField("Bill Number", max_length=10, blank=False, unique=True)
    bill_date = models.DateField("Bill Date", blank=False)
    basic_amount = models.FloatField("Basic Amount", blank=False, default=0)
    tax = models.FloatField("Tax( 0.10% - 30/% )", blank=False, default=0.10)
    total_amount = models.FloatField("Total Amount", default=0, blank=False)
    created_by = models.IntegerField("Created By", blank=False, default=1)

    # calculating the total amount..
    def save(self, *args, **kwargs):
        self.total_amount = self.basic_amount + self.basic_amount * (self.tax / 100)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.bill_no + " on " + str(self.bill_date)

    # def save(self,*args,**kwargs):                   # here if i am creating an item in bill model then it would change the status to completed but if i delete the item then it would not affect the status and it would leave it to Completed
    #     super().save(*args, **kwargs)
    #     self.order.status = f"Completed"
    #     self.order.save()


@receiver(post_save, sender=bill)
def update_status(sender, instance, created, **kwargs):
    if created:
        instance.order.status = "Completed"
        instance.order.save()


@receiver(pre_delete, sender=bill)
def reset_status(sender, instance, **kwargs):
    instance.order.status = "Pending"
    instance.order.save()


class rejection_list(models.Model):
    order = models.OneToOneField(work_order, on_delete=models.CASCADE, unique=True)
    reason = models.TextField("Reason", blank=False)
    rejected_by = models.IntegerField("Rejected By", blank=False, default=1)

    def __str__(self):
        return self.order.wo_number + " - " + self.reason


@receiver(post_save, sender=rejection_list)
def update(sender, instance, created, **kwargs):
    if created:
        instance.order.status = "Rejected"
        instance.order.save()


@receiver(pre_delete, sender=rejection_list)
def reset(sender, instance, **kwargs):
    instance.order.status = "Pending"
    instance.order.save()
