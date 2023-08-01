# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import pytest
import json
from pprint import pprint


@pytest.mark.parametrize("files", ["config_sw1.txt", "config_sw2.txt"])
def test_type_return_data(files):
    with open(files) as file:
        assert isinstance(get_int_vlan_map(file.read()), tuple) is True


@pytest.mark.parametrize("config, result", [("config_sw1.txt", "sw1_result.json"),
                                            ("config_sw2.txt", "sw2_result.json")])
def test_result_data(config, result):
    with open(config) as con, open(result) as res:
        access, trunk = json.load(res)
        assert get_int_vlan_map(con.read()) == (access, trunk)


def get_int_vlan_map(config_as_str):
    access_port_dict = {}
    trunk_port_dict = {}
    for line in config_as_str.splitlines():
        if line.startswith("interface") and "Ethernet" in line:
            current_interface = line.split()[-1]
            access_port_dict[current_interface] = 1
        elif "switchport access vlan" in line:
            access_port_dict[current_interface] = int(line.split()[-1])
        elif "switchport trunk allowed vlan" in line:
            vlans = [int(i) for i in line.split()[-1].split(",")]
            trunk_port_dict[current_interface] = vlans
            del access_port_dict[current_interface]
    return access_port_dict, trunk_port_dict


if __name__ == "__main__":
    with open("config_sw1.txt") as f:
        pprint(get_int_vlan_map(f.read()))
    with open("config_sw2.txt") as f:
        pprint(get_int_vlan_map(f.read()))
