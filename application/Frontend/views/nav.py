from django.shortcuts import render

def index(response):
    return render(response, "index.html")