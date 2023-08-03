import markdown
from django import template
from django.utils.safestring import mark_safe
from django import forms

from ..forms import AnswerForm, QuestionForm, CommentForm

register = template.Library()


@register.filter
def sub(value, arg):
    return value - arg


@register.filter
def mark(value):
    extensions = ["nl2br", "fenced_code"]
    return mark_safe(markdown.markdown(value, extensions=extensions))


@register.filter
def find_voter(voter, arg):
    return arg.voter.filter(id=voter.id).exists()


@register.filter
def check_label(source, arg):
    if isinstance(source, forms.ModelForm):
        for field in source:
            return field.label == arg
    else:
        return False


@register.filter
def include(source, arg):
    return str(arg) in source


@register.filter
def slice_end(source, arg):
    return source[:arg]

@register.filter
def slice_start(source, arg):
    return source[arg:]
