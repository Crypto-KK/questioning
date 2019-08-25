import uuid
from collections import Counter, defaultdict

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from mdeditor.fields import MDTextField
from markdownx.utils import markdownify
from slugify import slugify
from taggit.managers import TaggableManager

from questioning.utils.models import CreatedUpdatedMixin
from qa import QUESTION_STATUS, QUESTION_TYPE


@python_2_unicode_compatible
class Vote(CreatedUpdatedMixin, models.Model):
    """
    contenttype通用投票模型
    """
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='qa_vote',
                             on_delete=models.CASCADE)
    value = models.BooleanField(default=True, verbose_name='赞同or反对')
    """contenttype通用外键"""
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                     related_name='vote_on')
    object_id = models.CharField(max_length=255)
    vote = GenericForeignKey()

    class Meta:
        verbose_name = '投票'
        verbose_name_plural = verbose_name
        unique_together = ('user', 'content_type', 'object_id')
        index_together = ('content_type', 'object_id')


@python_2_unicode_compatible
class QuestionQuerySet(models.query.QuerySet):
    '''自定义question的查询集'''
    def get_answered(self):
        '''获取已经有答案的问题'''
        return self.filter(has_answer=True).select_related('user')

    def get_unanswered(self):
        '''还没有答案的问题'''
        return self.filter(has_answer=False).select_related('user')

    def get_counted_tags(self):
        '''获取所有标签的数量'''
        d = defaultdict(int)
        for obj in self.all():
            for tag in obj.tags.names():
                d[tag] += 1
        return d.items()


@python_2_unicode_compatible
class Question(CreatedUpdatedMixin, models.Model):

    title = models.CharField(max_length=255, verbose_name='标题')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='q_author', null=True, blank=True)
    content = MDTextField()
    slug = models.SlugField(max_length=255, null=True, blank=True, verbose_name='url别名')
    status = models.CharField(max_length=1, choices=QUESTION_STATUS, default='O',
                              verbose_name='问题状态')
    qtype = models.CharField(max_length=1, choices=QUESTION_TYPE, default='F',
                              verbose_name='问题类型')
    tags = TaggableManager(help_text='请用,隔开')
    has_answer = models.BooleanField(default=False, verbose_name='是否有正确回答')
    votes = GenericRelation(Vote, verbose_name='投票情况')
    objects = QuestionQuerySet.as_manager()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Question, self).save(force_insert=False, force_update=False, using=None,
             update_fields=None)

    def __str__(self):
        return self.title

    def get_markdown(self):
        return markdownify(self.content)

    def total_votes(self):
        '''获取总票数'''
        d = Counter(self.votes.values_list('value', flat=True))
        return d[True] - d[False]

    def get_answers(self):
        '''获取所有回答'''
        return Answer.objects.filter(question=self)

    def count_answers(self):
        '''获取回答数'''
        return self.get_answers().count()

    def get_upvoters(self):
        '''获取赞同的用户'''
        return [vote.user for vote in self.votes.filter(value=True)]

    def get_downvoters(self):
        '''获取踩的用户'''
        return [vote.user for vote in self.votes.filter(value=False)]

    def get_accepted_answers(self):
        '''获取被采纳的答案'''
        return Answer.objects.get(question=self, is_answer=True)

    class Meta:
        verbose_name = '问题'
        verbose_name_plural = verbose_name
        ordering = ('-created_at', )


@python_2_unicode_compatible
class Answer(CreatedUpdatedMixin, models.Model):
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='a_author')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = MDTextField()
    is_answer = models.BooleanField(default=False, verbose_name='是否为采纳的答案')

    votes = GenericRelation(Vote, verbose_name='投票')

    class Meta:
        verbose_name = '问答'
        verbose_name_plural = verbose_name
        ordering = ('-is_answer', '-created_at')

    def __str__(self):
        return self.content

    def get_markdown(self):
        return markdownify(self.content)

    def total_votes(self):
        '''获取回答的总票数'''
        d = Counter(self.votes.values_list('value', flat=True))
        return d[True] - d[False]

    def get_upvoters(self):
        '''获取赞同该答案的用户'''
        return [vote.user for vote in self.votes.filter(value=True)]

    def get_downvoters(self):
        '''获取踩该答案的用户'''
        return [vote.user for vote in self.votes.filter(value=False)]

    def accept_answer(self):
        '''接受回答为正确答案'''

        answer_set = Answer.objects.filter(question=self.question)
        answer_set.update(is_answer=False)

        self.is_answer = True
        self.save()

        self.question.has_answer = True
        self.question.save()
