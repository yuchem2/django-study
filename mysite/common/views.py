# Create your views here.
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from common.forms import UserForm, PasswordFindForm, PasswordForm, IDFindForm

from pybo.models import Question, Answer, Comment


def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)   # 사용자 인증
            login(request, user)    # 로그인
            return redirect('pybo:index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})


@login_required(login_url='common:login')
def profile(request, user_id):
    if request.method == "POST":
        user = get_object_or_404(User, pk=user_id)
        raw_password = request.POST.get('password')
        if user.check_password(raw_password):
            return redirect('common:password_modify', user_id=user_id)
        else:
            messages.error(request, '비밀번호가 틀렸습니다.')

    question_list = Question.objects.filter(author_id=user_id).order_by('create_date')
    answer_list = Answer.objects.filter(author_id=user_id).order_by('create_date')
    comment_list = Comment.objects.filter(author_id=user_id).order_by('create_date')
    context = {'question_list': question_list, 'answer_list': answer_list, 'comment_list': comment_list}
    return render(request, 'common/profile.html', context)


def password_find(request):
    if request.method == "POST":
        form = PasswordFindForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            if not User.objects.filter(username=username).exists():
                messages.error(request, '존재하지 않는 ID입니다.')
            elif not User.objects.filter(email=email).exists():
                messages.error(request, '존재하지 않는 email입니다.')
            else:
                user = User.objects.get(username=username)
                return redirect('common:password_modify', user_id=user.id)

    else:
        form = PasswordFindForm()
    return render(request, 'common/password_find.html', {'form': form})


def password_modify(request, user_id):
    user = User.objects.get(id=user_id)
    pre_password = user.password
    if request.method == "POST":
        form = PasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('password1')
            if pre_password == new_password:
                messages.error(request, '이전 비밀번호와 동일합니다.')
            else:
                user.set_password(new_password)
                user.save()
                user = authenticate(username=user.username, password=new_password)
                return redirect('common:login')
    else:
        form = PasswordForm()
    context = {'form': form}
    return render(request, 'common/password_modify.html', context)


def id_find(request):
    if request.method == "POST":
        form = IDFindForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if not User.objects.filter(email=email).exists():
                messages.error(request, '존재하지 않는 email입니다.')
            else:
                user = User.objects.get(email=email)
                context = {'username': user.username}
                return render(request, 'common/id_find_result.html', context)
    else:
        form = IDFindForm()
    context = {'form': form}
    return render(request, 'common/id_find.html', {'form': form})
