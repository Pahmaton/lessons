import uuid

from django.db import models


def get_file_path(instance, filename):
    return f"{uuid.uuid4()}.wav"


class AudioFile(models.Model):
    text = models.TextField()
    files = models.FileField(upload_to=get_file_path)
    file_name = models.TextField()
    file_time = models.TextField()
    real_file_name = models.TextField()

    class Meta:
        verbose_name_plural = "Файлы записей"

    def __str__(self):
        return f'{self.file_name}'




