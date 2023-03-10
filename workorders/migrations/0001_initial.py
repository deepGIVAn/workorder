# Generated by Django 4.1.5 on 2023-02-03 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='work_order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wo_number', models.CharField(max_length=50, verbose_name='Work Order Number')),
                ('wo_date', models.DateField(verbose_name='Work Order Date')),
                ('comp_date', models.DateField(verbose_name='Completion Date')),
                ('company_name', models.CharField(max_length=100, verbose_name='Company Name')),
                ('billing_address', models.CharField(max_length=200, verbose_name='Billing Address')),
                ('shipping_address', models.CharField(blank=True, max_length=200, null=True, verbose_name='Shipping Address')),
                ('person_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Concern Person')),
                ('contact', models.CharField(max_length=20, verbose_name='Contact')),
                ('email', models.EmailField(max_length=254, verbose_name='Email Address')),
                ('requirements', models.TextField(verbose_name='Requirements')),
                ('owner', models.IntegerField(default=1, verbose_name='Work Owner')),
            ],
        ),
    ]
