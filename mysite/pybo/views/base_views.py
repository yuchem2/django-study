from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from datetime import datetime, timedelta

from ..models import Question


def index(request):
    return redirect('pybo:question_list', category_id=1)


def detail(request, question_id):
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')
    sort = request.GET.get('sort', 'recommend')

    question = get_object_or_404(Question, pk=question_id)
    if sort == 'recent':
        answer_list = question.answer_set.order_by('-modify_date')
    else:
        answer_list = question.answer_set.annotate(voter_count=Count('voter')).order_by('-voter_count')
    paginator = Paginator(answer_list, 5)
    page_obj = paginator.get_page(page)

    context = {'question': question, 'answer_list': page_obj, 'page': page, 'kw': kw, 'sort': sort}
    response = render(request, 'pybo/question_detail.html', context)

    # hit functions(cookie)
    expire_date, now = datetime.now(), datetime.now()
    expire_date += timedelta(days=1)
    expire_date = expire_date.replace(hour=0, minute=0, second=0, microsecond=0)
    expire_date -= now
    max_age = expire_date.total_seconds()
    cookie_value = request.COOKIES.get('hitQuestion', '_')

    if f'_{question_id}_' not in cookie_value:
        cookie_value += f'{question_id}_'
        response.set_cookie('hitQuestion', value=cookie_value, max_age=max_age, httponly=True)
        question.hits += 1
        question.save()

    return response
