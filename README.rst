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

创建用户
^^^^^^^^^^^^^^^^^^^^^

* 创建一个 **普通用户**只需要去登录界面，使用邮箱注册一个用户。

* 创建一个 **超级用户**, 使用以下命令::

    $ python manage.py createsuperuser


类型检查
^^^^^^^^^^^

使用mypy运行类型检查:

::

  $ mypy questioning

测试覆盖度
^^^^^^^^^^^^^

运行测试程序、查看你的测试覆盖度报告，生成HTML测试覆盖度报告页面::

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ pytest

Live reloading and Sass CSS compilation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Moved to `Live reloading and SASS compilation`_.

.. _`Live reloading and SASS compilation`: http://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html



Celery
^^^^^^

本项目需要使用Celery.

运行一个Celery worker:

.. code-block:: bash

    cd questioning
    celery -A config.celery_app worker -l info

Please note: For Celery's import magic to work, it is important *where* the celery commands are run. If you are in the same folder with *manage.py*, you should be right.





Deployment
----------

The following details how to deploy this application.




