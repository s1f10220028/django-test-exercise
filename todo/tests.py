from django.test import TestCase, Client
from django.utils import timezone
from datetime import datetime
from todo.models import Task


# Create your tests here.
class SampleTestCase(TestCase):
    def test_sample1(self):
        self.assertEqual(1 + 2, 3)


class TaskModelTestCase(TestCase):
    def test_create_task1(self):
        due = timezone.make_aware(datetime(2024, 6, 30, 23, 59, 59))
        task = Task(title='task1',  due_at=due)
        task.save()

        task = Task.objects.get(pk=task.pk)
        self.assertEqual(task.title, 'task1')
        self.assertFalse(task.completed)
        self.assertEqual(task.due_at, due)

    def test_creat_task2(self):
        task = Task(title='task2')
        task.save()

        task = Task.objects.get(pk=task.pk)
        self.assertEqual(task.title, 'task2')
        self.assertFalse(task.completed)
        self.assertEqual(task.due_at, None)

    def test_is_overdue_future(self):
        due = timezone.make_aware(datetime(2024, 6, 30, 23, 59, 59))
        current = timezone.make_aware(datetime(2024, 6, 30, 0, 0, 0))
        task = Task(title='task1', due_at=due)
        task.save()

        self.assertFalse(task.is_overdue(current))


class TodoViewTestCase(TestCase):
    def test_index_get(self):
        # GETメソッドで / にアクセスしたとき、
        # ・ステータスコード200
        # 適切なテンプレートが呼び出される
        # Taskの件数が0
        client = Client()
        responce = client.get('/')

        self.assertEqual(responce.status_code, 200)
        self.assertEqual(responce.templates[0].name, 'todo/index.html')
        self.assertEqual(len(responce.context['tasks']), 0)

    def test_index_post(self):
        # ☝（件数が1になるか）
        client = Client()
        data = {'title': 'Test Task', 'due_at': '2024-06-30 23:59:59'}
        responce = client.post('/', data)

        self.assertEqual(responce.status_code, 200)
        self.assertEqual(responce.templates[0].name, 'todo/index.html')
        self.assertEqual(len(responce.context['tasks']), 1)

    def test_index_get_order_post(self):
        # ソート(post順)Check
        task1 = Task(title='task1', due_at=timezone.make_aware(datetime(2024, 7, 1)))
        task1.save()
        task2 = Task(title='task2', due_at=timezone.make_aware(datetime(2024, 8, 1)))
        task2.save()
        client = Client()
        responce = client.get('/?order=post')

        self.assertEqual(responce.status_code, 200)
        self.assertEqual(responce.templates[0].name, 'todo/index.html')
        self.assertEqual(responce.context['tasks'][0], task2)
        self.assertEqual(responce.context['tasks'][1], task1)

    def test_index_get_order_due(self):
        # ソート(due順)Check
        task1 = Task(title='task1', due_at=timezone.make_aware(datetime(2024, 7, 1)))
        task1.save()
        task2 = Task(title='task2', due_at=timezone.make_aware(datetime(2024, 8, 1)))
        task2.save()
        client = Client()
        responce = client.get('/?order=due')

        self.assertEqual(responce.status_code, 200)
        self.assertEqual(responce.templates[0].name, 'todo/index.html')
        self.assertEqual(responce.context['tasks'][0], task1)
        self.assertEqual(responce.context['tasks'][1], task2)
