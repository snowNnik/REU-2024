from entity import Entity
# The Zone is an Entity that can also be assigned attributes

class Zone(Entity):
    # Takes default constructor from Entity that instantiates atttribute dictionary
    # Must also store an x, y coordinate
    def __init__(self, x, y):
        super()
        self.x = x
        self.y = y
    
    # Takes default constructor from Entity that instates attribute dictionary and populates from given list.
    # Must also store an x, y coordinate
    def __init__(self, attribute_list, x, y):
        super(attribute_list)
        self.x = x
        self.y = y

    # In order to return coordinate of zone
    def get_coordinates(self):
        return (self.x, self.y)
    
    # In order to return current coordinate
    def set_coordinates(self, x, y):
        self.x = x
        self.y = y

   