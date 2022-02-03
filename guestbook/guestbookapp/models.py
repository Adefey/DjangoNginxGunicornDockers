from django.db import models

class Message(models.Model):
    author = models.TextField()
    text = models.TextField()
    date = models.DateField(auto_now_add=True)
    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ('-date', )


