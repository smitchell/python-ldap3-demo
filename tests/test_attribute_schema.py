import json

from flask import jsonify

from ldap3_demo.dtos.attribute_schema import AttributeSchema


def test_attribute_create():
    print('test_attribute_create')
    attribute_schema = AttributeSchema()
    data = {
        "name": 'A name',
        "values": ['A value']
    }
    attribute = attribute_schema.load(data)

    assert attribute.name == data['name']
    assert attribute.values == data['values']


def test_attribute_dump():
    print('test_attribute_dump')
    attribute_schema = AttributeSchema()
    data = {
        "name": 'A name',
        "values": ['A value']
    }
    attribute = attribute_schema.load(data)

    assert attribute.name == data['name']
    assert attribute.values == data['values']

    output = attribute_schema.dump(attribute)
    assert output is not None

    assert output['name'] == data['name']
    assert output['values'] == data['values']

