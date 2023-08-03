# -*- coding: utf-8 -*-
# !/usr/bin/env python3

from pprint import pprint

import yaml
import socket
from scrapli import Scrapli
from scrapli.exceptions import ScrapliException
from paramiko.ssh_exception import SSHException


def send_show(device, show_commands):
    transport = device.get("transport") or "system"
    host = device.get("host")
    if type(show_commands) == str:
        show_commands = [show_commands]
    cmd_dict = {}
    print(f">>> Connecting to {host}")
    try:
        with Scrapli(**device) as ssh:
            for cmd in show_commands:
                reply = ssh.send_command(cmd)
                cmd_dict[cmd] = reply.result
        print(f"<<< Received output from {host}")
        return cmd_dict
    except (ScrapliException, SSHException, socket.timeout, OSError) as error:
        print(f"Device {host}, Transport {transport}, Error {error}")


if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    for dev_type, device_list in devices.items():
        print(dev_type.upper())
        for dev in device_list:
            output = send_show(dev, "sh clock")
            print(output)
            pprint(output, width=120)