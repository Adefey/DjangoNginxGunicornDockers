from django.contrib import admin
from django.urls import path
import guestbookapp.views

urlpatterns = [
    path('', guestbookapp.views.index),
    path('<int:msg_id>/', guestbookapp.views.select_msg),
    path('save/', guestbookapp.views.save_msg),
    path('delete/<int:msg_id>/', guestbookapp.views.delete_msg),
]
