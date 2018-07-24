from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^submit/$', views.submit_leave, name='submit_leave'),
    url(r'^leaves/$', views.your_leaves, name='your_leaves'),
    url(r'^departmentleaves/$', views.department_leaves, name='department_leaves'),
    url(r'^api/changeapproval/$', views.change_approval, name='change_approval'),
]

