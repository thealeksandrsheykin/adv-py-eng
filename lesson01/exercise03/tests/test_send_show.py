# -*- coding: utf-8 -*-
# !/usr/bin/env python3

from exercise03 import send_show
import pytest
import yaml
from functools import wraps
from scrapli import Scrapli


def print_device_information(func: callable) -> callable:
    @wraps(func)
    def inner(*args, **kwargs) -> any:
        result = func(*args, **kwargs)
        group, device = kwargs.get('get_device')
        print(f' <- {device["host"]} Group: {group.upper()} Transport: {device["transport"]}')
        return result

    return inner


@pytest.fixture()
def result_reach_ssh_telnet_str():
    return {'sh clock': '*19:56:24.339 MSK Wed Aug 9 2023'}


def parse_input_file():
    with open('tests/test_devices.yml', 'r') as file:
        devices = yaml.safe_load(file)
        return [(group, device) for group, list_ in devices.items() for device in list_]


@pytest.fixture(params=parse_input_file())
def get_device(request):
    yield request.param


@print_device_information
def test_type_return_result(capsys, get_device):
    group, device = get_device
    result = send_show(device, 'show clock')
    captured = capsys.readouterr()
    match group, device['transport']:
        case 'reachable_ssh_telnet', 'paramiko' | 'telnet':
            assert isinstance(result, dict)
        case 'reachable_telnet_only', 'telnet':
            assert isinstance(result, dict)
        case _:
            assert result is None


@print_device_information
def test_correct_message_stdout(capsys, get_device):
    group, device = get_device
    send_show(device, 'show clock')
    captured = capsys.readouterr()
    if f'<<< Received output from {device["host"]}' not in captured.out:
        assert f'Device {device["host"]}, Transport {device["transport"]}, Error' in captured.out


@print_device_information
def test_send_config_commands_list(capsys, get_device):
    group, device = get_device
    commands = ['show ip int brief', 'show log']
    result = send_show(device, commands)
    captured = capsys.readouterr()
    if group == 'reachable_ssh_telnet' or (group == 'reachable_telnet_only' and device['transport'] == 'telnet'):
        with Scrapli(**device) as ssh:
            for cmd in commands:
                assert result[cmd] == ssh.send_command(cmd).result


@print_device_information
def test_send_config_command_str(capsys, get_device):
    group, device = get_device
    command = 'show log'
    result = send_show(device, command)
    captured = capsys.readouterr()
    if group == 'reachable_ssh_telnet' or (group == 'reachable_telnet_only' and device['transport'] == 'telnet'):
        with Scrapli(**device) as ssh:
            assert result[command] == ssh.send_command(command).result
