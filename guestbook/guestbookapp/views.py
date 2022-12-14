from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import DetailView
from .models import Message
import sys
import os
import requests


def index(request):
    obj = Message.objects.all().order_by('-pk')
    return render(request, 'main.html',
                  {"obj": obj})


def select_msg(request, msg_id=0):
    item = Message.objects.get(pk=msg_id)
    return render(request, 'message.html',
                  {"msg_id": msg_id, "item": item})


def save_msg(request):
    if request.method == "POST":
        obj = Message()
        if (request.POST.get("author") != "") and (request.POST.get("text") != ""):
            obj.author = request.POST.get("author")
            obj.text = request.POST.get("text")
            feature = {"feature": obj.text}
            response = requests.get(
                "http://127.0.0.1:3310/predict", json=feature)
            obj.answer = response.json()["result"]
            obj.save()
    return HttpResponseRedirect("/")


def delete_msg(request, msg_id):
    item = Message.objects.get(pk=msg_id)
    item.delete()
    return HttpResponseRedirect("/")
