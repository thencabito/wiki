from django.shortcuts import render
import markdown2
from . import util
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from random import randint

class NewTaskFormT(forms.Form):
    title = forms.CharField(widget=forms.Textarea(attrs={'placeholder': ''}), label="Title", max_length=100)
    def __init__(self, *args, **kwargs):
        super(NewTaskFormT, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            self.fields[field_name].widget.attrs['placeholder'] = field.label
class NewTaskFormC(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': ''}), label="Content", max_length=100)

class NewTaskFormE(forms.Form):
    edit = forms.CharField(widget=forms.TextInput, label="Edit", required=False)

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
        {"title": title, "body": mk2html})

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

        last = title(request, titled)
        
    else:
        last = render(request, "encyclopedia/new_page.html",
        {"title": NewTaskFormT(),"content": NewTaskFormC()
        })
    
    return last

def edit_page(request):

    titled = ''
    content = ''

    if request.method == "POST":
        form = NewTaskFormE(request.POST)
        if form.is_valid():
            titled = form.cleaned_data["edit"]
        content = util.get_entry(titled)

    #title_form = forms.CharField(widget=forms.Textarea(attrs={'placeholder': titled}), label="Title", max_length=100)
    #content_form = forms.CharField(widget=forms.Textarea(attrs={'placeholder': content}), label="Title", max_length=100)
    #print(form.order_fields())
    return render(request, "encyclopedia/edit_page.html",
        {"title": NewTaskFormT(),"content": NewTaskFormC()
        })

def editing(request):

    if request.method == "POST":
        
        form = NewTaskFormT(request.POST)
        if form.is_valid():
            titled = form.cleaned_data["title"]
        else:
            return render(request,"encyclopedia/edit_page.html", {
                "form": form
            })

        form = NewTaskFormC(request.POST)
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



