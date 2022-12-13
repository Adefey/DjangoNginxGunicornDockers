from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import DetailView
from .models import Message
import pickle
try:
    with open("./model.pk", "rb") as file:
        bytes_data = pickle.load(file)
        trained_model = pickle.loads(bytes_data)
except Exception:
    class TrainedModelMock:
        def __init__(self):
            pass
        def predict(self, text):
            return "Файл нейросети поврежден и/или отсутствует и не был загружен :("
    trained_model = TrainedModelMock()

def index(request):
    obj = Message.objects.all().order_by('-pk')
    return render(request, 'main.html',
                  {"obj":obj})

def select_msg(request, msg_id=0):
    item = Message.objects.get(pk = msg_id)
    return render(request, 'message.html',
                  {"msg_id": msg_id, "item" : item})

def save_msg(request):
    if request.method == "POST":
        obj = Message()
        if (request.POST.get("author") != "") and (request.POST.get("text") != ""):
            obj.author = request.POST.get("author")
            obj.text = request.POST.get("text")
            obj.answer = trained_model.predict(obj.text)
            obj.save();
    return HttpResponseRedirect("/")

def delete_msg(request, msg_id):
    item = Message.objects.get(pk = msg_id)
    item.delete()
    return HttpResponseRedirect("/")
