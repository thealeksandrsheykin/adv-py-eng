# -*- coding: utf-8 -*-
# !/usr/bin/env python3

from exercise03 import send_show
import random
import pytest

@pytest.fixture
def values():
    return [random.randint(0, 100) for _ in range(10)]


@pytest.fixture
def value(request):
    return request.param


@pytest.mark.parametrize("value", params=values)
def test_function(value):
    assert value > 0
