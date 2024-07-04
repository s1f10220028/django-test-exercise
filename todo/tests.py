from django.test import TestCase, Client
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


    def test_is_overdue_future(self):  # タスクが未来の日付で期限切れかどうかをテストするメソッドを定義
        # 2024/6/30 23:59:59のawareなdatetimeオブジェクトを作成
        due = timezone.make_aware(datetime(2024, 6, 30, 23, 59, 59))
        # 2024/6/30 0:0:0のawareなdatetimeオブジェクトを作成
        current = timezone.make_aware(datetime(2024, 6, 30, 0, 0, 0))
        
        # タイトル'task1'、締切日時dueを持つタスクを作成
        task = Task(title='task1', due_at=due)
        task.save()  # データベースに保存

        # タスクが現在の日時で期限切れでないことを確認
        self.assertFalse(task.is_overdue(current))




class TodoViewTestCase(TestCase):  # TestCaseクラスを継承してテストケースを定義
    def test_index_get(self):  # GETリクエストのテストメソッドを定義
        client = Client()  # テスト用のクライアントを作成
        response = client.get('/')  # ルートURLにGETリクエストを送信

        # ステータスコードが200（OK）であることを確認
        self.assertEqual(response.status_code, 200)
        # 使用されるテンプレートが'todo/index.html'であることを確認
        self.assertEqual(response.templates[0].name, 'todo/index.html')
        # コンテキストに渡される'tasks'が空であることを確認
        self.assertEqual(len(response.context['tasks']), 0)


    def test_index_post(self):  # POSTリクエストのテストメソッドを定義
        client = Client()  # テスト用のクライアントを作成
        # テストデータを定義
        data = {'title': 'Test Task', 'due_at': '2024-06-30 23:59:59'}
        response = client.post('/', data)  # ルートURLにPOSTリクエストを送信

        # ステータスコードが200（OK）であることを確認
        self.assertEqual(response.status_code, 200)
        # 使用されるテンプレートが'todo/index.html'であることを確認
        self.assertEqual(response.templates[0].name, 'todo/index.html')
        # コンテキストに渡される'tasks'が1件であることを確認
        self.assertEqual(len(response.context['tasks']), 1)


    def test_index_get_order_post(self):  # テストメソッドを定義
        # タスク1を作成し保存
        task1 = Task(title='task1', due_at=timezone.make_aware(datetime(2024, 7, 1)))
        task1.save()
        # タスク2を作成し保存
        task2 = Task(title='task2', due_at=timezone.make_aware(datetime(2024, 8, 1)))
        task2.save()

        client = Client()  # テスト用のクライアントを作成
        response = client.get('/?order=post')  # パラメータ'order=post'でGETリクエストを送信

        # ステータスコードが200（OK）であることを確認
        self.assertEqual(response.status_code, 200)
        # 使用されるテンプレートが'todo/index.html'であることを確認
        self.assertEqual(response.templates[0].name, 'todo/index.html')
        # コンテキストに渡される'tasks'の最初の要素がtask2であることを確認
        self.assertEqual(response.context['tasks'][0], task2)
        # コンテキストに渡される'tasks'の2番目の要素がtask1であることを確認
        self.assertEqual(response.context['tasks'][1], task1)


    def test_index_get_order_due(self):  # テストメソッドを定義
        # タスク1を作成して、保存
        task1 = Task(title='task1', due_at=timezone.make_aware(datetime(2024, 7, 1)))
        task1.save()
        # タスク2を作成して、保存
        task2 = Task(title='task2', due_at=timezone.make_aware(datetime(2024, 8, 1)))
        task2.save()

        client = Client()  # テスト用のクライアントを作成
        response = client.get('/?order=due')  # パラメータ'order=due'でGETリクエストを送信

        # ステータスコードが200（OK）であることを確認
        self.assertEqual(response.status_code, 200)
        # 使用されるテンプレートが'todo/index.html'であることを確認
        self.assertEqual(response.templates[0].name, 'todo/index.html')
        # コンテキストに渡される'tasks'の最初の要素がtask1であることを確認
        self.assertEqual(response.context['tasks'][0], task1)
        # コンテキストに渡される'tasks'の2番目の要素がtask2であることを確認
        self.assertEqual(response.context['tasks'][1], task2)
