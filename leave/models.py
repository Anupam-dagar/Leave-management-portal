from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    DESIGNATION_CHOICES = (
        ("CE", "CE"),
        ("SE", "SE"),
        ("XEN", "XEN"),
        ("AEE", "AEE"),
    )
    STATION_CHOICES = (
        ("Hisar", "Hisar"),
        ("Panipat", "Panipat"),
        ("Yamuna Nagar", "Yamuna Nagar"),
        ("Panchkula", "Panchkula"),
    )
    DEPARTMENT_CHOICES = (
        ("MP&GS", "MP&GS"),
        ("O&M1", "O&M1"),
        ("O&M2", "QAO&M2"),
        ("M&T", "M&T"),
        ("MM&Store", "MM&Store"),
        ("Civil", "Civil"),
    )
    department = models.CharField(max_length=200, blank=False, null=False, choices=DEPARTMENT_CHOICES)
    available_leaves = models.IntegerField(default=15)
    designation = models.CharField(max_length=200, blank=False, null=False, choices=DESIGNATION_CHOICES)
    power_station = models.CharField(max_length=200, blank=False, null=False, choices=STATION_CHOICES, default="")

    def __str__(self):
        return self.first_name + ' - ' + self.department

    def __unicode__(self):
        return self.first_name + ' - ' + self.department

class Leave(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    sanctioned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_sanctioned', blank=True, null=True)
    noted_to =  models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_noted', blank=False, null=False)
    from_date = models.DateField(blank=False, null=False)
    to_date = models.DateField(blank=False, null=False)
    purpose = models.CharField(max_length=1200, blank=False, null=False)
    approval = models.BooleanField(default=False, blank=False, null=False)

    def __str__(self):
        return self.employee.first_name + ': ' + str(self.from_date) + ' - ' + str(self.to_date)

    def __unicode__(self):
        return self.employee.first_name + ': ' + str(self.from_date) + ' - ' + str(self.to_date)
