questioning
===========

Django开发的问答网站

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style


:License: MIT


设置
--------

跳转到 设置_.

.. _settings: http://cookiecutter-django.readthedocs.io/en/latest/settings.html

基本命令
--------------

项目运行
^^^^^^^^^^^^^^^^^^^^^

* 版本要求：Python3.6及以上版本、Django2.2.0以上版本
* 依赖说明：使用虚拟环境，使用如下命令安装依赖::

    $ pip install -r requirements.txt

* 使用以下命令生成 **数据库迁移文件**::

    $ python manage.py makemigrations

* 使用以下命令创建 **空数据表**::

    $ python manage.py migrate

* 使用以下命令创建 **超级管理员账号**::

    $ python manage.py createsuperuser

* 使用以下命令在开发机中运行项目::

    $ python manage.py runserver 0.0.0.0:8000

* 如需编辑项目中的配置信息，请在项目目录下编辑.env文件

* 访问/xadmin进入后台管理系统

Celery
^^^^^^

本项目需要使用Celery.

运行一个Celery worker:

.. code-block:: bash

    cd questioning
    celery -A config.celery_app worker -l info
