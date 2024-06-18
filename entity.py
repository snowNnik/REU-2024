class Entity:

    def __init__(self, attributes={}):
        self.attributes = attributes

    def addAttributes(self, newAttributes):
        self.attributes.update(newAttributes)

