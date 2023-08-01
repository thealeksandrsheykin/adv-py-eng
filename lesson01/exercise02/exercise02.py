# -*- coding: utf-8 -*-
# !/usr/bin/env python3
import inspect

import pytest
import ipaddress
import collections


@pytest.fixture
def create_instance_class():
    return Network("10.1.1.192/30")


@pytest.mark.parametrize("attribute, result", [("network", "10.1.1.192/30"),
                                               ("addresses", ("10.1.1.193", "10.1.1.194"))])
def test_var_class(create_instance_class, attribute, result):
    assert getattr(create_instance_class, attribute) == result


@pytest.mark.parametrize("method", [("__iter__"),
                                    ("__len__"),
                                    ("__getitem__")])
def test_check_exist_method(create_instance_class, method):
    assert getattr(create_instance_class, method, None) is not None


def test_check_method_iter(create_instance_class):
    assert isinstance(create_instance_class.__iter__(), collections.Iterable) == True
    address = create_instance_class.__iter__()
    assert next(address) == '10.1.1.193'
    assert next(address) == '10.1.1.194'


def test_check_method_len(create_instance_class):
    assert len(create_instance_class) == 2


@pytest.mark.parametrize("index, result", [(1, "10.1.1.194"),
                                           (-1, "10.1.1.194")])
def test_check_method_getitem(create_instance_class, index, result):
    assert create_instance_class[index] == result


def test_check_method_getitem_error(create_instance_class):
    with pytest.raises(IndexError):
        create_instance_class[len(create_instance_class)]


class Network:
    def __init__(self, network):
        self.network = network
        subnet = ipaddress.ip_network(self.network)
        self.addresses = tuple([str(ip) for ip in subnet.hosts()])

    def __iter__(self):
        return iter(self.addresses)

    def __len__(self):
        return len(self.addresses)

    def __getitem__(self, index):
        return self.addresses[index]


if __name__ == "__main__":
    # пример создания экземпляра
    net1 = Network('10.1.1.192/30')
