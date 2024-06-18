#Entity Class responsible for storing and creating attributes
class Entity:

    #   Parameterized Constructor
    #       creates empty attribute dictionary and uses the parameter attributeList
    #       to update the List by calling addAttribute(attributeList)
    def __init__(self, attributes={}):
        self.attributes = attributes

    #   addAttributes
    #       updates the attribute dictionary using the attribute dictionary newAttributs
    #       it was given
    def addAttributes(self, newAttributes):
        self.attributes.update(newAttributes)

