import markdown2
from random import choice
from django.shortcuts import render
from django import forms
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import date


from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from . import util

class Searchen(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={'class' : 'myfieldclass', 'placeholder': 'Search...'}), label='Search Here')

class Post(forms.Form):
    name = forms.CharField(label= "Name of Article")
    textarea = forms.CharField(widget=forms.Textarea())

class Delete(forms.Form):
    delete_this = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Full Name of Page'}), label='Delete Pages')

def index(request):
    if request.method == "GET":
        return render(request, "C:/users/defen/downloads/wiki/encyclopedia/templates/encyclopedia/index.html", {
            "entries": util.list_entries(),
            "form": Searchen(),
        })
    else:
        retrievedsearch = Searchen(request.POST)
        if retrievedsearch.is_valid():
            queryenEn = retrievedsearch.cleaned_data["query"]
        queryenEn = str(queryenEn).lower()
        results = []
        none = False
        _, filenames = default_storage.listdir("C:/users/defen/downloads/wiki/entries")
        for filename in filenames:
            filename = str(filename)
            if queryenEn in filename.lower():
                filename = filename.replace('\'', '')
                filename = filename[:-3]
                filename = filename.replace(' ', '%20')
                results.append(f"{filename}")
        for result in results:
            format(result)
        if len(results) == 1:
            return HttpResponseRedirect(f"/{results[0]}")
        if len(results) == 0:
            none = True
        return render(request, "C:/users/defen/downloads/wiki/encyclopedia/templates/encyclopedia/searchpage.html", {
            "form": Searchen,
            "results": results,
            "none": none,
        })
        

def entry(request, name):
    try:
        bome = open(f"C:/users/defen/downloads/wiki/entries/{name}.md", "r")
        entrylist = util.list_entries()
        namecap = str({name})
        namecap = namecap.replace('{', '')
        namecap = namecap.replace('}', '')
        namecap = namecap.replace('\'', '')
    except FileNotFoundError:
        return HttpResponse(status=404)
    else:
        return render(request, "C:/users/defen/downloads/wiki/encyclopedia/templates/encyclopedia/entry.html", {
            "content": markdown2.markdown_path(f"C:/users/defen/downloads/wiki/entries/{name}.md"),
            "name": str({name}),
            "namecap": namecap,
            "form": Searchen,
        })

def add(request):
    if request.method == "GET":
        return render(request, "C:/users/defen/downloads/wiki/encyclopedia/templates/encyclopedia/add.html", {
            "form": Searchen(),
            "post": Post(),
        })
    else:
        rob = False
        retrievedpost = Post(request.POST)
        if retrievedpost.is_valid():
            thetitle = retrievedpost.cleaned_data["name"]
            content = retrievedpost.cleaned_data["textarea"]
        thetitle = str({thetitle})
        thetitle = thetitle.replace('{', '')
        thetitle = thetitle.replace('}', '')
        thetitle = thetitle.replace('\'', '')
        entrylist = util.list_entries()
        if thetitle in entrylist:
            rob = True
            return render(request, "C:/users/defen/downloads/wiki/encyclopedia/templates/encyclopedia/add.html", {
            "form": Searchen(),
            "post": Post(),
            "rob": rob
        })
        util.save_entry(thetitle, content)
        contentpage = util.get_entry(thetitle)
        
        return render(request, "C:/users/defen/downloads/wiki/encyclopedia/templates/encyclopedia/entry.html", {
            "content": markdown2.markdown_path(f"C:/users/defen/downloads/wiki/entries/{thetitle}.md"),
            "namecap": thetitle,
            "form": Searchen(),
        })

def edit(request, namecap):
    if request.method == "GET":
        preparedcontent = util.get_entry(namecap)
        return render(request, "C:/users/defen/downloads/wiki/encyclopedia/templates/encyclopedia/edit.html", {
            "form": Searchen(),
            "namecap": namecap,
            "editor": Post(initial={'textarea': preparedcontent, 'name': namecap,}),
        })
    if request.method == "POST":
        edited = Post(request.POST)
        if edited.is_valid() == False:
            editedcontent = edited.cleaned_data["textarea"]
        util.save_entry(str(namecap), editedcontent)
        return render(request, "C:/users/defen/downloads/wiki/encyclopedia/templates/encyclopedia/entry.html", {
            'form': Searchen(),
            'content': markdown2.markdown_path(f"C:/users/defen/downloads/wiki/entries/{namecap}.md"),
            'namecap': namecap
        })

def random(request):
    _, filenames = default_storage.listdir("C:/users/defen/downloads/wiki/entries")
    randomentry = choice(filenames)
    randomentry = randomentry[:-3]
    return render(request, "C:/users/defen/downloads/wiki/encyclopedia/templates/encyclopedia/entry.html", {
        "content": markdown2.markdown_path(f"C:/users/defen/downloads/wiki/entries/{randomentry}.md"),
        "name": str({randomentry}),
        "namecap": randomentry,
        "form": Searchen,
    })

def delete(request):
    if request.method == "POST":
        bob = True
        form = Delete(request.POST)
        if form.is_valid():
            deletedfile = form.cleaned_data["delete_this"]
        deletedfile = str(deletedfile)
        deletedfile.replace('\'', '')
        if default_storage.exists(f"C:/users/defen/downloads/wiki/entries/{deletedfile}.md"):
            default_storage.delete(f"C:/users/defen/downloads/wiki/entries/{deletedfile}.md")
            deletestatus = "Successful"
        else:
            deletestatus = "Unsuccessful (Page not found)"
        return render(request, "C:/users/defen/downloads/wiki/encyclopedia/templates/encyclopedia/delete.html", {
            "entries": util.list_entries(),
            "form": Searchen(),
            "bob": bob,
            "delete": Delete(),
            "status": deletestatus
        })
    else:
        bob = False
        return render(request, "C:/users/defen/downloads/wiki/encyclopedia/templates/encyclopedia/delete.html", {
            "entries": util.list_entries(),
            "form": Searchen(),
            "delete": Delete(),
        })