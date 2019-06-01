from django.shortcuts import render
import time
import requests

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

def show_data_in_excel(request):
    

    row_data = 1
    column_data = 0

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = "attachment; filename=Worksnaps Report.xlsx"
    book = Workbook(response,{'in_memory': True})

    work_sheet = book.add_worksheet("Monthly Summary Report")
    cell_format = book.add_format()
    cell_format.set_bold(True)
    cell_format.set_bg_color('#85C1E9')
    cell_format.set_align('center')
    cell_format.set_font_size()

    user_list = UserProfile.objects.all()
    users_data = []
    Joined_Date = []
    for users_details in user_list:
        users_data.append(users_details.user_name)
        Joined_Date.append(str(users_details.joined_date))


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

    for row_data,(users_name,Joined_Date) in enumerate(zip(users_data, Joined_Date)):
        row_data += 2
        work_sheet.write(row_data,column_data,Joined_Date)
        work_sheet.write(row_data,column_data1,users_name)
    
    bnk_acnt_details = BankAccountNumbers.objects.all()
    user_names_copy = users_data.copy()
    for row_data,username in enumerate(user_names_copy):
        row_data += 2
        for single_user in bnk_acnt_details:
            if username == single_user.user.username:
                work_sheet.write(row_data,column_data6,single_user.account_number)
    
    salary_details = Salary.objects.all()
    user_names = users_data.copy()
    for row_data,username in enumerate(user_names):
        row_data += 2
        for user_salary in salary_details:
            if username == user_salary.user.username:
                work_sheet.write(row_data,column_data2,user_salary.Salary)

    Total_working_days = 31
    Total_worked_days = 30

    salary_list = []
    salary_details = Salary.objects.all()
    for single_salary in salary_details:
        salary_list.append(single_salary.Salary)

    single_user_perday = []
    Net_amount = []
    for PerDay in salary_list:
        calculated_salary = int(PerDay) / Total_working_days
        single_user_perday.append(calculated_salary)

        for single_user_salary in single_user_perday:
            netamount = single_user_salary * Total_worked_days
            Net_amount.append(round(netamount))

    for row_data,(PerDay,Net_amount) in enumerate(zip(single_user_perday,Net_amount)):
        row_data += 2
        work_sheet.write(row_data,column_data3,PerDay)
        work_sheet.write(row_data,column_data4,Total_working_days)
        work_sheet.write(row_data,column_data5,Net_amount)



    book.close()

    return response

# def salary_perday(request):
#     Total_working_days = 31
#     Total_worked_days = 30
#     salary_list = []
#     salary_details = Salary.objects.all()
#     for single_salary in salary_details:
#         salary_list.append(single_salary.Salary)

#     single_user_perday = []
#     Net_amount = []
#     for user_salary in salary_list:
#         calculated_salary = int(user_salary) / Total_working_days
#         single_user_perday.append(calculated_salary)
        
#         for single_user_salary in single_user_perday:
#             netamount = single_user_salary * Total_worked_days
#             Net_amount.append(round(netamount))


    
#     return single_user_perday,Net_amount

