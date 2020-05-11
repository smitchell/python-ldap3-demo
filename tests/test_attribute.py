from ldap3_demo.dtos.attribute import Attribute


def test_create_attribute():
    print('test_create_attribute')
    data = {
        "name": "My Attribute",
        "value": "My Value"
    }

    attribute = Attribute('My Attribute', 'My Value')
    print('attribute = ', attribute)

    expected = 'My Attribute'
    actual = attribute.name
    assert expected == actual

    expected = 'My Value'
    actual = attribute.value
    assert expected == actual

