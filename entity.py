class Entity:
    #   Parameterized Constructor
    #       creates empty attribute dictionary and uses the parameter attributeList 
    #       to update teh List by calling addAttribute(attributeList)
    def __init__(self, attributeList=()):
        self.attributes = {}  
        self.addAttribute(attributeList)
    #   addAttributes
    #       updates the attribute dictionary using the attribute dictionary newAttributs
    #       it was given
    def addAttributes(self, newAttributes):
        self.attributes.update(newAttributes)

