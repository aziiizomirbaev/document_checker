from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Document(models.Model):
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def latest_version(self):
        return self.versions.order_by('-created_at').first()

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('document-detail', args=[str(self.pk)])


class DocumentVersion(models.Model):
    document = models.ForeignKey(Document, related_name='versions', on_delete=models.CASCADE)
    version_number = models.PositiveIntegerField(default=1)
    file = models.FileField(upload_to='documents/')
    created_at = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    diff = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.pk:
            last = self.document.versions.order_by('-version_number').first()
            self.version_number = last.version_number + 1 if last else 1
        super().save(*args, **kwargs)