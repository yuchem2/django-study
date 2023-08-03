from django.urls import path
from .views import base_views, question_views, answer_views, comment_views

app_name = 'pybo'

urlpatterns = [
    # base_views.py
    path('', base_views.index, name='index'),
    path('question/detail/<int:question_id>/', base_views.detail, name='detail'),

    # question_views.py
    path('question/create/', question_views.question_create, name='question_create'),
    path('question/modify/<int:question_id>/', question_views.question_modify, name='question_modify'),
    path('question/delete/<int:question_id>/', question_views.question_delete, name='question_delete'),
    path('question/vote/<int:question_id>/', question_views.question_vote, name='question_vote'),
    path('question/vote/del/<int:question_id>/', question_views.question_vote_del, name='question_vote_del'),
    path('question/list/<int:category_id>/', question_views.question_list, name='question_list'),

    # answer_views.py
    path('answer/create/<int:question_id>/', answer_views.answer_create, name='answer_create'),
    path('answer/modify/<int:answer_id>/', answer_views.answer_modify, name='answer_modify'),
    path('answer/delete/<int:answer_id>/', answer_views.answer_delete, name='answer_delete'),
    path('answer/vote/<int:answer_id>/', answer_views.answer_vote, name='answer_vote'),
    path('answer/vote/del/<int:answer_id>/', answer_views.answer_vote_del, name='answer_vote_del'),

    # comment_views.py
    path('question/comment/create/<int:question_id>/', comment_views.question_comment_create, name='question_comment_create'),
    path('answer/comment/create/<int:answer_id>/<str:page_num>', comment_views.answer_comment_create, name='answer_comment_create'),
    path('comment/vote/<int:question_id>?<int:comment_id>', comment_views.comment_vote, name='comment_vote'),
    path('comment/vote/del/<int:question_id>?<int:comment_id>', comment_views.comment_vote_del, name='comment_vote_del'),
    path('comment/del/<int:question_id>?<int:comment_id>', comment_views.comment_delete, name='comment_delete'),
    path('comment/modify/<int:question_id>?<int:comment_id>', comment_views.comment_modify, name='comment_modify'),
]