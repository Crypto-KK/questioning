# Generated by Django 2.1.9 on 2019-08-25 11:41

from django.db import migrations
import mdeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='content',
            field=mdeditor.fields.MDTextField(verbose_name='内容'),
        ),
    ]
