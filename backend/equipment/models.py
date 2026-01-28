from django.db import models

class Dataset(models.Model):
    file = models.FileField(upload_to='datasets/')
    summary = models.JSONField()
    columns = models.JSONField(default=list)  # ✅ ADD DEFAULT
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dataset {self.id}"