from django.test import TestCase
from django.utils import timezone
from datetime import datetime
from todo.models import Task
# Create your tests here.
class SampleTestCase(TestCase):
    def test_sample(self):
        self.assertEqual(1 + 2, 3)

class TaskModelTestCase(TestCase):  # TestCaseクラスを継承してテストケースを定義
    def test_create_task1(self):  # テストメソッドを定義
        # 2024/6/30 23:59:59のawareなdatetimeオブジェクトを作成
        due = timezone.make_aware(datetime(2024, 6, 30, 23, 59, 59))  

        # タイトル'task1'、締切日時dueを持つタスクを作成
        task = Task(title='task1', due_at=due)
        task.save()  # データベースに保存

        # データベースからタスクを取得
        task = Task.objects.get(pk=task.pk)

        # タスクのタイトルが'task1'であることをCheck
        self.assertEqual(task.title, 'task1')
        # タスクが未完了状態であることをCheck
        self.assertFalse(task.completed)
        # タスクの締切日時をCheck
        self.assertEqual(task.due_at, due)


    def test_create_task2(self):  # 新しいテストメソッドを定義
        # タイトル'task2'のタスクを作成
        task = Task(title='task2')
        task.save()  # データベースに保存

        # データベースからタスクを取得
        task = Task.objects.get(pk=task.pk)

        # タスクのタイトルが'task2'であることを確認
        self.assertEqual(task.title, 'task2')
        # タスクが未完了状態であることを確認
        self.assertFalse(task.completed)
        # タスクの締切日時がNoneであることを確認
        self.assertEqual(task.due_at, None)
