class ModifyEntryRequest:

    def __init__(self, dn, changes, controls=None):
        self.dn = dn
        self.changes = changes
        self.controls = controls

