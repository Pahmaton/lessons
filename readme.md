- https://git-scm.com/book/ru/v2/
- https://djbook.ru/rel1.9/intro/tutorial01.html


# http протокол

вопросы в чем разница между get/post/delete
различия cтатус кодов 200/300/400/500
разница между query_string и body

httpbin.org/get
httpbin.org/post
httpbin.org/delete
httpbin.org/options

httpbin.org/status/200
httpbin.org/status/500

httpbin.org/ip
httpbin.org/user-agent



# django
https://docs.djangoproject.com/en/3.0/intro/tutorial01/#creating-the-polls-app

http://localhost:8000/admin

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})