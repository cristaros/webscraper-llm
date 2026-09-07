"""Default tests cannot open connections to production services."""

import ipaddress
import socket

import pytest


def _assert_local(address):
    if not isinstance(address, tuple):
        return  # Local Unix-domain sockets do not reach an external host.
    host = address[0]
    if host == "localhost":
        return
    try:
        if ipaddress.ip_address(host).is_loopback:
            return
    except ValueError:
        pass
    raise AssertionError("External network disabled: use fixtures or MockTransport")


@pytest.fixture(autouse=True)
def deny_external_network(monkeypatch, request):
    if request.node.get_closest_marker("live"):
        return
    original_connect = socket.socket.connect
    original_connect_ex = socket.socket.connect_ex
    original_create = socket.create_connection

    def connect(sock, address):
        _assert_local(address)
        return original_connect(sock, address)

    def connect_ex(sock, address):
        _assert_local(address)
        return original_connect_ex(sock, address)

    def create_connection(address, *args, **kwargs):
        _assert_local(address)
        return original_create(address, *args, **kwargs)

    monkeypatch.setattr(socket.socket, "connect", connect)
    monkeypatch.setattr(socket.socket, "connect_ex", connect_ex)
    monkeypatch.setattr(socket, "create_connection", create_connection)
