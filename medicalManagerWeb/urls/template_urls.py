from django.urls import path
from ..views.template_views import *

urlpatterns = [
    path('', multiple_template_view, name="multiple_template_view"),
    path('<str:tid>/', single_template_view, name="single_template_view"),
]