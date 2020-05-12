from ldap3_demo.dtos.key_value_pair import KeyValuePair


def test_create_key_value_pair():
    print('test_create_attribute')

    attribute = KeyValuePair('My Key', 'My Value')

    expected = 'My Key'
    actual = attribute.key
    assert expected == actual

    expected = 'My Value'
    actual = attribute.value
    assert expected == actual

