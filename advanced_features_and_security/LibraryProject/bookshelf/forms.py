# LibraryProject/bookshelf/forms.py
from django import forms

class ExampleForm(forms.Form):
    query = forms.CharField(max_length=100, required=False, label="Search title")
    title = forms.CharField(max_length=200, required=False, label="New book title")

    def clean_query(self):
        # Strip whitespace; Django auto-escapes in templates.
        return (self.cleaned_data.get("query") or "").strip()

    def clean_title(self):
        return (self.cleaned_data.get("title") or "").strip()
