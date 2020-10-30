from django import forms

from .util import save_entry, get_entry, list_entries

class NewEntryForm(forms.Form):
    title = forms.CharField(
        label="title",
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Title',
                'style': 'width: 10cm',
                'autocomplete': 'off'
            }
        ),
        help_text='Please use "_" instead of spaces for the title.'
    )
    content = forms.CharField(
        label="content",
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Input entry content here.',
                'style': 'width: 90%'
            }
        )
    )
    
class SearchForm(forms.Form):
    item = forms.CharField(
        label="title", 
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Search Encyclopedia',
                'style': 'width: 100%; height: 10%;',
                'autocomplete': 'off'
            }
        )
    )
