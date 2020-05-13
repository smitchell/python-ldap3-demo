from ldap3_demo.controllers.ldap_controller import LdapController


def test_scrub_json_present_value():
    json = {
        'key1': 'A Key',
        'controls': 'control=value'
    }
    LdapController.scrub_json(json)
    assert 'controls' in json, 'Controls were not deleted'


def test_scrub_json_present_none():
    json = {
        'key1': 'A Key',
        'controls': None
    }
    LdapController.scrub_json(json)
    assert 'controls' not in json, 'Controls were not deleted'


def test_scrub_json_present_none_str():
    json = {
        'key1': 'A Key',
        'controls': 'None'
    }
    LdapController.scrub_json(json)
    assert 'controls' not in json, 'Controls were not deleted'


def test_scrub_json_present_empty():
    json = {
        'key1': 'A Key',
        'controls': ''
    }
    LdapController.scrub_json(json)
    assert 'controls' not in json, 'Controls were not deleted'
