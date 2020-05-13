class AddEntryRequest:

    def __init__(self, dn, object_class, attributes, controls=None):
        self.dn = dn
        self.object_class = object_class
        self.attributes = attributes
        self.controls = controls

