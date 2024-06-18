from entity import Entity
# The user is an Entity that can also be assigned attributes

class User(Entity):
    # Takes default constructor from Entity that instantiates atttribute dictionary
    def __init__(self, attribute_list={}):
        super().__init__(attribute_list)

    # Takes a zone class, ensures the users attributes contain all the required attributes.
    def isAllowed(self, zone):
        zone_req = zone.attributes
        for key in zone_req.keys():
            if key not in self.attributes.keys():
                return False
            elif self.attributes[key] != zone_req[key]:
                return False
        return True