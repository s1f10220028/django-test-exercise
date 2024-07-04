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
    
    # ★メソッド
    def is_overdue(self, dt):  # タスクが期限切れかどうかを判定するメソッドを定義
        # 締切日時が設定されていない場合、Falseを返す
        if self.due_at is None:
            return False
        # 締切日時が指定された日時より前かどうかを判定し、その結果を返す
        return self.due_at < dt
