"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

from login import views

app_name = 'TransferGuide'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name="index.html")),
    path('accounts/', include('allauth.urls')),
    path('logout/', LogoutView.as_view()),
    path('home/', views.login_handler),
    path('home/seas/', views.SeasView.as_view()),
    path('home/seas/admin/', views.SeasReqView.as_view()),
    path('home/clas/admin', views.ASReqView.as_view()),
    path('home/seas/results', views.SeasSearchView.as_view()),
    path('home/seas/admin/results', views.SeasSearchView.as_view()),
    path('home/clas/results', views.SeasSearchView.as_view()),
    path('home/seas/equivalencies', views.SeasTransferView.as_view()),
    path('home/seas/admin/equivalencies', views.SeasTransferView.as_view()),
    path('home/clas/', views.ClasView.as_view()),
    path('home/seas/post', views.post),
    path('home/clas/post_AS', views.post_AS),
    path('home/clas/search', views.search),
    path('home/seas/search', views.search),
    path('home/seas/transfer', views.transfer),
    path('home/seas/admin/transfer', views.transfer),
    path('home/seas/approved',views.ApprovedTransferView.as_view()),
    path('home/seas/post', views.post),
    path('home/seas/search', views.search),
    path('home/seas/admin/post', views.post),
    path('home/seas/admin/search', views.search),
    path('home/seas/admin/approveTransfer',views.approveTransfer),
    path('home/clas/approveTransfer_AS', views.approveTransfer_AS),
    path('home/clas/denyTransfer_AS', views.denyTransfer_AS),
    path('home/clas/transfer_AS', views.transfer_AS),
    path('home/clas/ASequivalencies', views.ClasTransferView.as_view()),
    path('home/seas/admin/denyTransfer',views.denyTransfer),
    path('home/pending',views.pend),
    path('home/seas/freeSearch', views.freeSearch)
]
