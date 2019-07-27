# Generated by Django 2.1.9 on 2019-07-27 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': '用户', 'verbose_name_plural': '用户'},
        ),
        migrations.RemoveField(
            model_name='user',
            name='name',
        ),
        migrations.AddField(
            model_name='user',
            name='github',
            field=models.URLField(blank=True, max_length=255, null=True, verbose_name='Github链接'),
        ),
        migrations.AddField(
            model_name='user',
            name='introduction',
            field=models.TextField(blank=True, null=True, verbose_name='简介'),
        ),
        migrations.AddField(
            model_name='user',
            name='job_title',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='职称'),
        ),
        migrations.AddField(
            model_name='user',
            name='linkedin',
            field=models.URLField(blank=True, max_length=255, null=True, verbose_name='LinkedIn链接'),
        ),
        migrations.AddField(
            model_name='user',
            name='location',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='城市'),
        ),
        migrations.AddField(
            model_name='user',
            name='nickname',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='昵称'),
        ),
        migrations.AddField(
            model_name='user',
            name='personal_url',
            field=models.URLField(blank=True, max_length=255, null=True, verbose_name='个人链接'),
        ),
        migrations.AddField(
            model_name='user',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics/', verbose_name='头像'),
        ),
        migrations.AddField(
            model_name='user',
            name='weibo',
            field=models.URLField(blank=True, max_length=255, null=True, verbose_name='微博链接'),
        ),
        migrations.AddField(
            model_name='user',
            name='zhihu',
            field=models.URLField(blank=True, max_length=255, null=True, verbose_name='知乎链接'),
        ),
    ]
