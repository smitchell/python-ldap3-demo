
class Attribute:

    def __init__(self, name, value):
        self.name = name
        self.value = value


# class AttributeSchema(Schema):
#     name = fields.Str()
#     value = fields.Str()
#
#     @post_load
#     def create_attribute(self, data, **kwargs):
#         return Attribute(**data)



