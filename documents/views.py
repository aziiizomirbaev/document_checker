from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count
from django.db.models.functions import TruncDate

from .models import Document, DocumentVersion
from .forms import DocumentForm, DocumentVersionForm
from .utils import text_from_docx_filefield, generate_unified_diff


@login_required
def dashboard_data(request):
    qs = DocumentVersion.objects.filter(document__owner=request.user)
    data = qs.annotate(day=TruncDate('created_at'))\
             .values('day').annotate(count=Count('id')).order_by('day')
    labels = [item['day'].strftime('%Y-%m-%d') for item in data]
    counts = [item['count'] for item in data]
    return JsonResponse({'labels': labels, 'counts': counts})


@login_required
def document_list(request):
    documents = Document.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'documents/document_list.html', {'documents': documents})


@login_required
def document_detail(request, pk):
    document = get_object_or_404(Document, pk=pk, owner=request.user)
    versions = document.versions.all()
    return render(request, 'documents/document_detail.html', {'document': document, 'versions': versions})


@login_required
def document_create(request):
    if request.method == "POST":
        form = DocumentForm(request.POST)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.owner = request.user
            doc.save()
            return redirect('document-list')
    else:
        form = DocumentForm()
    return render(request, 'documents/document_form.html', {'form': form})


@login_required
def version_create(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if document.owner != request.user:
        return redirect('document-detail', pk=document.pk)

    if request.method == "POST":
        form = DocumentVersionForm(request.POST, request.FILES)
        if form.is_valid():
            version = form.save(commit=False)
            version.document = document
            version.changed_by = request.user
            version.save()
            prev = document.versions.exclude(pk=version.pk).order_by('-created_at').first()
            old_text = text_from_docx_filefield(prev.file) if prev else ""
            new_text = text_from_docx_filefield(version.file)
            version.diff = generate_unified_diff(old_text, new_text)
            version.save(update_fields=['diff'])
            return redirect('document-detail', pk=document.pk)
    else:
        form = DocumentVersionForm()
    return render(request, 'documents/version_form.html', {'form': form, 'document': document})