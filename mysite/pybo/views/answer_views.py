from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone
from django.db.models import Count

from ..forms import AnswerForm
from ..models import Question, Answer


@login_required(login_url='common:login')
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.modify_date = answer.create_date
            answer.question = question
            answer.save()
            return redirect('{}#answer_{}'.format(resolve_url('pybo:detail', question_id=question.id), answer.id))
    else:
        form = AnswerForm()
    page = request.GET.get('page', '1')
    answer_list = question.answer_set.annotate(voter_count=Count('voter')).order_by('-voter_count')
    paginator = Paginator(answer_list, 5)
    page_obj = paginator.get_page(page)
    context = {'question': question, 'answer_list': page_obj, 'page': page, 'form': form}
    return render(request, 'pybo/question_detail.html', context)


@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=answer.question.id)
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()  # 수정일시 저장
            answer.save()
            return redirect(
                '{}#answer_{}'.format(resolve_url('pybo:detail', question_id=answer.question.id), answer.id))
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'pybo/answer_form.html', context)


@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        answer.delete()
    return redirect('pybo:detail', question_id=answer.question.id)


@login_required(login_url='common:login')
def answer_vote(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    try:
        if request.user == answer.author:
            messages.error(request, '본인이 작성한 답변은 추천할 수 없습니다')
        elif request.user.voter_answer.all().get(id=answer_id):
            messages.error(request, '이미 추천을 누른답변은 추천할 수 없습니다')
    except Answer.DoesNotExist:
        answer.voter.add(request.user)
    return redirect('{}#answer_{}'.format(resolve_url('pybo:detail', question_id=answer.question.id), answer.id))


@login_required(login_url='common:login')
def answer_vote_del(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    answer.voter.remove(request.user)
    return redirect('pybo:detail', question_id=answer.question.id)
