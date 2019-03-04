====================
Django Settings Toml
====================

This project is used to configure  `Django <https://www.djangoproject.com>`_ projects using a `Toml <https://github.com/toml-lang/toml>`_ configuration file. This project chooses Toml over other configuration language becuase of it's simplicity and small specification. It is easier to understand and looks very much like INI-style config. We couldn't use INI-style because it is difficult to repsent data structures like dictionaries and lists, and there is no support for nesting.

Usage
=====

To use this in your Django project, Add the following to your ``settings.py`` file::

  # settings.py
  from django_settings_toml import load_settings

  load_settings(__name__, ['/etc/project.toml', '~/.project.toml'])


Then, you can run your django project like this::

  $ DJANGO_SETTINGS_MODULE=project.settings django-admin runserver


Example Settings
================
::

   # /etc/project.toml
   # SECURITY WARNING: keep the secret key used in production secret!
   SECRET_KEY = 'change-this-on-your-production-server'

   # SECURITY WARNING: don't run with debug turned on in production!
   DEBUG = false

   ADMINS = [
   ['Mailman Suite Admin', 'root@localhost'],
   ]

   # Application definition
   INSTALLED_APPS = [
   'django.contrib.admin',
   'django.contrib.auth',
   'django.contrib.contenttypes',
   'django.contrib.sessions',
   'django.contrib.sites',
   'django.contrib.messages',
   'django.contrib.staticfiles',
   'rest_framework',
   'django_q',
   'allauth',
   ]

   MIDDLEWARE = [
   'django.contrib.sessions.middleware.SessionMiddleware',
   'django.middleware.common.CommonMiddleware',
   'django.middleware.csrf.CsrfViewMiddleware',
   'django.middleware.locale.LocaleMiddleware',
   'django.contrib.auth.middleware.AuthenticationMiddleware',
   'django.contrib.messages.middleware.MessageMiddleware',
   'django.middleware.clickjacking.XFrameOptionsMiddleware',
   'django.middleware.security.SecurityMiddleware',
   ]

   ROOT_URLCONF = 'project.urls'

   WSGI_APPLICATION = 'project.wsgi.application'

   [DATABASES.default]
   ENGINE = 'django.db.backends.sqlite3'
   NAME = 'mailmansuite.db'

   [LOGGING]
   version = 1
   disable_existing_loggers = false

   [LOGGING.filters.require_debug_false]
   '()' = 'django.utils.log.RequireDebugFalse'

   [LOGGING.handlers.mail_admins]
   level = 'ERROR'
   filters = ['require_debug_false']
   class =  'django.utils.log.AdminEmailHandler'

   [LOGGING.handlers.file]
   level = 'INFO'
   class = 'logging.handlers.WatchedFileHandler'
   filename =  'logs/mailmansuite.log'
   formatter = 'verbose'

   [LOGGING.loggers."django.request"]
   handlers = ['mail_admins', 'file']
   level = 'ERROR'
   propagate = true

   [LOGGING.formatters.verbose]
   format = '%(levelname)s %(asctime)s %(process)d %(name)s %(message)s'


Gotchas
=======

- Please make sure that you have writtena valid Toml, you can use 
  `TOML Validator <https://github.com/BurntSushi/toml/tree/master/cmd/tomlv>`_ or 
  `tomlcheck <https://github.com/vmchale/tomlcheck>`_ tools to 
  validate the toml file.

- Please make sure that all smiple ``KEY = value`` pairs are in the
  root namespace (above any ``[section]``) so that they don't get 
  swallowed under one of the maps or arrays. Previously, we have
  seen ``ImproperlyConfiguredError`` for missing keys that were
  actually defined in the toml file.

LICENSE
=======

The contents of this project is licensed under Apache License 2.0. Please see
the LICENSE file for a complete copy of license text.
