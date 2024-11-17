from django.shortcuts import render

from django.http import HttpResponse

def index(request):
    return HttpResponse("You are at poll index.")

def detail(request, question_id):
    return HttpResponse("You're looking at question %s" %question_id)

def results(request, question_id):
    response = "You're looking at the results of the question %s"
    return HttpResponse(response %question_id)

def votes(request, question_id):
    return HttpResponse("You're voting on question %s" %question_id)
