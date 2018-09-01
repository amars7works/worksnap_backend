"""worksnaps_report URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from reports import views as reports_views

urlpatterns = [
    url(r'^biggboss/', admin.site.urls),
    url(r'^refesh_projects/',reports_views.create_project,name='refresh the projects'),
    url(r'^refesh_users/',reports_views.create_users,name='refresh the users'),
    url(r'^users_summary/',reports_views.create_users_summary,name='users summary reports'),
    url(r'^add_holiday/',reports_views.add_holiday_list,name='add holiday')

]
