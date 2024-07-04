from django.shortcuts import render
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

    # データベースから全てのTaskオブジェクトを取得
    tasks = Task.objects.all()

    # コンテキストを作成し、テンプレートに渡す
    context = {
        'tasks': tasks
    }
    return render(request, 'todo/index.html', context)  # テンプレートをレンダリングし、レスポンスを返す
