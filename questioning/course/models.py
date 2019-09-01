import os
import uuid

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now as timezone_now
from mdeditor.fields import MDTextField

from questioning.utils.models import CreatedUpdatedMixin


def image_upload_to(instance, filename):
    now = timezone_now()
    base, ext = os.path.splitext(filename)
    ext = ext.lower()
    return f'course/%Y/%m/{now:%Y/%m/%Y%m%d%H%M%S}{ext}'


@python_2_unicode_compatible
class CourseName(models.Model):
    """课程名"""
    uid = models.UUIDField(default=uuid.uuid4, verbose_name='uid',
                           primary_key=True, editable=False)
    name = models.CharField(default='', max_length=30, verbose_name='课程名')
    description = models.TextField(default='', verbose_name='类别描述')
    image = models.ImageField(upload_to=image_upload_to, blank=True, null=True,
                              verbose_name='封面图')

    class Meta:
        verbose_name = '课程名'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class CourseChapter(CreatedUpdatedMixin, models.Model):
    """课程章节"""
    # CHAPTER_TYPE = (
    #     (1, '大章节'),
    #     (2, '小章节'),
    # )
    uid = models.UUIDField(default=uuid.uuid4, verbose_name='uid',
                           primary_key=True, editable=False)
    title = models.CharField(default='', max_length=250, verbose_name='章节名')
    # chapter_type = models.CharField(choices=CHAPTER_TYPE, verbose_name='章节级别',
    #                                 max_length=10, default=1)
    parent_chapter = models.ForeignKey('self', on_delete=models.CASCADE,
                                       null=True, blank=True, verbose_name='父章节')

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Course(CreatedUpdatedMixin, models.Model):
    """课程"""
    uid = models.UUIDField(default=uuid.uuid4, verbose_name='uid',
                           primary_key=True, editable=False)
    title = models.CharField(default='', max_length=250, verbose_name='文章实际标题')
    content = MDTextField(verbose_name='内容')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             verbose_name='作者')
    chapter = models.ForeignKey(CourseChapter, on_delete=models.CASCADE,
                                )

    course_name = models.ForeignKey(CourseName, on_delete=models.CASCADE,
                                    verbose_name='课程名')

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
