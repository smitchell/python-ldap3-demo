from collections import OrderedDict

from ldap3 import Server, Connection

from ldap3_demo.controllers.connection_manager import ConnectionManager

data: OrderedDict = OrderedDict(
    [('connection_default_config', OrderedDict(
        [('auto_bind', 'AUTO_BIND_NONE'),
         ('version', 3),
         ('authentication', 'AUTH_SIMPLE'),
         ('client_strategy', 'REUSABLE'),
         ('auto_referrals', True),
         ('sasl_mechanism', None),
         ('sasl_credential', None),
         ('collect_usage', True),
         ('read_only', False),
         ('lazy', True),
         ('check_names', True),
         ('raise_exceptions', False),
         ('pool_active', True),
         ('poop_exhust', True),
         ('pool_strategy', 'ROUND_ROBIN'),
         ('pool_name', 'default'),
         ('pool_size', 5),
         ('pool_lifetime', 120),
         ('pool_keepalive', 0),
         ('fast_decoder', True),
         ('receive_timeout', 20),
         ('return_empty_attributes', True),
         ('auto_range', True),
         ('use_referral_cache', True),
         ('auto_escape', True),
         ('auto_encode', True)
        ])),
     ('server_default_config', OrderedDict(
        [('ldap_port', 389),
         ('use_ssl', False),
         ('allowed_referral_hosts', None),
         ('get_info', 'SCHEMA'),
         ('mode', 'IP_SYSTEM_DEFAULT'),
         ('tls', None),
         ('formatter', None),
         ('connect_timeout', 20)
        ])),
     ('servers', OrderedDict(
         [('local', OrderedDict(
             [('server_config', OrderedDict(
                 [('ldap_host', '192.168.1.5')])),
              ('connection_config', OrderedDict(
                [('user', 'admin'),
                 ('password', 'abadpassword'),
                 ('pool_name', 'local'),
                 ('pool_size', 1)
                ]))
             ])),
          ('mocked', OrderedDict(
              [('server_config', {}),
               ('connection_config', OrderedDict(
                  [('user', 'admin'),
                   ('password', 'abadpassword'),
                   ('client_strategy', 'MOCK_SYNC')
                   ]))
               ]))
          ]))
     ])

connection_manager = ConnectionManager(data)


def test_init_connection_manager_server_defaults():
    assert connection_manager.server_default_config is not None, 'Expected server_default_config but found none'
    print(connection_manager.server_default_config )
    expected = connection_manager.server_default_config['ldap_port']
    actual = 389
    assert actual == expected, f'Expected {expected} but found {actual}'

    expected = connection_manager.server_default_config['use_ssl']
    actual = False
    assert actual == expected, f'Expected {expected} but found {actual}'

    expected = connection_manager.server_default_config['allowed_referral_hosts']
    actual = None
    assert actual == expected, f'Expected {expected} but found {actual}'


def test_init_connection_manager_connection_defaults():
    assert connection_manager.connection_default_config is not None, 'Expected server_default_config but found none'
    print(connection_manager.connection_default_config )

    expected = connection_manager.connection_default_config['auto_bind']
    actual = 'AUTO_BIND_NONE'
    assert actual == expected, f'Expected {expected} but found {actual}'

    expected = connection_manager.connection_default_config['authentication']
    actual = 'AUTH_SIMPLE'
    assert actual == expected, f'Expected {expected} but found {actual}'

    expected = connection_manager.connection_default_config['client_strategy']
    actual = 'REUSABLE'
    assert actual == expected, f'Expected {expected} but found {actual}'


def test_init_connection_manager_local_server():
    local_server: Server = connection_manager.servers['local']
    assert local_server is not None, 'Expected to find "local" server, but found none'
    assert local_server.connect_timeout == 20


def test_init_connection_manager_mocked_server():
    mock_server: Server = connection_manager.servers[connection_manager.mocked]
    assert mock_server is not None, 'Expected to find "mocked" server, but found none'


def test_server_connection_config():
    config = connection_manager.connection_configs['local']
    assert config is not None, 'Expected mocked config, but found none'

    expected = config['auto_bind']
    actual = 'AUTO_BIND_NONE'
    assert actual == expected, f'Expected {expected} but found {actual}'

    actual = config['user']
    expected = 'admin'
    assert actual == expected, f'Expected {expected} but found {actual}'

    actual = config['password']
    expected = 'abadpassword'
    assert actual == expected, f'Expected {expected} but found {actual}'

    actual = config['client_strategy']
    expected = 'REUSABLE'
    assert actual == expected, f'Expected {expected} but found {actual}'

    actual = config['authentication']
    expected = 'AUTH_SIMPLE'
    assert actual == expected, f'Expected {expected} but found {actual}'


def test_connection_manager_get_connection():
    connection: Connection = connection_manager.get_connection('mocked', None)
    assert connection is not None, 'Expected a Connection, but found none.'



