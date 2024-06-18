from entity import Entity
# The Zone is an Entity that can also be assigned attributes

class Zone(Entity):
    # Takes default constructor from Entity that instantiates atttribute dictionary
    # Must also store an x, y coordinate
    def __init__(self, x, y, attribute_list={}):
        super().__init__(attribute_list)
        self.x = x
        self.y = y
    
    # In order to return coordinate of zone
    def get_coordinates(self):
        return (self.x, self.y)
    
    # In order to return current coordinate
    def set_coordinates(self, x, y):
        self.x = x
        self.y = y

   