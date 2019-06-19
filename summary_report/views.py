from django.shortcuts import render
import time
import requests
from django.http import JsonResponse
from datetime import datetime,timedelta,date
from calendar import monthrange
from reports.models import TotalLeaves,\
                            UserProfile,\
                            UsersList

from django.contrib.auth.models import User
from reports_2.models import BankAccountNumber
from rest_framework.response import Response
from django.shortcuts import render, HttpResponse,redirect
from xlsxwriter.workbook import Workbook
from summary_report.models import Salary,BankAccountNumbers
from reports.views import *
from reports.models import *
import ast
from django.forms.models import model_to_dict

def show_data_in_excel(request):
    month = request.GET.get("month",0)
    year = request.GET.get("year",2018)
    month_start,monthrang = monthrange(int(year),int(month))

    row_data = 1
    column_data = 0

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = "attachment; filename=Montly Summary Report.xlsx"
    book = Workbook(response,{'in_memory': True})

    work_sheet = book.add_worksheet("{}-{}".format(month,year))
    cell_format = book.add_format()
    cell_format.set_bold(True)
    cell_format.set_bg_color('#85C1E9')
    cell_format.set_align('center')
    cell_format.set_font_size()

    column_data +=1
    work_sheet.write(row_data,column_data,'Joined Date',cell_format)
    column_data1 = column_data + 1
    work_sheet.write(row_data,column_data1,'Name',cell_format)
    column_data2 = column_data1 + 1
    work_sheet.write(row_data,column_data2,'Salary',cell_format)
    column_data3 = column_data2 + 1
    work_sheet.write(row_data,column_data3,'PerDay',cell_format)
    column_data4 = column_data3 + 1
    work_sheet.write(row_data,column_data4,'Worked Days',cell_format)
    column_data5 = column_data4 + 1
    work_sheet.write(row_data,column_data5,'Net',cell_format)
    column_data6 = column_data5 + 1
    work_sheet.write(row_data,column_data6,'Bank Account No',cell_format)


    work_sheet.set_column(1, 15, 15)

    users_data = monthly_amount_calc(request)

    for month_data in users_data.values():
        row_data += 1
        work_sheet.write(row_data,column_data,month_data['joined_date'])
        work_sheet.write(row_data,column_data1,month_data['Name'])
        work_sheet.write(row_data,column_data2,month_data['salary'])
        work_sheet.write(row_data,column_data3,month_data['per_day_salary'])
        work_sheet.write(row_data,column_data4,month_data['No of days worked'])
        work_sheet.write(row_data,column_data5,month_data['salary_to_be_paid'])
        work_sheet.write(row_data,column_data6,month_data['account_number'])

    book.close()

    return response

def monthly_amount_calc(request):
    month = request.GET.get("month",0)
    year = request.GET.get("year",2018)
    user_name = request.GET.get("user_name","")
    month_start,monthrang = monthrange(int(year),int(month))
    from_date = "%s-%s-01"% (year, month)
    to_date = "%s-%s-%s" % (year,month,monthrang)
    t_working_days = working_days(year,month,from_date,to_date)
    total_working_days = list(t_working_days)[0]

    summary = users_summary(from_date,to_date,year,month,"all")
    stored,user_names = list(summary)

    month_data = {}
    for user_dt in stored.values():
        leaves_count=user_dt['No of leaves']
        remaining_leaves_dict = TotalLeaves.objects.get(user__username=user_dt['Name'])
        try:
            remaining_leaves = ast.literal_eval(remaining_leaves_dict.data)['%s-%s'%(year,int(month)-1)]['accrued_leaves']
        except KeyError:
            remaining_leaves = 0

        worked_days = user_dt['No of days worked'] 
        worked_days = total_working_days if worked_days >= total_working_days else worked_days
        month_data[user_dt['Name']] = {
            'Name': user_dt['Name'],
            'No of days worked': worked_days 
        }
    for single_user_salary in Salary.objects.all():
        if  single_user_salary.user.username in user_names:
            per_day = int(single_user_salary.Salary) / total_working_days
            net_amount = month_data[single_user_salary.user.username]['No of days worked'] * per_day
            month_data[single_user_salary.user.username].update({
                'salary': single_user_salary.Salary,
                'per_day_salary': per_day,
                'salary_to_be_paid': net_amount,
                })
            bank_account = list(BankAccountNumber.objects.filter(
                user=single_user_salary.user).values('account_number'))
            if bank_account:
                month_data[single_user_salary.user.username].update(bank_account[0])
            else:
                month_data[single_user_salary.user.username].update({'account_number': "Not Specified"})
            joined_date = list(UserProfile.objects.filter(
                user_name=single_user_salary.user.username).values('joined_date'))
            joined_date = {'joined_date': str(joined_date[0]['joined_date'])}
            month_data[single_user_salary.user.username].update(joined_date)  

    # return JsonResponse(month_data[user_name])
    if user_name:
        return {user_name: month_data[user_name]}
    return month_data