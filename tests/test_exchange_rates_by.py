#!/usr/bin/env python

"""Tests for `exchange_rates_by` package."""

from exchange_rates_by import MyfinClient
import pytest


# from exchange_rates_by import exchange_rates_by


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string

def test_myfin():
    assert 2+2 == 4