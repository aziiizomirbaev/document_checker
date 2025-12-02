from django import forms
from .models import Document, DocumentVersion

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title']

class DocumentVersionForm(forms.ModelForm):
    class Meta:
        model = DocumentVersion
        fields = ['file']