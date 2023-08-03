from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Count

from ..forms import CommentForm
from ..models import Question, Answer, Comment


@login_required(login_url='common:login')
def question_comment_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.category = question.category
            comment.parent_content = question.subject
            comment.save()
            question.comments.add(comment)
            return redirect('pybo:detail', question_id=question_id)
    else:
        form = CommentForm()

    page = request.GET.get('page', '1')
    answer_list = question.answer_set.annotate(voter_count=Count('voter')).order_by('-voter_count')
    paginator = Paginator(answer_list, 5)
    page_obj = paginator.get_page(page)
    context = {'question': question, 'answer_list': page_obj, 'page': page, 'form': form}
    return render(request, 'pybo/question_detail.html', context)


@login_required(login_url='common:login')
def answer_comment_create(request, answer_id, page_num):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.category = answer.question.category
            comment.parent_content = answer.content
            comment.save()
            answer.comments.add(comment)
            return redirect('pybo:detail', question_id=answer.question.id)
    else:
        form = CommentForm()

    question = get_object_or_404(Question, pk=answer.question_id)
    answer_list = question.answer_set.annotate(voter_count=Count('voter')).order_by('-voter_count')
    page = request.GET.get('page', page_num)
    paginator = Paginator(answer_list, 5)
    page_obj = paginator.get_page(page)
    context = {'question': question, 'answer_list': page_obj, 'page': page, 'form': form}
    return render(request, 'pybo/question_detail.html', context)


@login_required(login_url='common:login')
def comment_vote(request, question_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    try:
        if request.user == comment.author:
            messages.error(request, '본인이 작성한 댓글은 추천할 수 없습니다')
        elif request.user.voter_question.all().get(id=comment_id):
            messages.error(request, '이미 추천을 누른 댓글은 추천할 수 없습니다')
    except Question.DoesNotExist:
        comment.voter.add(request.user)
    return redirect('pybo:detail', question_id=question_id)


@login_required(login_url='common:login')
def comment_vote_del(request, question_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.voter.remove(request.user)
    return redirect('pybo:detail', question_id=question_id)


@login_required(login_url='common:login')
def comment_delete(request, question_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '삭제권한이 없습니다.')
        return redirect('pybo:detail', question_id=question_id)
    comment.delete()
    return redirect('pybo:detail', question_id=question_id)


@login_required(login_url='common:login')
def comment_modify(request, question_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('pybo:detail', question_id=question_id)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('pybo:detail', question_id=question_id)
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)
