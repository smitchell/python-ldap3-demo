
from ldap3_demo.schemas.key_value_pair_schema import KeyValuePairSchema

schema = KeyValuePairSchema()
data = {
    "key": 'A key',
    "value": 'A value'
}


def test_attribute_create():
    print('test_attribute_create')

    attribute = schema.load(data)

    assert attribute.key == data['key']
    assert attribute.value == data['value']


def test_attribute_dump():
    print('test_attribute_dump')

    attribute = schema.load(data)

    assert attribute.key == data['key']
    assert attribute.value == data['value']

    output = schema.dump(attribute)
    assert output is not None

    assert output['key'] == data['key']
    assert output['value'] == data['value']

