from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group, User
from django.views import generic
import os, fileinput
import requests
from django.templatetags.static import static
import json

from .models import Message, Offering, Transfer, ApprovedTransfer, NewApprovedSchool
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


class SeasTransferView(generic.ListView):
    model = Transfer
    template_name = 'equivalencies.html'
    fields = ['transferClass', 'title', 'transferCredits', 'UVAClass', 'UVACredits']

    def get_queryset(self):
        return Transfer.objects.all()


class ApprovedTransferView(generic.ListView):
    model = ApprovedTransfer
    template_name = 'approved.html'
    def get_queryset(self):
        return ApprovedTransfer.objects.all()


class SeasView(generic.ListView):
    model = NewApprovedSchool
    template_name = 'seas.html'
    fields = ['school_name', 'index']
    def get_queryset(self):
        return NewApprovedSchool.objects.all()


def approveTransfer(request):
    me=Message.objects.get(id=request.GET.get('id'))
    school = me.school_name
    i = 118
    flag= False
    new = me.class_number + "\t" + me.message_text + "\t" + me.class_credits + "\t" + me.equivalency_name + \
        "\t" + me.UVA_credits
    listings = open('mysite/static/mysite/transfer.txt', 'r')
    lines = listings.readlines()
    listings.close()
    with open('mysite/static/mysite/transfer.txt', 'w') as new_listings:
        for line in lines:
            if school in line:
                new_listings.write(line)
                new_listings.write(new)
                new_listings.write('\n')
                flag=True
            else:
                new_listings.write(line)
    new_listings.close()

    if not flag:
        neq = NewApprovedSchool(school_name=school, index=i+NewApprovedSchool.objects.count())
        neq.save()
        listings_2 = open('mysite/static/mysite/transfer.txt', 'r')
        lines_2 = listings_2.readlines()
        listings_2.close()
        new_school = "$"+school
        with open('mysite/static/mysite/transfer.txt', 'w') as new_listings_2:
            for item in lines_2:
                if "End" in item:
                    new_listings_2.write(new_school)
                    new_listings_2.write('\n')
                    new_listings_2.write(new)
                    new_listings_2.write('\n')
                    new_listings_2.write(item)
                else:
                    new_listings_2.write(item)
        new_listings_2.close()

    req=ApprovedTransfer(class_name=me.message_text,school_name=me.school_name,equivalency_name=me.equivalency_name)
    me.delete()
    req.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def denyTransfer(request):
    me = Message.objects.get(id=request.GET.get('id'))
    me.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class ClasView(CreateView):
    template_name = 'clas.html'
    model = User
    fields = ['email']


def post(request):
    m = Message(class_number=request.POST.get("message4", ""), message_text=request.POST.get("message", ""),
                class_credits=request.POST.get("message5", ""), UVA_credits=request.POST.get("message6", ""),
                school_name=request.POST.get("message2", ""), equivalency_name=request.POST.get("message3", ""),
                user=request.user)
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


def transfer(request):
    Transfer.objects.all().delete()
    index = request.POST.get("transfer", "")
    listings = open('mysite/static/mysite/transfer.txt', 'r')
    lines = listings.readlines()
    max = len(lines)
    count = 0
    countIter = 0
    while countIter < max:
        if lines[countIter][0] == "$":
            count+=1
            if count == int(index):
                countIter+=1
                while lines[countIter][0] != "$":
                    data = lines[countIter].strip('\n').split('\t')
                    print(data)
                    t = Transfer(transferClass=data[0], title=data[1], transferCredits=data[2], UVAClass=data[3], UVACredits=data[4])
                    t.save()
                    countIter+=1
            countIter+=1
        else:
            countIter+=1

    return HttpResponseRedirect('equivalencies')

class PendingView(generic.ListView):
    model = Message
    template_name = 'pending.html'
    fields = ['message_text']
#what does get_attr do
    def get_queryset(self):
        return Message.objects.all()

def pend(request):
    pendlist=Message.objects.all().filter(user=request.user)
    return render(request,'pending.html',{'list':pendlist})
