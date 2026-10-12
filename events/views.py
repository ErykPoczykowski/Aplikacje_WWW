from django.shortcuts import render

from django.http import HttpResponse

def welcome_view(request):
    return HttpResponse("Witaj w platformie EventHub – systemie obsługi wydarzeń i biletów!")

def about_view(request):
    return HttpResponse("Informacja o stronie")