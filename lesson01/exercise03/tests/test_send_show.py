# -*- coding: utf-8 -*-
# !/usr/bin/env python3

from exercise03 import send_show
import pytest
import yaml

def parse_input_file():
    with open('tests/test_devices.yml', 'r') as file:
       devices = yaml.safe_load(file)
       return [(group, device) for group, list_ in devices.items() for device in list_]

@pytest.fixture(params=parse_input_file())
def get_device(request):
    yield request.param

def test_type_return_result(get_device):
    group, device = get_device
    print(f'\t-> {device["host"]}')
    match group:
        case 'reachable_ssh_telnet':
            assert device['platform'] == 'cisco_iosxe'
        case 'reachable_ssh_telnet_wrong_auth_password':
            assert device['platform'] == 'test'
        case 'reachable_telnet_only':
            assert device['platform'] == 'test1'
        case 'unreachable':
            assert device['platform'] == 'cisco_iosxe'
