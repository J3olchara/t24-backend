from django.db import models


class Voice(models.Model):
    text = models.TextField()
    short_text = models.TextField()
    voice = models.FileField()
    input_file = models.FileField(null=True)
    session_id = models.CharField(max_length=128)

