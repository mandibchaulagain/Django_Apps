from django.shortcuts import render

from django.http import HttpResponse

def home(request):
    people = [
        {'name': 'Mandib','age':22},
        {'name': 'Durga','age':9},
        {'name': 'Mohan','age':62},
        {'name': 'Hari','age':34},
        {'name': 'Raja','age':12},
        {'name': 'Bhai','age':90},
    ]
    text= """
        Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
    """
    return render(request,"index.html",context={'peoples':people,'page':'Home','text':text})

def about(request):
    context = {'page':'About'}
    return render(request,"about.html",context)

def failure_page(request):
    context = {'page':'Failure Page'}
    return render(request, "failure.html",context)