class AddEntryRequest:

    def __init__(self, basedn, dn, object_class, attributes, controls=None):
        self.basedn = basedn
        self.dn = dn
        self.object_class = object_class
        self.attributes = attributes
        self.controls = controls

