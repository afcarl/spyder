# -*- coding: utf-8 -*-
# Copyright © QCrash - Colin Duquesnoy
# Copyright © Spyder Project Contributors
# Licensed under the terms of the MIT License
# (see spyder/__init__.py for details)

"""
Tests for the Github backend

Taken from the QCrash Project:
https://github.com/ColinDuquesnoy/QCrash
"""

import os
import sys

import pytest

from spyder.config.main import CONF
from spyder.widgets.github import backend


USERNAME = 'tester'
PASSWORD = 'test1234'
GH_OWNER = 'ccordoba12'
GH_REPO = 'spyder'


def get_backend():
    b = backend.GithubBackend(GH_OWNER, GH_REPO)
    b._show_msgbox = False
    return b


def get_backend_bad_repo():
    b = backend.GithubBackend(GH_OWNER, GH_REPO + '1234')
    b._show_msgbox = False
    return b


def get_wrong_user_credentials():
    """
    Monkeypatch GithubBackend.get_user_credentials to force the case where
    invalid credentias were provided
    """
    return dict(username='invalid',
                password='invalid',
                token='invalid',
                remember=False,
                remember_token=False)


def get_empty_user_credentials():
    """
    Monkeypatch GithubBackend.get_user_credentials to force the case where
    invalid credentias were provided
    """
    return dict(username='',
                password='',
                token='',
                remember=False,
                remember_token=False)


def get_fake_user_credentials():
    """
    Monkeypatch GithubBackend.get_user_credentials to force the case where
    invalid credentias were provided
    """
    return dict(username=USERNAME,
                password=PASSWORD,
                token='',
                remember=False,
                remember_token=False)


def test_invalid_credentials():
    b = get_backend()
    b.get_user_credentials = get_wrong_user_credentials
    ret_value = b.send_report('Wrong credentials', 'Wrong credentials')
    assert ret_value is False


def test_empty_credentials():
    b = get_backend()
    b.get_user_credentials = get_empty_user_credentials
    ret_value = b.send_report('Empty credentials', 'Wrong credentials')
    assert ret_value is False


def test_fake_credentials_bad_repo():
    b = get_backend_bad_repo()
    b.get_user_credentials = get_fake_user_credentials
    ret_value = b.send_report('Test suite', 'Test fake credentials')
    assert ret_value is False


def test_get_credentials_from_settings():
    b = get_backend()
    username, remember_me, remember_token = b._get_credentials_from_settings()
    assert username == ''
    assert remember_me is False
    assert remember_token is False

    CONF.set('main', 'report_error/username', 'user')
    CONF.set('main', 'report_error/remember_me', True)
    CONF.set('main', 'report_error/remember_token', True)

    username, remember_me, remember_token = b._get_credentials_from_settings()
    assert username == 'user'
    assert remember_me is True
    assert remember_token is True


@pytest.mark.skipif((os.environ.get('CI', None) is not None and
                     sys.platform.startswith('linux')),
                    reason="Hard to make it work in our CIs and Linux")
def test_store_user_credentials():
    b = get_backend()
    b._store_credentials('user', 'toto', True)
    credentials = b.get_user_credentials()

    assert credentials['username'] == 'user'
    assert credentials['password'] == 'toto'
    assert credentials['remember'] is True
