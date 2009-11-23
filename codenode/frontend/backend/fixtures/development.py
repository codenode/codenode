#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file has been automatically generated, changes may be lost if you
# go and generate it again. It was generated with the following command:
# ./manage.py dumpscript

import datetime
from decimal import Decimal
from django.contrib.contenttypes.models import ContentType

def run():
    from django.contrib.auth.models import Permission

    auth_permission_1 = Permission()
    auth_permission_1.name = u'Can add log entry'
    auth_permission_1.content_type = ContentType.objects.get(app_label="admin", model="logentry")
    auth_permission_1.codename = u'add_logentry'
    auth_permission_1.save()

    auth_permission_2 = Permission()
    auth_permission_2.name = u'Can change log entry'
    auth_permission_2.content_type = ContentType.objects.get(app_label="admin", model="logentry")
    auth_permission_2.codename = u'change_logentry'
    auth_permission_2.save()

    auth_permission_3 = Permission()
    auth_permission_3.name = u'Can delete log entry'
    auth_permission_3.content_type = ContentType.objects.get(app_label="admin", model="logentry")
    auth_permission_3.codename = u'delete_logentry'
    auth_permission_3.save()

    auth_permission_4 = Permission()
    auth_permission_4.name = u'Can add group'
    auth_permission_4.content_type = ContentType.objects.get(app_label="auth", model="group")
    auth_permission_4.codename = u'add_group'
    auth_permission_4.save()

    auth_permission_5 = Permission()
    auth_permission_5.name = u'Can add message'
    auth_permission_5.content_type = ContentType.objects.get(app_label="auth", model="message")
    auth_permission_5.codename = u'add_message'
    auth_permission_5.save()

    auth_permission_6 = Permission()
    auth_permission_6.name = u'Can add permission'
    auth_permission_6.content_type = ContentType.objects.get(app_label="auth", model="permission")
    auth_permission_6.codename = u'add_permission'
    auth_permission_6.save()

    auth_permission_7 = Permission()
    auth_permission_7.name = u'Can add user'
    auth_permission_7.content_type = ContentType.objects.get(app_label="auth", model="user")
    auth_permission_7.codename = u'add_user'
    auth_permission_7.save()

    auth_permission_8 = Permission()
    auth_permission_8.name = u'Can change group'
    auth_permission_8.content_type = ContentType.objects.get(app_label="auth", model="group")
    auth_permission_8.codename = u'change_group'
    auth_permission_8.save()

    auth_permission_9 = Permission()
    auth_permission_9.name = u'Can change message'
    auth_permission_9.content_type = ContentType.objects.get(app_label="auth", model="message")
    auth_permission_9.codename = u'change_message'
    auth_permission_9.save()

    auth_permission_10 = Permission()
    auth_permission_10.name = u'Can change permission'
    auth_permission_10.content_type = ContentType.objects.get(app_label="auth", model="permission")
    auth_permission_10.codename = u'change_permission'
    auth_permission_10.save()

    auth_permission_11 = Permission()
    auth_permission_11.name = u'Can change user'
    auth_permission_11.content_type = ContentType.objects.get(app_label="auth", model="user")
    auth_permission_11.codename = u'change_user'
    auth_permission_11.save()

    auth_permission_12 = Permission()
    auth_permission_12.name = u'Can delete group'
    auth_permission_12.content_type = ContentType.objects.get(app_label="auth", model="group")
    auth_permission_12.codename = u'delete_group'
    auth_permission_12.save()

    auth_permission_13 = Permission()
    auth_permission_13.name = u'Can delete message'
    auth_permission_13.content_type = ContentType.objects.get(app_label="auth", model="message")
    auth_permission_13.codename = u'delete_message'
    auth_permission_13.save()

    auth_permission_14 = Permission()
    auth_permission_14.name = u'Can delete permission'
    auth_permission_14.content_type = ContentType.objects.get(app_label="auth", model="permission")
    auth_permission_14.codename = u'delete_permission'
    auth_permission_14.save()

    auth_permission_15 = Permission()
    auth_permission_15.name = u'Can delete user'
    auth_permission_15.content_type = ContentType.objects.get(app_label="auth", model="user")
    auth_permission_15.codename = u'delete_user'
    auth_permission_15.save()

    auth_permission_16 = Permission()
    auth_permission_16.name = u'Can add backend server'
    auth_permission_16.content_type = ContentType.objects.get(app_label="backend", model="backendserver")
    auth_permission_16.codename = u'add_backendserver'
    auth_permission_16.save()

    auth_permission_17 = Permission()
    auth_permission_17.name = u'Can add engine type'
    auth_permission_17.content_type = ContentType.objects.get(app_label="backend", model="enginetype")
    auth_permission_17.codename = u'add_enginetype'
    auth_permission_17.save()

    auth_permission_18 = Permission()
    auth_permission_18.name = u'Can add notebook backend record'
    auth_permission_18.content_type = ContentType.objects.get(app_label="backend", model="notebookbackendrecord")
    auth_permission_18.codename = u'add_notebookbackendrecord'
    auth_permission_18.save()

    auth_permission_19 = Permission()
    auth_permission_19.name = u'Can change backend server'
    auth_permission_19.content_type = ContentType.objects.get(app_label="backend", model="backendserver")
    auth_permission_19.codename = u'change_backendserver'
    auth_permission_19.save()

    auth_permission_20 = Permission()
    auth_permission_20.name = u'Can change engine type'
    auth_permission_20.content_type = ContentType.objects.get(app_label="backend", model="enginetype")
    auth_permission_20.codename = u'change_enginetype'
    auth_permission_20.save()

    auth_permission_21 = Permission()
    auth_permission_21.name = u'Can change notebook backend record'
    auth_permission_21.content_type = ContentType.objects.get(app_label="backend", model="notebookbackendrecord")
    auth_permission_21.codename = u'change_notebookbackendrecord'
    auth_permission_21.save()

    auth_permission_22 = Permission()
    auth_permission_22.name = u'Can delete backend server'
    auth_permission_22.content_type = ContentType.objects.get(app_label="backend", model="backendserver")
    auth_permission_22.codename = u'delete_backendserver'
    auth_permission_22.save()

    auth_permission_23 = Permission()
    auth_permission_23.name = u'Can delete engine type'
    auth_permission_23.content_type = ContentType.objects.get(app_label="backend", model="enginetype")
    auth_permission_23.codename = u'delete_enginetype'
    auth_permission_23.save()

    auth_permission_24 = Permission()
    auth_permission_24.name = u'Can delete notebook backend record'
    auth_permission_24.content_type = ContentType.objects.get(app_label="backend", model="notebookbackendrecord")
    auth_permission_24.codename = u'delete_notebookbackendrecord'
    auth_permission_24.save()

    auth_permission_25 = Permission()
    auth_permission_25.name = u'Can add Bookshelf Folder'
    auth_permission_25.content_type = ContentType.objects.get(app_label="bookshelf", model="folder")
    auth_permission_25.codename = u'add_folder'
    auth_permission_25.save()

    auth_permission_26 = Permission()
    auth_permission_26.name = u'Can change Bookshelf Folder'
    auth_permission_26.content_type = ContentType.objects.get(app_label="bookshelf", model="folder")
    auth_permission_26.codename = u'change_folder'
    auth_permission_26.save()

    auth_permission_27 = Permission()
    auth_permission_27.name = u'Can delete Bookshelf Folder'
    auth_permission_27.content_type = ContentType.objects.get(app_label="bookshelf", model="folder")
    auth_permission_27.codename = u'delete_folder'
    auth_permission_27.save()

    auth_permission_28 = Permission()
    auth_permission_28.name = u'Can add content type'
    auth_permission_28.content_type = ContentType.objects.get(app_label="contenttypes", model="contenttype")
    auth_permission_28.codename = u'add_contenttype'
    auth_permission_28.save()

    auth_permission_29 = Permission()
    auth_permission_29.name = u'Can change content type'
    auth_permission_29.content_type = ContentType.objects.get(app_label="contenttypes", model="contenttype")
    auth_permission_29.codename = u'change_contenttype'
    auth_permission_29.save()

    auth_permission_30 = Permission()
    auth_permission_30.name = u'Can delete content type'
    auth_permission_30.content_type = ContentType.objects.get(app_label="contenttypes", model="contenttype")
    auth_permission_30.codename = u'delete_contenttype'
    auth_permission_30.save()

    auth_permission_31 = Permission()
    auth_permission_31.name = u'Can add Cell'
    auth_permission_31.content_type = ContentType.objects.get(app_label="notebook", model="cell")
    auth_permission_31.codename = u'add_cell'
    auth_permission_31.save()

    auth_permission_32 = Permission()
    auth_permission_32.name = u'Can add cell audit'
    auth_permission_32.content_type = ContentType.objects.get(app_label="notebook", model="cellaudit")
    auth_permission_32.codename = u'add_cellaudit'
    auth_permission_32.save()

    auth_permission_33 = Permission()
    auth_permission_33.name = u'Can add Notebook'
    auth_permission_33.content_type = ContentType.objects.get(app_label="notebook", model="notebook")
    auth_permission_33.codename = u'add_notebook'
    auth_permission_33.save()

    auth_permission_34 = Permission()
    auth_permission_34.name = u'Can add notebook audit'
    auth_permission_34.content_type = ContentType.objects.get(app_label="notebook", model="notebookaudit")
    auth_permission_34.codename = u'add_notebookaudit'
    auth_permission_34.save()

    auth_permission_35 = Permission()
    auth_permission_35.name = u'Can change Cell'
    auth_permission_35.content_type = ContentType.objects.get(app_label="notebook", model="cell")
    auth_permission_35.codename = u'change_cell'
    auth_permission_35.save()

    auth_permission_36 = Permission()
    auth_permission_36.name = u'Can change cell audit'
    auth_permission_36.content_type = ContentType.objects.get(app_label="notebook", model="cellaudit")
    auth_permission_36.codename = u'change_cellaudit'
    auth_permission_36.save()

    auth_permission_37 = Permission()
    auth_permission_37.name = u'Can change Notebook'
    auth_permission_37.content_type = ContentType.objects.get(app_label="notebook", model="notebook")
    auth_permission_37.codename = u'change_notebook'
    auth_permission_37.save()

    auth_permission_38 = Permission()
    auth_permission_38.name = u'Can change notebook audit'
    auth_permission_38.content_type = ContentType.objects.get(app_label="notebook", model="notebookaudit")
    auth_permission_38.codename = u'change_notebookaudit'
    auth_permission_38.save()

    auth_permission_39 = Permission()
    auth_permission_39.name = u'Can delete Cell'
    auth_permission_39.content_type = ContentType.objects.get(app_label="notebook", model="cell")
    auth_permission_39.codename = u'delete_cell'
    auth_permission_39.save()

    auth_permission_40 = Permission()
    auth_permission_40.name = u'Can delete cell audit'
    auth_permission_40.content_type = ContentType.objects.get(app_label="notebook", model="cellaudit")
    auth_permission_40.codename = u'delete_cellaudit'
    auth_permission_40.save()

    auth_permission_41 = Permission()
    auth_permission_41.name = u'Can delete Notebook'
    auth_permission_41.content_type = ContentType.objects.get(app_label="notebook", model="notebook")
    auth_permission_41.codename = u'delete_notebook'
    auth_permission_41.save()

    auth_permission_42 = Permission()
    auth_permission_42.name = u'Can delete notebook audit'
    auth_permission_42.content_type = ContentType.objects.get(app_label="notebook", model="notebookaudit")
    auth_permission_42.codename = u'delete_notebookaudit'
    auth_permission_42.save()

    auth_permission_43 = Permission()
    auth_permission_43.name = u'Can add registration profile'
    auth_permission_43.content_type = ContentType.objects.get(app_label="registration", model="registrationprofile")
    auth_permission_43.codename = u'add_registrationprofile'
    auth_permission_43.save()

    auth_permission_44 = Permission()
    auth_permission_44.name = u'Can change registration profile'
    auth_permission_44.content_type = ContentType.objects.get(app_label="registration", model="registrationprofile")
    auth_permission_44.codename = u'change_registrationprofile'
    auth_permission_44.save()

    auth_permission_45 = Permission()
    auth_permission_45.name = u'Can delete registration profile'
    auth_permission_45.content_type = ContentType.objects.get(app_label="registration", model="registrationprofile")
    auth_permission_45.codename = u'delete_registrationprofile'
    auth_permission_45.save()

    auth_permission_46 = Permission()
    auth_permission_46.name = u'Can add session'
    auth_permission_46.content_type = ContentType.objects.get(app_label="sessions", model="session")
    auth_permission_46.codename = u'add_session'
    auth_permission_46.save()

    auth_permission_47 = Permission()
    auth_permission_47.name = u'Can change session'
    auth_permission_47.content_type = ContentType.objects.get(app_label="sessions", model="session")
    auth_permission_47.codename = u'change_session'
    auth_permission_47.save()

    auth_permission_48 = Permission()
    auth_permission_48.name = u'Can delete session'
    auth_permission_48.content_type = ContentType.objects.get(app_label="sessions", model="session")
    auth_permission_48.codename = u'delete_session'
    auth_permission_48.save()

    auth_permission_49 = Permission()
    auth_permission_49.name = u'Can add site'
    auth_permission_49.content_type = ContentType.objects.get(app_label="sites", model="site")
    auth_permission_49.codename = u'add_site'
    auth_permission_49.save()

    auth_permission_50 = Permission()
    auth_permission_50.name = u'Can change site'
    auth_permission_50.content_type = ContentType.objects.get(app_label="sites", model="site")
    auth_permission_50.codename = u'change_site'
    auth_permission_50.save()

    auth_permission_51 = Permission()
    auth_permission_51.name = u'Can delete site'
    auth_permission_51.content_type = ContentType.objects.get(app_label="sites", model="site")
    auth_permission_51.codename = u'delete_site'
    auth_permission_51.save()

    auth_permission_52 = Permission()
    auth_permission_52.name = u'Can add user settings'
    auth_permission_52.content_type = ContentType.objects.get(app_label="usersettings", model="usersettings")
    auth_permission_52.codename = u'add_usersettings'
    auth_permission_52.save()

    auth_permission_53 = Permission()
    auth_permission_53.name = u'Can change user settings'
    auth_permission_53.content_type = ContentType.objects.get(app_label="usersettings", model="usersettings")
    auth_permission_53.codename = u'change_usersettings'
    auth_permission_53.save()

    auth_permission_54 = Permission()
    auth_permission_54.name = u'Can delete user settings'
    auth_permission_54.content_type = ContentType.objects.get(app_label="usersettings", model="usersettings")
    auth_permission_54.codename = u'delete_usersettings'
    auth_permission_54.save()

    from django.contrib.auth.models import Group


    from django.contrib.auth.models import User

    auth_user_1 = User()
    auth_user_1.username = u'admin'
    auth_user_1.first_name = u''
    auth_user_1.last_name = u''
    auth_user_1.email = u'admin@example.com'
    auth_user_1.password = u'sha1$5dbb9$8ba5bd30d0826b8eae5cbf76ae88b19f934aeca1'
    auth_user_1.is_staff = True
    auth_user_1.is_active = True
    auth_user_1.is_superuser = True
    auth_user_1.last_login = datetime.datetime(2009, 10, 17, 8, 56, 0, 458130)
    auth_user_1.date_joined = datetime.datetime(2009, 10, 17, 8, 54, 47, 894137)
    auth_user_1.save()

    from django.contrib.auth.models import Message


    from django.contrib.sessions.models import Session

    django_session_1 = Session()
    django_session_1.session_key = u'5fce245e1961fd38e693ce67df6da6d8'
    django_session_1.session_data = u'gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwF1LjcyMDFjMTJlMGMzYzM3YzMzYzE3\nMDFlMzUzOTgwNWMw\n'
    django_session_1.expire_date = datetime.datetime(2009, 10, 31, 8, 56, 0, 488306)
    django_session_1.save()

    from django.contrib.sites.models import Site

    django_site_1 = Site()
    django_site_1.domain = u'example.com'
    django_site_1.name = u'example.com'
    django_site_1.save()

    from django.contrib.admin.models import LogEntry

    django_admin_log_1 = LogEntry()
    django_admin_log_1.action_time = datetime.datetime(2009, 10, 17, 8, 56, 27, 639334)
    django_admin_log_1.user = auth_user_1
    django_admin_log_1.content_type = ContentType.objects.get(app_label="backend", model="backendserver")
    django_admin_log_1.object_id = u'1'
    django_admin_log_1.object_repr = u'Backend Server local @ http://localhost:8337'
    django_admin_log_1.action_flag = 1
    django_admin_log_1.change_message = u''
    django_admin_log_1.save()

    from codenode.frontend.registration.models import RegistrationProfile


    from codenode.frontend.notebook.models import NotebookAudit


    from codenode.frontend.notebook.models import Notebook


    from codenode.frontend.notebook.models import CellAudit


    from codenode.frontend.notebook.models import Cell


    from codenode.frontend.backend.models import BackendServer

    backend_backendserver_1 = BackendServer()
    backend_backendserver_1.name = u'local'
    backend_backendserver_1.address = u'http://localhost:8337'
    backend_backendserver_1.save()

    from codenode.frontend.backend.models import EngineType

    backend_enginetype_1 = EngineType()
    backend_enginetype_1.name = u'Python'
    backend_enginetype_1.backend = backend_backendserver_1
    backend_enginetype_1.description = None
    backend_enginetype_1.save()

    from codenode.frontend.backend.models import NotebookBackendRecord


    from codenode.frontend.usersettings.models import UserSettings


    from codenode.frontend.bookshelf.models import Folder


