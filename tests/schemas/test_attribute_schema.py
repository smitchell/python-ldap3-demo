
from ldap3_demo.schemas.attribute_schema import AttributeSchema

schema = AttributeSchema()
data = {
    "name": 'A name',
    "value": 'A value'
}


def test_attribute_create():
    print('test_attribute_create')

    attribute = schema.load(data)

    assert attribute.name == data['name']
    assert attribute.value == data['value']


def test_attribute_dump():
    print('test_attribute_dump')

    attribute = schema.load(data)

    assert attribute.name == data['name']
    assert attribute.value == data['value']

    output = schema.dump(attribute)
    assert output is not None

    assert output['name'] == data['name']
    assert output['value'] == data['value']

