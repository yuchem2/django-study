# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    subject = models.CharField(max_length=200)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_comment')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_comment')
    parent_content = models.TextField(null=True, default='')
    content = models.TextField(null=True, default='')
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_comment')


class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_question')
    subject = models.CharField(max_length=200)          # 글자 수의 길이가 제한된 텍스트를 이용할 때
    content = models.TextField(null=True, default='')   # 글자 수를 제한할 수 없는 텍스트를 이용할 때
    create_date = models.DateTimeField()                # 생성된 날짜와 시간에 관계된 필드.
    modify_date = models.DateTimeField(null=True, blank=True)               # 수정 날짜
    voter = models.ManyToManyField(User, related_name='voter_question')     # 추천인 추가
    comments = models.ManyToManyField(Comment, related_name='comment_question')
    hits = models.DecimalField(max_digits=7, decimal_places=0, default=0)

    def __str__(self):
        return self.subject


class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField(null=True, default='')
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_answer')
    comments = models.ManyToManyField(Comment, related_name='comment_answer')
