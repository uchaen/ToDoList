from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200) #할일의 제목. 리스트에 보여지는 글자
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False) #할일 완료시 True
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete']

