from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import LeaveForm
from .models import Leave, User
# Create your views here.
from django.core.mail import send_mail


def home(request):
    if request.user.is_authenticated():
        return render(request, 'leave/index.html', {})
    else:
        return redirect('/accounts/login')


def submit_leave(request):
    if request.user.is_authenticated():
        if request.method == "POST":
            noted_to = User.objects.get(pk=request.POST.get('noted_to'))
            form = LeaveForm(request.POST)
            if form.is_valid():
                form_data = form.save(commit=False)
                form_data.employee = request.user
                form_data.save()
                mail_subject = 'New leave submitted by ' + request.user.get_full_name()
                mail_message = 'The following leave has been submitted by ' + request.user.get_full_name() + '\n\n'\
                       'From ' + str(request.POST.get('from_date')) + ' to ' + str(request.POST.get('to_date')) + '\n\n'\
                       'Purpose: ' + request.POST.get('purpose') + '\n\n'\
                       'Employee ' + request.user.get_full_name() + ' has ' + str(request.user.available_leaves) + ' leaves remaining.\n\n'\
                       'Login to portal at https://hpgcl.herokuapp.com/accounts/login/ to approve or deny the leave.'\
                       'This is an autogenerated mail by the leave portal.'
                send_mail(mail_subject, mail_message, 'HPGCL Leave Portal <hpgcl@leaveportal.com>', [noted_to.email], fail_silently=False)                
                return redirect('/')
        else:
            form = LeaveForm(request.user)
        return render(request, 'leave/submit_leave.html', {'form': form})


def your_leaves(request):
    if request.user.is_authenticated():
        leaves = Leave.objects.filter(employee=request.user).order_by('-pk')
        return render(request, 'leave/your_leaves.html', {'leaves': leaves})
    else:
        return redirect('/accounts/login')


def department_leaves(request):
    if request.user.is_authenticated():
        user_designation = request.user.designation
        user_department = request.user.department
        user_station = request.user.power_station
        if user_designation == 'CE':
            dept_leaves = Leave.objects.filter(
                employee__power_station=user_station)
        elif user_designation == 'SE':
            dept_leaves = Leave.objects.filter(employee__power_station=user_station).exclude(
                employee__power_station=user_station, employee__designation="CE").exclude(employee__designation="SE")
        elif user_designation == 'XEN':
            dept_leaves = Leave.objects.filter(employee__power_station=user_station).exclude(
                employee__designation="CE").exclude(employee__designation="SE").exclude(employee__designation="XEN")
        elif user_designation == 'AEE':
            dept_leaves = Leave.objects.filter(employee__power_station=user_station).exclude(employee__designation="CE").exclude(
                employee__designation="SE").exclude(employee__designation="XEN").exclude(employee__designation="AEE")
        return render(request, 'leave/department_leaves.html', {'dept_leaves': dept_leaves})


def change_approval(request):
    approval_val = request.GET.get('approval_val')
    leavepk = request.GET.get('leavepk')
    sanctioned_by = int(request.GET.get('sanctionedby'))
    sanctioned_byuser = User.objects.get(pk=sanctioned_by)
    employee_pk = int(request.GET.get('employee'))
    employee = User.objects.get(pk = employee_pk)
    myobject = Leave.objects.filter(pk=leavepk)
    if approval_val == 'True':
        myobject.update(approval=approval_val, sanctioned_by=sanctioned_byuser)
        employee.available_leaves=employee.available_leaves-1
        mail_subject = 'Leave from ' + str(myobject[0].from_date) + ' to ' + str(myobject[0].to_date) + ' approved.'
        mail_message = 'Your following leave has been approved by ' + myobject[0].sanctioned_by.get_full_name() + '\n\n'\
                       'From ' + str(myobject[0].from_date) + ' to ' + str(myobject[0].to_date) + '\n\n'\
                       'Purpose: ' + myobject[0].purpose + '\n\n'\
                       'You have ' + str(employee.available_leaves) + ' leaves remaining.\n\n'\
                       'This is an autogenerated mail by the leave portal.'
        send_mail(mail_subject, mail_message, 'HPGCL Leave Portal <hpgcl@leaveportal.com>', [employee.email], fail_silently=False)
        employee.save()
    if approval_val == 'False':
        myobject.update(approval=approval_val, sanctioned_by=sanctioned_byuser)
        mail_subject = 'Leave from ' + str(myobject[0].from_date) + ' to ' + str(myobject[0].to_date) + ' denied.'
        mail_message = 'Your following leave has been denied by ' + myobject[0].sanctioned_by.get_full_name() + '\n\n'\
                       'From ' + str(myobject[0].from_date) + ' to ' + str(myobject[0].to_date) + '\n\n'\
                       'Purpose: ' + myobject[0].purpose + '\n\n'\
                       'You have ' + str(employee.available_leaves) + ' leaves remaining.\n\n'\
                       'This is an autogenerated mail by the leave portal.'
        send_mail(mail_subject, mail_message, 'HPGCL Leave Portal <hpgcl@leaveportal.com>', [employee.email], fail_silently=False)
        employee.save()
    data = {
        'valdb': 'True'
    }
    return JsonResponse(data)
