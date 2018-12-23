from django import forms
from .models import User, Leave
from registration.forms import RegistrationForm

class MyCustomUserForm(RegistrationForm):
    class Meta:
        model = User
        exclude =  ['available_leaves', 'last_login', 'is_superuser', 'groups', 'user_permissions', 'is_staff', 'is_active', 'date_joined_0', 'date_joined_1', 'date_joined', 'password']

class LeaveForm(forms.ModelForm):
    def __init__(self, userdetails, request_method, *args, **kwargs):
        super (LeaveForm,self).__init__(*args,**kwargs)
        if request_method == 'GET':
            if userdetails.designation == 'SE':
                self.fields['noted_by'].queryset = User.objects.filter(power_station=userdetails.power_station, designation='CE')
                self.fields['noted_to'].queryset = User.objects.filter(power_station=userdetails.power_station, designation='SE')
            if userdetails.designation == 'XEN':
                self.fields['noted_by'].queryset = User.objects.filter(power_station=userdetails.power_station, designation='SE')
                self.fields['noted_to'].queryset = User.objects.filter(power_station=userdetails.power_station, designation='XEN')
            if userdetails.designation == 'AEE':
                self.fields['noted_by'].queryset = User.objects.filter(power_station=userdetails.power_station, designation='XEN')
                self.fields['noted_to'].queryset = User.objects.filter(power_station=userdetails.power_station, designation='AEE')

    class Meta:
        model = Leave
        fields = ('noted_by', 'from_date', 'to_date', 'purpose', 'noted_to')