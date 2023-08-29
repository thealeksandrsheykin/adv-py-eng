# Advanced Python для сетевых инженеров

## Lesson №1

### *Task 1*

Написать тест или тесты для функции `get_int_vlan_map`. Тест должен проверять:

* тип возвращаемых данных
* что словари, которые возвращает функция, содержат правильные данные

Проверить работу функции с разными входящими данными и убедиться, что словари генерируются правильно 
для этих данных. Пример вызова функции показан в файле заданий. Тест(ы) написать в файле заданий.
Ограничение: функцию менять нельзя.

```python

from pprint import pprint


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
```

### *Task 2*

Написать тесты для класса Network. Тесты должны проверять:

1. переменные экземпляров network и addresses:
   * наличие переменной экземпляра
   * правильное значение

2. метод __iter__:
   * метод есть
   * возвращает итератор
   * при итерации возвращаются IP-адреса и правильные IP-адреса (достаточно проверить 2 адреса)

3. метод __len__:
   * проверка количества IP-адресов

4. метод __getitem__:
   * проверить обращение по положительному, отрицательному индексу
   * проверить, что при обращении к не существующему индексу, генерируется исключение IndexError

Тесты написать в файле заданий. Разделить на тесты по своему усмотрению. Ограничение: класс менять нельзя.

```python
import ipaddress


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

```

### *Task 3*

Написать тесты для функции `send_show`. Тесты должны проверять:

* тип возвращаемых данных - словарь или None, если было исключение
* при возникновении исключения, опционально можно сделать проверку на то правильное ли выводится сообщение на stdout, 
  как минимум, что в stdout был вывод IP-адреса
* что функция возвращает правильный результат при передаче команды строки и при передаче списка команд. 
  И в том и в том случае должен возвращаться словарь в котором ключ команда, а значение вывод команды

Для проверки разных ситуаций - доступное устройство, недоступное и так далее в файле `devices.yaml` создано несколько
групп устройств:
* `reachable_ssh_telnet` - это устройства на которых доступен Telnet и SSH, прописаны правильные логин и пароли
* `reachable_ssh_telnet_wrong_auth_password` - это доступное устройство на котором разрешены SSH/Telnet, но настроен
   неправильный пароль auth_password
* `reachable_telnet_only` - это доступное устройство на котором разрешен только Telnet и прописаны правильные логин и пароли
* `unreachable` - это недоступное устройство

Для корректной работы тестов надо написать в файле `devices.yaml` параметры ваших устройств или создать аналогичный файл
с другим именем. Плюс надо соответственно настроить устройства так, чтобы где нужно был только Telnet или неправильный 
пароль соответственно.

Ограничение: функцию менять нельзя.

```python
from pprint import pprint

import yaml
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
            pprint(output, width=120)

```

### *Task 4*

Написать тесты для класса `CiscoTelnet`. Тесты должны проверять:
1. Cоздание подключения `telnet` при создании экземпляра. Один из признаков тут - отсутствие исключений при создании экземлпяра.
   Также можно проверить значение `self.prompt`.
2. Проверка параметра secret в методе `__init__` - при значении по умолчанию `None` (пароль не указывается), надо 
   проверить, что подключение выполнилось без исключений и `self.prompt` равен `#` или `>`. Проверить лучше оба значения, так как на
   оборудовании может быть настроен `privilege`. Если указан правильный пароль `secret`, проверить что получается без ошибок 
   выполнить команды `sh clock и sh run | i hostname`. Плюс `self.prompt` должен быть равен `#`;
3. работу метода send_show_command;
4. проверить работу экземпляра в менеджере контекста;
5. приватные методы и переменные мы не проверяем потому что они могут меняться, так как это не public API класса и лучше
   в тестах не привязываться к ним.

В целом тут свобода творчества и один из нюансов задания как раз в том чтобы придумать что именно и как тестировать. В 
задании даны несколько идей для старта, но остальное надо продумать самостоятельно.
Тут аналогично с заданием №3 можно создать отдельный файл с устройствами. В отличии от задания №3, в этом задании при 
подключении к оборудованию могут генерироваться исключения, если что-то пошло не так.
Тест должен проверять, что исключения генерируются и какие именно исключения. Тест(ы) написать в файле заданий.
Ограничение: класс менять нельзя.
