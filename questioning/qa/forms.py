from django import forms

from questioning.qa.models import Question


class QuestionForm(forms.ModelForm):
    status = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Question
        fields = ['title', 'content', 'tags', 'status']

