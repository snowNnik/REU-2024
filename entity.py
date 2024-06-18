#Entity Class responsible for storing and creating attributes
class Entity:
    #default constructor
    #   creates empty attribute dictonary instance variable
    def __init__(self):
        self.attributes = {}  
    #parametized constructor
    #   Creates empty attribute dictionary instance variable and use the list 
    #   of tuples provided by attributeList to update the dictioanry using the 
    #   addAttributes function
    def __init__(self, attributeList):
        self.attributes = {}  
        self.addAttributes(attributeList)
    #add attributes
    #   updates the attribute dictioinary instance variable with the newAttributes 
    #   parameter
    def addAttributes(self, newAttributes):
        self.attributes.update(newAttributes)

