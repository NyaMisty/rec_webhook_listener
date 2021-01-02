from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('bilirec', views.BilirecHookView.as_view(), name='BilirecHookView'),
    path('vtbrec', views.VtbrecHookView.as_view(), name='VtbrecHookView'),
]