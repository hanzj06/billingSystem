from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from Apps.Baseinfo import models
def index(request):
    return HttpResponse("Hello")


def test
