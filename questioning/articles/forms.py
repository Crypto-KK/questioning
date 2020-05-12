from django import forms


from questioning.articles.models import Article


class ArticleForm(forms.ModelForm):
    status = forms.CharField(widget=forms.HiddenInput(), initial='P')
    edited = forms.BooleanField(widget=forms.HiddenInput(),
                                initial=False, required=False)

    class Meta:
        fields = ['title', 'content', 'image', 'tags', 'status']
        model = Article
