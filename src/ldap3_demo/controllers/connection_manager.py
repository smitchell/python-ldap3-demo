#!/usr/bin/env python3
import logging
from ldap3 import Server, Connection
from flask import current_app
from ldap3_demo.app import app


class ConnectionManager:
    servers: dict = {}
    ldap_configs: dict = {}

    def __init__(self):
        with app.app_context():
            self.logger = current_app.logger
            self.ldap_configs = app.config['ldap_servers']
        for server_name in self.ldap_configs.keys():
            ldap_config = self.ldap_configs[server_name]
            self.servers[server_name] = Server(ldap_config['ldap_host'], **ldap_config['server_config'])

    def get_connection(self, server_name: str, params: dict = None):
        if server_name not in self.ldap_configs:
            self.logger.warning(f'Server name {server_name} not found in the LDAP configuration')
            return None
        ldap_config = self.ldap_configs[server_name]['connection_config']
        if params is None or len(params) == 0:
            connection_config = ldap_config
        else:
            connection_config = params
            for key in ldap_config:
                if key not in connection_config:
                    connection_config[key] = ldap_config[key]
        conn: Connection = Connection(self.servers[server_name], **connection_config)
        return conn
