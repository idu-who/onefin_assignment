from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import F
from .models import *
from datetime import datetime
import re

# Create your views here.
@csrf_exempt
@require_POST
def create_employee_view(request):
    employee_code = request.POST.get('employee_code', '').strip().upper()
    name = request.POST.get('name', '').strip().upper()
    response = {}
    try:
        new_employee = Employee()
        new_employee.employee_code = employee_code
        new_employee.name = name
        new_employee.full_clean()
        new_employee.save()
        response['message'] = 'Employee created.'
    except ValidationError as validation_error:
        response['message'] = validation_error.message_dict
    return JsonResponse(response)

@csrf_exempt
@require_GET
def get_employee_view(request):
    employee_code = request.GET.get('employee_code', '').strip().upper()
    response = {}
    if employee_code:
        try:
            employee = Employee.objects.get(employee_code = employee_code)
            response = {
                'employee_code': employee.employee_code,
                'name': employee.name,
            }
        except ObjectDoesNotExist as does_not_exist:
            response['message'] = str(does_not_exist)
    else:
        response['message'] = 'Please provide an employee_code.'
    return JsonResponse(response)

@csrf_exempt
@require_POST
def create_vendor_view(request):
    vendor_code = request.POST.get('vendor_code', '').strip().upper()
    name = request.POST.get('name', '').strip().upper()
    response = {}
    try:
        new_vendor = Vendor()
        new_vendor.vendor_code = vendor_code
        new_vendor.name = name
        new_vendor.full_clean()
        new_vendor.save()
        response['message'] = 'Vendor created.'
    except ValidationError as validation_error:
        response['message'] = validation_error.message_dict
    return JsonResponse(response)

@csrf_exempt
@require_GET
def get_vendor_view(request):
    vendor_code = request.GET.get('vendor_code', '').strip().upper()
    response = {}
    if vendor_code:
        try:
            vendor = Vendor.objects.get(vendor_code = vendor_code)
            response = {
                'vendor_code': vendor.vendor_code,
                'name': vendor.name,
            }
        except ObjectDoesNotExist as does_not_exist:
            response['message'] = str(does_not_exist)
    else:
        response['message'] = 'Please provide a vendor_code.'
    return JsonResponse(response)

@csrf_exempt
@require_POST
def create_expense_view(request):
    print(request.POST)
    vendor_code = request.POST.get('vendor_code', '').strip().upper()
    employee_code = request.POST.get('employee_code', '').strip().upper()
    expense_comment = request.POST.get('expense_comment', '').strip().upper()
    expense_done_on = request.POST.get('expense_done_on', '').strip().upper()
    expense_amount = request.POST.get('expense_amount', '').strip().upper()
    response = {}
    try:
        new_expense = Expense()
        new_expense.vendor_code_id = vendor_code
        new_expense.employee_code_id = employee_code
        new_expense.expense_comment = expense_comment
        expense_done_on_message = None
        try:
            new_expense.expense_done_on = datetime.strptime(expense_done_on, '%d-%b-%Y')
        except ValueError as value_error:
            # Checking if error was due to incorrect format
            if re.search(r"%d-%b-%Y", str(value_error)):
                expense_done_on_message = f'“{expense_done_on}” does not match the format DD-MMM-YYYY.'
            else:
                expense_done_on_message = str(value_error)
        new_expense.expense_amount = expense_amount
        new_expense.full_clean()
        new_expense.save()
        response['message'] = 'Expense created.'
    except ValidationError as validation_error:
        response['message'] = validation_error.message_dict
        if expense_done_on_message:
            # adding the expense_done_on_message from value_error to message
            response['message'].setdefault('expense_done_on', []).append(expense_done_on_message)
    return JsonResponse(response)

@csrf_exempt
@require_GET
def get_employee_expense_view(request):
    employee_code = request.GET.get('employee_code', '').strip().upper()
    response = {}
    if employee_code:
        try:
            employee = Employee.objects.get(employee_code = employee_code)
            response['name'] = employee.name
            # Using annotate to refer to vendor_code.name as vendor
            expenses = employee.expense_set.annotate(vendor=F('vendor_code__name'))
            response['expenses'] = list(expenses.values('vendor', 'expense_comment', 'expense_done_on', 'expense_amount'))
        except ObjectDoesNotExist as does_not_exist:
            response['message'] = str(does_not_exist)
    else:
        response['message'] = 'Please provide an employee_code.'
    return JsonResponse(response)

@csrf_exempt
@require_GET
def get_vendor_expense_view(request):
    vendor_code = request.GET.get('vendor_code', '').strip().upper()
    response = {}
    if vendor_code:
        try:
            vendor = Vendor.objects.get(vendor_code = vendor_code)
            response['name'] = vendor.name
            # Using annotate to refer to employee_code.name as employee
            expenses = vendor.expense_set.annotate(employee=F('employee_code__name'))
            response['expenses'] = list(expenses.values('employee', 'expense_comment', 'expense_done_on', 'expense_amount'))
        except ObjectDoesNotExist as does_not_exist:
            response['message'] = str(does_not_exist)
    else:
        response['message'] = 'Please provide a vendor_code.'
    return JsonResponse(response)
