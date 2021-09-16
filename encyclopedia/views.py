from django.shortcuts import render
import markdown2
from . import util
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from random import randint

class FormT(forms.Form):
    title = forms.CharField(widget=forms.Textarea(attrs={'placeholder': ''}), max_length=100)

class FormC(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': ''}), max_length=100)

class FormE(forms.Form):
    edit = forms.CharField(widget=forms.TextInput, required=False)

def index(request):

    lists = util.list_entries()
    lists.remove('Error404')
    lists.remove('ErrorR')

    return render(request, "encyclopedia/index.html", {
        "entries": lists
    })

def title(request, item):

    flag = 0
    mk = util.get_entry(item)
    mk2html = markdown2.markdown(mk)

    if item == 'ErrorR' or item == 'Error404':
        flag = 1

    return render(
        request,
        "encyclopedia/title.html",
        {"title": item, "body": mk2html, "flag":flag})

def search(request):

    if request.method == "GET":
        form = request.GET
        value = form.dict()["q"]

    lists = util.list_entries()
    new_list = []

    for l in lists:
        if value in l:
            new_list.append(l)

    if new_list == []:
        item = "Error404"
        return title(request,item)

    return render(request, "encyclopedia/search.html",
        {"matches": new_list})

def new_page(request):

    if request.method == "POST":

        form = FormT(request.POST)

        if form.is_valid():
            titled = form.cleaned_data["title"]
        else:
            return render(request,"encyclopedia/new_page.html", {
                "form": form
            })

        form = FormC(request.POST)

        if form.is_valid():
            content = form.cleaned_data["content"]
        else:
            return render(request,"encyclopedia/new_page.html", {
                "form": form
            })

        if titled in util.list_entries():
            return title(request, 'ErrorR')

        if ((titled != '') and (content != '')):
            util.save_entry(titled,content)

        last = title(request, titled)
        
    else:
        last = render(request, "encyclopedia/new_page.html",
        {"title": FormT(),"content": FormC()
        })
    
    return last

def edit_page(request):

    titled = ''
    content = ''

    if request.method == "POST":

        form = FormE(request.POST)

        if form.is_valid():

            titled = form.cleaned_data["edit"]

        content = util.get_entry(titled)

    return render(request, "encyclopedia/edit_page.html",
        {"title": titled,"content": content
        })

def editing(request):

    if request.method == "POST":
        
        form = FormT(request.POST)
        if form.is_valid():
            titled = form.cleaned_data["title"]
        else:
            return render(request,"encyclopedia/edit_page.html", {
                "form": form
            })

        form = FormC(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
        else:
            return render(request,"encyclopedia/edit_page.html", {
                "form": form
            })

        if ((titled != '') and (content != '')):
            util.save_entry(titled,content)

        last = title(request, titled)

    return last

def random_page(request):

    lists = util.list_entries()
    lists.remove('Error404')
    lists.remove('ErrorR')
    value = randint(0, len(lists)-1)
    titled = lists[value]
    last = title(request, titled)

    return last



