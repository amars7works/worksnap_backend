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
from django.conf.urls import url,include
from django.contrib import admin
from reports import views as reports_views
from reports import urls as reportsUrls

urlpatterns = [
    url(r'^s7_admin/', admin.site.urls),
    url(r'^api/',include(reportsUrls)),
    url(r'^api/',include('reports_2.urls')),
    url(r'^api/',include('s7_auth.urls')),
    url(r'^api/',include('summary_report.urls')),

]
