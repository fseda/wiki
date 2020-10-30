from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.files.storage import default_storage
from markdown2 import Markdown
import random


from .util import save_entry, get_entry, list_entries
from .forms import NewEntryForm, SearchForm

markdown = Markdown()

# DONE
def index(request):
    """Show a list of existing entries"""

    return render(request, "encyclopedia/index.html", {
        "entries": list_entries(),
        "search_form": SearchForm()
    })
###

# DONE
def entry(request, title):
    """Display a selected entry page"""
    
    entries = []
    if not title:
        return render(request, "encyclopedia/search_error.html", {
            "title": "no_title",
            "entries": entries,
            "search_form": SearchForm()
        })

    for entry_title in list_entries():
        if entry_title.lower() == title.lower():
            content = markdown.convert(get_entry(entry_title))

            return render(request, "encyclopedia/entry.html", {
                "entry_title": title,
                "entry_content": content,
                "search_form": SearchForm()
            })

        elif title.lower() in entry_title.lower():
                entries.append(entry_title)

    # List related entry searches if no match is found
    return render(request, "encyclopedia/search_error.html", {
            "entry_title": title,
            "entries": entries,
            "search_form": SearchForm()
        })
###

# DONE
def new(request):
    """Add a new entry to memory"""

    # request method is "POST"
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        
        if form.is_valid():
            content = form.cleaned_data["content"]
            title = form.cleaned_data["title"]
            
            for entry_title in list_entries():
                if entry_title.lower() == title.lower():
                    return render(request, "encyclopedia/new_error.html", {
                        "heading": "Add New Entry",
                        "error": f'"{title}" already exists as "{entry_title}"',
                        "form": NewEntryForm
                    })
            
            save_entry(title, content)
            
            content = markdown.convert(content)

            return render(request, "encyclopedia/entry.html", {
                "entry_content": content,
                "entry_title": title,
                "search_form": SearchForm()
            })
            
        else:
            return render(request, "encyclopedia/new_error.html", {
                "heading": "Add New Entry",
                'error': 'Please fill "Title" and "Content" input fields.',
                "form": NewEntryForm,
                "search_form": SearchForm()
            })

    # request method is "GET"
    else:
        return render(request, "encyclopedia/new.html", {
            "heading": "Add New Entry",
            "form": NewEntryForm,
            "search_form": SearchForm()
        })
####

# DONE
def edit(request, title):
    """Edit an existing entry"""

    entry_title0 = title

    # request method is "GET"
    if request.method == "GET":
        content = get_entry(entry_title0)

        form = NewEntryForm(
            initial={
                'content': content
            })

        form.fields["title"].widget = forms.HiddenInput()
        form.fields["title"].required = False

        return render(request, "encyclopedia/edit.html", {
            "heading": "Edit Entry",
            'form': form,
            "entry_title": entry_title0,
            "search_form": SearchForm()
        })
    
    # request method is "POST"
    else:
        form = NewEntryForm(request.POST)

        form.fields["title"].required = False

        if form.is_valid():
            content = form.cleaned_data["content"]
            
            save_entry(title, content)

            content = markdown.convert(get_entry(title))

            return render(request, "encyclopedia/entry.html", {
                "entry_title": title,
                "entry_content": content,
                "search_form": SearchForm()
            })
            
        else:
            form = NewEntryForm()
            form.fields["title"].widget = forms.HiddenInput()

            return render(request, "encyclopedia/edit_error.html", {
                "heading": "Edit Entry",
                'error': 'Please fill "Content" input field.',
                "entry_title": entry_title0,
                "form": form,
                "search_form": SearchForm()
            })
###
    
#DONE
def random_entry(request):
    """Get a random entry page"""
    
    entry_title = random.choice(list_entries())
    content = markdown.convert(get_entry(entry_title))

    return render(request, "encyclopedia/entry.html", {
        "entry_title": entry_title,
        "entry_content": content,
        "search_form": SearchForm()
    })
###

# DONE
def delete(request):
    """Delete an entry from memory"""

    title1 = request.GET.get('d')
    if title1:
        filename = f"entries/{title1}.md"
        if default_storage.exists(filename):
            default_storage.delete(filename)
            return HttpResponseRedirect(reverse('wiki:index'))
###

# DONE
def search(request):
    """Search for an entry by keywords 
    via a form
    """ 
    form = SearchForm(request.POST)

    if form.is_valid():
        item = form.cleaned_data["item"]
        entries = []

        for entry_title in list_entries():
            if item.lower() == entry_title.lower():
                content = markdown.convert(get_entry(entry_title))
                
                return render(request, "encyclopedia/entry.html", {
                    "entry_content": content,
                    "entry_title": entry_title,
                    "search_form": SearchForm()
                })

            elif item.lower() in entry_title.lower():
                entries.append(entry_title)

        if not entries:
            return render(request, "encyclopedia/search_error.html", {
                "entry_title": item,
                "search_form": SearchForm()
            })
        
        return render(request, "encyclopedia/search.html", {
            "entry_title": item,
            "entries": entries,
            "search_form": SearchForm()
        })
###
            
            
