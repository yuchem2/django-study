
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count

from ..models import Question


def index(request):
    return redirect('pybo:question_list', category_id=1)


def detail(request, question_id):
    page = request.GET.get('page', '1')
    question = get_object_or_404(Question, pk=question_id)
    answer_list = question.answer_set.annotate(voter_count=Count('voter')).order_by('-voter_count')
    paginator = Paginator(answer_list, 5)
    page_obj = paginator.get_page(page)
    context = {'question': question, 'answer_list': page_obj, 'page': page}
    return render(request, 'pybo/question_detail.html', context)
