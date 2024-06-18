from entity import Entity
# The user is an Entity that can also be assigned attributes

class User(Entity):
    # Takes default constructor from Entity that instantiates atttribute dictionary
    def __init__(self, attribute_list={}):
        super().__init__(attribute_list)