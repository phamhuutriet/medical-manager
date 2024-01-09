"""
URL configuration for medicalManager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('service/user/<str:uid>/doctors/', include("medicalManagerWeb.urls.doctor_urls")),
    path('service/access/', include("medicalManagerWeb.urls.access_urls")),
    path('service/user/<str:uid>/roles/', include("medicalManagerWeb.urls.role_urls")),
    path('service/user/<str:uid>/patients/', include("medicalManagerWeb.urls.patient_urls")),
    path('service/user/<str:uid>/templates/', include("medicalManagerWeb.urls.template_urls")),
]
