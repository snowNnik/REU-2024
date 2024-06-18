from entity import Entity
# The user is an Entity that can also be assigned attributes

class User(Entity):
    # Takes default constructor from Entity that instantiates atttribute dictionary
    def __init__(self):
        super()
    
    # Takes default constructor from Entity that instates attribute dictionary and populates from given list.
    def __init__(self, attribute_list):
        super(attribute_list)

    # Takes a zone class, ensures the users attributes contain all the required attributes.
    def isAllowed(self, zone):
        zone_req = zone.attributes
        for key in zone_req.keys():
            if self.attributes[key] != zone_req[key]:
                return False
        return True