from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import LeaveForm
from .models import Leave, User
# Create your views here.


def home(request):
    if request.user.is_authenticated():
        return render(request, 'leave/index.html', {})
    else:
        return redirect('/accounts/login')


def submit_leave(request):
    if request.user.is_authenticated():
        if request.method == "POST":
            form = LeaveForm(request.POST)
            if form.is_valid():
                form_data = form.save(commit=False)
                form_data.employee = request.user
                form_data.save()
                return redirect('/')
        else:
            form = LeaveForm
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
    if myobject.exists():
        if str(myobject[0].approval) != approval_val:
            print("inside")
            myobject.update(approval=approval_val, sanctioned_by=sanctioned_byuser)
            employee.available_leaves=employee.available_leaves-1
            employee.save()
        boolval = 'True'
    else:
        boolval = 'False'
    data = {
        'valdb': boolval
    }
    return JsonResponse(data)
