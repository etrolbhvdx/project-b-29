from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group, User
from django.views import generic
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
import os, fileinput
import requests
from django.templatetags.static import static
import json

from .models import Message, Message_AS, Offering, Transfer, Transfer_AS, ApprovedTransfer, DeniedTransfer, ApprovedTransfer_AS, NewApprovedSchool, NewApprovedSchool_AS
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


@method_decorator(user_passes_test(lambda u: u.groups.filter(name='Admin').exists()), name='dispatch')
class SeasReqView(generic.ListView):
    model = Message
    template_name = 'seasadmin.html'
    fields = ['message_text']
#what does get_attr do
    def get_queryset(self):
        return Message.objects.all()
    def __str__(self):
        return self.email


@method_decorator(user_passes_test(lambda u: u.groups.filter(name='Admin').exists()), name='dispatch')
class ASReqView(generic.ListView):
    model = Message_AS
    template_name = 'clasadmin.html'
    fields = ['message_text']
#what does get_attr do

    def get_queryset(self):
        return Message_AS.objects.all()

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


class ClasTransferView(generic.ListView):
    model = Transfer_AS
    template_name = 'ASequivalencies.html'
    fields = ['transferClass', 'title', 'transferCredits', 'UVAClass', 'UVACredits']

    def get_queryset(self):
        return Transfer_AS.objects.all()


class ApprovedTransferView(generic.ListView):
    model = ApprovedTransfer
    template_name = 'approved.html'
    def get_queryset(self):
        return ApprovedTransfer.objects.all()


@method_decorator(user_passes_test(lambda u: u.groups.filter(name='Student').exists()), name='dispatch')
class SeasView(generic.ListView):
    model = NewApprovedSchool
    template_name = 'seas.html'
    fields = ['school_name', 'index']

    def get_queryset(self):
        return NewApprovedSchool.objects.all()


@method_decorator(user_passes_test(lambda u: u.groups.filter(name='Student').exists()), name='dispatch')
class ClasView(generic.ListView):
    template_name = 'clas.html'
    model = NewApprovedSchool_AS
    fields = ['school_name', 'index']


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

    req=ApprovedTransfer(class_name=me.message_text,school_name=me.school_name,equivalency_name=me.equivalency_name,user=request.user)
    me.delete()
    req.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def approveTransfer_AS(request):
    me_AS=Message_AS.objects.get(id=request.GET.get('id'))
    school = me_AS.school_name
    i = 0
    flag= False
    new = me_AS.class_number + "\t" + me_AS.message_text + "\t" + me_AS.class_credits + "\t" + me_AS.equivalency_name + \
        "\t" + me_AS.UVA_credits
    listings = open('mysite/static/mysite/transfer_AS.txt', 'r')
    lines = listings.readlines()
    listings.close()
    with open('mysite/static/mysite/transfer_AS.txt', 'w') as new_listings:
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
        neq_AS = NewApprovedSchool_AS(school_name=school, index=i+NewApprovedSchool_AS.objects.count())
        neq_AS.save()
        listings_2 = open('mysite/static/mysite/transfer_AS.txt', 'r')
        lines_2 = listings_2.readlines()
        listings_2.close()
        new_school = "$"+school
        with open('mysite/static/mysite/transfer_AS.txt', 'w') as new_listings_2:
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

    req_AS=ApprovedTransfer_AS(class_name=me_AS.message_text,school_name=me_AS.school_name,equivalency_name=me_AS.equivalency_name)
    me_AS.delete()
    req_AS.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def denyTransfer(request):
    me = Message.objects.get(id=request.GET.get('id'))
    req = DeniedTransfer(class_name=me.message_text, school_name=me.school_name, equivalency_name=me.equivalency_name,
                           user=request.user)
    me.delete()
    req.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def denyTransfer_AS(request):
    me_AS = Message_AS.objects.get(id=request.GET.get('id'))
    me_AS.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def post(request):
    m = Message(class_number=request.POST.get("message4", ""), message_text=request.POST.get("message", ""),
                class_credits=request.POST.get("message5", ""), UVA_credits=request.POST.get("message6", ""),
                school_name=request.POST.get("message2", ""), equivalency_name=request.POST.get("message3", ""),
                user=request.user, site_url=request.POST.get("message7", ""))
    m.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def post_AS(request):
    m_as = Message_AS(class_number=request.POST.get("message4", ""), message_text=request.POST.get("message", ""),
                class_credits=request.POST.get("message5", ""), UVA_credits=request.POST.get("message6", ""),
                school_name=request.POST.get("message2", ""), equivalency_name=request.POST.get("message3", ""),
                site_url=request.POST.get("message7", ""))

    m_as.save()
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
                    t = Transfer(transferClass=data[0], title=data[1], transferCredits=data[2], UVAClass=data[3], UVACredits=data[4])
                    t.save()
                    countIter+=1
            countIter+=1
        else:
            countIter+=1
        listings.close()

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
    apprlist=ApprovedTransfer.objects.all().filter(user=request.user)
    denylist=DeniedTransfer.objects.all().filter(user=request.user)
    return render(request,'pending.html',{'list':pendlist,'appr':apprlist,'deny':denylist})

