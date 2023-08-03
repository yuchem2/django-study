from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Q, Count

from ..forms import QuestionForm
from ..models import Question, Category


def question_list(request, category_id):
    page = request.GET.get('page', '1')  # page
    kw = request.GET.get('kw', '')  # search
    sort = request.GET.get('sort', 'recent')
    category = get_object_or_404(Category, pk=category_id)
    if sort == 'recommend':
        question_list = Question.objects.filter(category=category_id).annotate(voter_count=Count('voter')).order_by('-voter_count')
    else:
        question_list = Question.objects.filter(category=category_id).order_by('-create_date')

    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(answer__content__icontains=kw) |  # 답변 내용 검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색
        ).distinct()
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj, 'page': page, 'kw': kw, 'sort': sort, 'category': category}
    return render(request, 'pybo/question_list.html', context)


@login_required(login_url='common:login')
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()  # 수정일시 저장
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=question_id)
    question.delete()
    return redirect('pybo:index')


@login_required(login_url='common:login')
def question_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        if request.user == question.author:
            messages.error(request, '본인이 작성한 글은 추천할 수 없습니다')
        elif request.user.voter_question.all().get(id=question_id):
            messages.error(request, '이미 추천을 누른 글은 추천할 수 없습니다')
    except Question.DoesNotExist:
        question.voter.add(request.user)
    return redirect('pybo:detail', question_id=question.id)


@login_required(login_url='common:login')
def question_vote_del(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.voter.remove(request.user)
    return redirect('pybo:detail', question_id=question.id)
