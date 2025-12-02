from django.contrib import admin
from .models import Document, DocumentVersion

# Встраивание версий внутрь документа
class DocumentVersionInline(admin.TabularInline):
    model = DocumentVersion
    extra = 0  # не показывать пустые формы
    readonly_fields = ('created_at', 'changed_by', 'diff')  # поля только для чтения
    can_delete = False

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'created_at', 'latest_version_display')
    list_filter = ('owner', 'created_at')
    search_fields = ('title', 'owner__username')
    inlines = [DocumentVersionInline]  # показываем версии внутри документа

    def latest_version_display(self, obj):
        latest = obj.latest_version()
        return latest.created_at if latest else 'Нет версий'
    latest_version_display.short_description = 'Последняя версия'

@admin.register(DocumentVersion)
class DocumentVersionAdmin(admin.ModelAdmin):
    list_display = ('document', 'created_at', 'changed_by')
    list_filter = ('created_at', 'changed_by')
    search_fields = ('document__title', 'changed_by__username')
    readonly_fields = ('created_at',)