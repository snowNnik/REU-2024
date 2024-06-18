class Entity:

    def __init__(self):
        self.attributes = {}  
        
    def __init__(self, attributeList):
        self.attributes = {}  
        self.addAttribute(attributeList)
            
    def addAttributes(self, newAttributes):
        self.attributes.update(newAttributes)

