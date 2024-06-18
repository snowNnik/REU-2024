<<<<<<< HEAD
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
=======
class Entity:

    #   creates empty attribute dictionary
    #   Parameterized Constructor
    #       creates empty attribute dictionary and uses the parameter attributeList
    #       to update the List by calling addAttribute(attributeList)
    def __init__(self, attributes={}):
        self.attributes = attributes

    #   addAttributes
    #       updates the attribute dictionary using the attribute dictionary newAttributs
    #       it was given
>>>>>>> f310f0fca22b2a6cd3ade76223493d46d3f42e03
    def addAttributes(self, newAttributes):
        self.attributes.update(newAttributes)

