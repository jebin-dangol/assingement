from django.db import models
from django.conf import settings
from .utils import generate_short_code

class ShortURL(models.Model):
    original_url = models.URLField(max_length=500)
    short_code = models.CharField(max_length=10, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    clicks = models.IntegerField(default=0)
    expires_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.short_code:
            self.short_code = generate_short_code()
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        if self.expires_at:
            from django.utils import timezone
            return timezone.now() > self.expires_at
        return False

    def __str__(self):
        return f"{self.short_code} -> {self.original_url}"