def freeSearch(request):
    Transfer.objects.all().delete()
    keyword = request.POST.get("searchNum", "")
    contents = open('mysite/static/mysite/transfer.txt', 'r')
    line_data = contents.readlines()
    num = len(line_data)
    n = 0
    internalCount = 0
    newCount = 0
    t = Transfer(transferClass="No Results", title="", transferCredits="", UVAClass="", UVACredits="")
    while n<num:
        if line_data[n][0] == "$":
            t = Transfer(transferClass=line_data[n][1:], title="", transferCredits="", UVAClass="", UVACredits="")
            n += 1
            internalCount = 0
        else:
            if keyword.lower() in line_data[n].lower():
                newCount += 1
                new_data = line_data[n].strip('\n').split('\t')
                s = Transfer(transferClass=new_data[0], title=new_data[1], transferCredits=new_data[2], UVAClass=new_data[3],
                             UVACredits=new_data[4])
                internalCount += 1
                if internalCount == 1:
                    t.save()
                    s.save()
                else:
                    s.save()
                n += 1
            else:
                n += 1
    if newCount == 0:
        t = Transfer(transferClass="No Results", title="", transferCredits="", UVAClass="", UVACredits="")
        t.save()

    return HttpResponseRedirect('equivalencies')


def freeSearchAS(request):
    Transfer_AS.objects.all().delete()
    keyword = request.POST.get("searchNumAS", "")
    contents = open('mysite/static/mysite/transfer_AS.txt', 'r')
    line_data = contents.readlines()
    num = len(line_data)
    n = 0
    internalCount = 0
    newCount = 0
    t = Transfer_AS(transferClass="No Results", title="", transferCredits="", UVAClass="", UVACredits="")
    while n < num:
        if line_data[n][0] == "$":
            t = Transfer_AS(transferClass=line_data[n][1:], title="", transferCredits="", UVAClass="", UVACredits="")
            n += 1
            internalCount = 0
        else:
            if keyword.lower() in line_data[n].lower():
                newCount += 1
                new_data = line_data[n].strip('\n').split('\t')
                s = Transfer_AS(transferClass=new_data[0], title=new_data[1], transferCredits=new_data[2],
                             UVAClass=new_data[3],
                             UVACredits=new_data[4])
                internalCount += 1
                if internalCount == 1:
                    t.save()
                    s.save()
                else:
                    s.save()
                n += 1
            else:
                n += 1
    if newCount == 0:
        t = Transfer_AS(transferClass="No Results", title="", transferCredits="", UVAClass="", UVACredits="")
        t.save()

    return HttpResponseRedirect('ASequivalencies')

def transfer_AS(request):
    Transfer_AS.objects.all().delete()
    index_AS = request.POST.get("transfer_AS", "")
    listings_AS = open('mysite/static/mysite/transfer_AS.txt', 'r')
    lines_AS = listings_AS.readlines()
    max_AS = len(lines_AS)
    count_AS = 0
    countIter_AS = 0
    while countIter_AS < max_AS:
        if lines_AS[countIter_AS][0] == "$":
            count_AS+=1
            if count_AS == int(index_AS)+1:
                countIter_AS+=1
                while lines_AS[countIter_AS][0] != "$":
                    data_AS = lines_AS[countIter_AS].strip('\n').split('\t')
                    t_AS = Transfer_AS(transferClass=data_AS[0], title=data_AS[1], transferCredits=data_AS[2], UVAClass=data_AS[3], UVACredits=data_AS[4])
                    t_AS.save()
                    countIter_AS+=1
            countIter_AS+=1
        else:
            countIter_AS+=1
        listings_AS.close()

    return HttpResponseRedirect('ASequivalencies')
