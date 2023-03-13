from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group, User
from django.views import generic

from .models import Message
from django.urls import reverse


# Create your views here.
from django.views.generic import CreateView


def login_handler(request):
    if request.user.groups.filter(name='Student').exists():
        return render(request, 'student.html')
    if request.user.groups.filter(name='Admin').exists():
        return render(request,'admin.html')
    else:
        student_group = Group.objects.get(name='Student')
        student_group.user_set.add(request.user)
        return render(request, 'student.html')


class SeasView(generic.ListView):
    model = Message
    template_name = 'seas.html'
    fields = ['message_text']

    def get_queryset(self):
        return Message.objects.all()



class ClasView(CreateView):
    template_name = 'clas.html'
    model = User
    fields = ['email']


def post(request):
    m = Message(message_text=request.POST.get("message", ""))
    m.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
