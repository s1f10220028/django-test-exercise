from django.shortcuts import render
from django.http import Http404
from django.utils.timezone import make_aware  # タイムゾーンを含む日時を作成する関数をインポート
from django.utils.dateparse import parse_datetime  # 文字列からdatetimeオブジェクトを解析する関数をインポート
from todo.models import Task  # Taskモデルをインポート


# Create your views here.
def index(request):
    if request.method == 'POST':  # リクエストがPOSTメソッドの場合
        # 受け取ったデータを使ってTaskオブジェクトを作成し、データベースに保存
        task = Task(title=request.POST['title'],
                    due_at=make_aware(parse_datetime(request.POST['due_at'])))
        task.save()

    # order=dueというパラメータが指定されている場合、締切の早い順に表示
    if request.GET.get('order') == 'due':
        tasks = Task.objects.order_by('due_at')
    else:
        # それ以外の場合、登録の最新順に表示
        tasks = Task.objects.order_by('-posted_at')

    # コンテキストを作成し、テンプレートに渡す
    context = {
        'tasks': tasks
    }
    return render(request, 'todo/index.html', context)  # テンプレートをレンダリングし、レスポンスを返す


def detail(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")

    context = {
        'task': task,
    }
    return render(request, 'todo/detail.html', context)
