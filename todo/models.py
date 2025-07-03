from django.db import models
from django.utils import timezone # FFF

# Create your models here.
class Task(models.Model):
    # タイトル
    title = models.CharField(max_length=100)
    # 完了しているか T/F
    completed = models.BooleanField(default=False)
    # 登録日 デフォ:現在時刻
    posted_at = models.DateTimeField(default=timezone.now)
    # 締切 null可
    due_at = models.DateTimeField(null=True,blank=True)

    def is_overdue(self, dt):
        if self.due_at is None:
            return False
        return self.due_at < dt
