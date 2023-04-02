from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group, User
from django.views import generic
import requests
import json


from .models import Message, Offering, ApprovedTransfer
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

def viewSeas(request):
    if request.user.groups.filter(name='Student').exists():
        return render(request,'seas.html')

class SeasReqView(generic.ListView):
    model = Message
    template_name = 'seasadmin.html'
    fields = ['message_text']
#what does get_attr do
    def get_queryset(self):
        return Message.objects.all()
    def __str__(self):
        return self.email


class SeasSearchView(generic.ListView):
    model = Offering
    template_name = 'results.html'
    fields = ['section', 'name', 'day', 'enrollment', 'if_full']

    def get_queryset(self):
        return Offering.objects.all()


class ApprovedTransferView(generic.ListView):
    model = ApprovedTransfer
    template_name = 'approved.html'
    def get_queryset(self):
        return ApprovedTransfer.objects.all()

def approveTransfer(request):
    me=Message.objects.first()
    req=ApprovedTransfer(class_name=me.message_text,school_name=me.school_name,equivalency_name=me.equivalency_name)
    me.delete()
    req.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def denyTransfer(request):
    me = Message.objects.first()
    me.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class ClasView(CreateView):
    template_name = 'clas.html'
    model = User
    fields = ['email']


def post(request):
    m = Message(message_text=request.POST.get("message", ""),school_name=request.POST.get("message2",""),equivalency_name=request.POST.get("message3",""))
    m.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def search(request):
    subj = request.POST.get("search", "")
    url = 'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1232'
    Offering.objects.all().delete()
    r = requests.get(url + '&subject=' + subj)

    for c in r.json():
        o = Offering(section=c['subject']+' '+c['catalog_nbr']+'-'+c['class_section'], name=c['descr'], day=c['meetings'][0]['days']+' '+c['meetings'][0]['start_time'][0:5]+'-'+c['meetings'][0]['end_time'][0:5], enrollment=str(c['enrollment_available']), if_full=isfull(c['enrollment_available']))
        o.save()
    return HttpResponseRedirect('results')


def isfull(n):
    if n > 0:
        return False
    else:
        return True
