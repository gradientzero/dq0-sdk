# -*- coding: utf-8 -*-
import pytest


@pytest.fixture(scope='session')
def fixtures(pytestconfig):
    my_global_test_variable = 'Test'
    return locals()


def test_dummy_with_fixtures(fixtures):
    var = fixtures['my_global_test_variable']
    assert var == 'Test'


def test_dummy_capsys(capsys):
    assert True


@pytest.mark.slow
def test_slow(capsys):
    # run slow marked tests with 'python -m pytest -m slow'
    assert True
