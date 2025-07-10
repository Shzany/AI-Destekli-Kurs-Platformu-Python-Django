from django.db import models
from django.contrib.auth.models import User
from pages.models import Page

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    last_accessed = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'page']

    def __str__(self):
        return f"{self.user.username} - {self.page.title}"
