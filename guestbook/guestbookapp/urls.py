from django.contrib import admin
from django.urls import path
from guestbookapp.views import index, select_msg, save_msg, delete_msg;

urlpatterns = [
    path('', index),
    path('<int:msg_id>/', select_msg),
    path('save/', save_msg),
    path('delete/<int:msg_id>/', delete_msg),
]
