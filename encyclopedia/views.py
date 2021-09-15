from django.shortcuts import render
import markdown2
from . import util
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

class NewTaskFormT(forms.Form):
    title = forms.CharField(widget=forms.Textarea, label="Title", max_length=100, help_text='100 characters max.')

class NewTaskFormC(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label="Content", max_length=100, help_text='100 characters max.')

class NewTaskFormE(forms.Form):
    edit = forms.CharField(required=False)

def index(request):
    lists = util.list_entries()
    lists.remove('Error404')
    lists.remove('ErrorR')
    return render(request, "encyclopedia/index.html", {
        "entries": lists
    })

def title(request, item):

    mk = util.get_entry(item)

    for i in range(len(mk)):
        if mk[i:i+1]=='\n':
            break
    title = mk[2:i]
    mk2html = markdown2.markdown(mk)
    return render(
        request,
        "encyclopedia/title.html",
        {"title": title, "body": mk2html, "form": NewTaskFormE()})

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

        form = NewTaskFormT(request.POST)
        if form.is_valid():
            titled = form.cleaned_data["title"]
        else:
            return render(request,"encyclopedia/new_page.html", {
                "form": form
            })

        form = NewTaskFormC(request.POST)
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

        data = []
        data.append(titled)

        return title(request, titled)
 
    return render(request, "encyclopedia/new_page.html",
        {"title": NewTaskFormT(),"content": NewTaskFormC()
        })

def edit_page(request):

    if request.method == "POST":
        form = NewTaskFormE(request.POST)
        if form.is_valid():
            edit = form.cleaned_data["edit"]
        print(form)
        print("Este es edit:", edit)

    return render(request, "encyclopedia/edit_page.html",
        {"title": NewTaskFormE()
        })