from django.db import models
from django.core import validators
from datetime import date

# Create your models here.
class Employee(models.Model):
    employee_code = models.CharField(
        primary_key=True,
        max_length=8,
        validators=[
            validators.RegexValidator(
                regex=r'^EMP\-[0-9]+$',
                message='employee_code must be in the format EMP-XXX, where X is any digit.'
            ),
        ],
    )
    name = models.CharField(max_length=30)

class Vendor(models.Model):
    vendor_code = models.CharField(
        primary_key=True,
        max_length=8,
        validators=[
            validators.RegexValidator(
                regex=r'^VND\-[0-9]+$',
                message='vendor_code must be in the format VND-XXX, where X is any digit.'
            ),
        ],
    )
    name = models.CharField(max_length=30)

class Expense(models.Model):
    vendor_code = models.ForeignKey(Vendor, on_delete=models.PROTECT)
    employee_code = models.ForeignKey(Employee, on_delete=models.PROTECT)
    expense_comment = models.TextField()
    expense_done_on = models.DateField(validators=[
        validators.MaxValueValidator(date.today, message='expense_done_on must not be after today\'s date'),
    ])
    expense_amount = models.IntegerField()
