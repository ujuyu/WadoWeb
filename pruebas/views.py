from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse
from django.template import loader

# Create your views here.
def index(request):
    context = {}
    template = loader.get_template("pruebas/index.html")
    return HttpResponse(template.render(context, request))
