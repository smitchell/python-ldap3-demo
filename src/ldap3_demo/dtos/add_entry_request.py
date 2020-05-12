class AddEntryRequest:

    def __init__(self, dn, object_class, attributes):
        self.dn = dn
        self.object_class = object_class
        self.attributes = attributes
