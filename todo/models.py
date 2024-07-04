from django.db import models
from django.utils import timezone

# Create your models here.
class Task(models.Model):
    # タイトル
    title = models.CharField(max_length=100)
    # 完了しているか T/F
    completed = models.BooleanField(default=False)
    # 登録日 datetime デフォ現在時刻
    posted_at = models.DateTimeField(default=timezone.now)
    # 締切 datetime
    due_at = models.DateTimeField(null=True, blank=True)
