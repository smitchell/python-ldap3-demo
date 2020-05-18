#!/usr/bin/env python3
from collections import OrderedDict
from ldap3 import Server, Connection
from ldap3.utils.dn import escape_rdn


class ConnectionManager:
    mocked = 'mocked'
    connection_default_config: dict = {}
    server_default_config: dict = {}
    servers: dict = {}
    connection_configs: dict = {}

    def __init__(self, config: OrderedDict):
        self.connection_default_config = config['connection_default_config']
        self.server_default_config = config['server_default_config']

        for server_name in config['servers'].keys():
            server_name_config = config['servers'][server_name]
            self._add_connection_config(server_name, server_name_config['connection_config'])
            self.add_server(server_name, server_name_config['server_config'])

    def get_connection(self, server_name: str, params: dict = None) -> Connection:

        merged_config = self.connection_configs[server_name]

        if params is not None and len(params.keys()) > 0:
            connection_config = params
        else:
            connection_config = {}

        for key in merged_config:
            if key in connection_config:
                continue
            connection_config[key] = merged_config[key]

        if server_name == self.mocked:
            return Connection(self.servers[self.mocked],
                          user=escape_rdn(connection_config['user']),
                          password=connection_config['password'],
                          client_strategy=connection_config['client_strategy'])

        return Connection(self.servers[server_name],
                          user=escape_rdn(connection_config['user']),
                          password=connection_config['password'],
                          client_strategy=connection_config['client_strategy'],
                          auto_bind=connection_config['auto_bind'],
                          version=connection_config['version'],
                          authentication=connection_config['authentication'],
                          auto_referrals=connection_config['auto_referrals'],
                          collect_usage=connection_config['collect_usage'],
                          read_only=connection_config['read_only'],
                          lazy=connection_config['lazy'],
                          check_names=connection_config['check_names'],
                          raise_exceptions=connection_config['raise_exceptions'],
                          fast_decoder=connection_config['fast_decoder'],
                          receive_timeout=connection_config['receive_timeout'],
                          return_empty_attributes=connection_config['return_empty_attributes'],
                          auto_range=connection_config['auto_range'],
                          auto_escape=connection_config['auto_escape'],
                          auto_encode=connection_config['auto_encode']
                          )

    def add_server(self, server_name: str, config: OrderedDict):
        if server_name == self.mocked:
            self.servers[self.mocked] = Server(self.mocked)
        else:
            server_config = {}
            for key in config.keys():
                server_config[key] = config[key]
            # Only pull in the default value if it is missing.
            for key in self.server_default_config.keys():
                if key not in server_config.keys():
                    server_config[key] = self.server_default_config[key]
            self.servers[server_name] = self._server_factory(server_config)

    def _add_connection_config(self, server_name: str, config: OrderedDict):
        connection_config = {}
        for key in config.keys():
            connection_config[key] = config[key]
            # Only pull in the default value if it is missing.
        if server_name != 'mocked':
            for key in self.connection_default_config.keys():
                if key not in connection_config.keys():
                    connection_config[key] = self.connection_default_config[key]

        self.connection_configs[server_name] = connection_config

    @staticmethod
    def _server_factory(config: dict) -> Server:
        return Server(
            config['ldap_host'],
            port=config['ldap_port'],
            use_ssl=config['use_ssl'],
            allowed_referral_hosts=config['allowed_referral_hosts'],
            get_info=config['get_info'],
            mode=config['mode'],
            tls=config['tls'],
            formatter=config['formatter'],
            connect_timeout=config['connect_timeout'])
