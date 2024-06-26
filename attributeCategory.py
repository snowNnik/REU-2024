# Updated attributeCategory, mostly complete with toString and equals to mess around with.

class attributeInstance():
    def __init__(self, name, datatype):
        self.name = name
        self.datatype = datatype
    
    def getName(self):
        return self.name

    def getDatatype(self):
        return self.datatype
    
    def setName(self, new_name):
        self.name = new_name

    def setDatatype(self, new_datatype):
        self.datatype = new_datatype

    # TODO
    def toString(self):
        return "<" + ">" # Datatype, name

    def hashCode(self):
        prime = 31
        result = 1
        result = prime * result + (0 if (self.datatype is None) else self.category.hashCode())
        result = prime * result + (0 if (self.name is None) else self.value.hashCode())
        return result

    def equals(self, obj):
        if (self is obj):
            return True
        if (self is None):
            return False
        # TODO No classes in Java. Maybe we can just skip this step then. I can't think right now.
		# if (self.getClass() != obj.getClass())
		#	return false;
		# AttributeInstance other = (AttributeInstance) obj;
        if (self.datatype is None):
            # TODO Perhaps instead raise an exception here if obj doesn't have category.
            if (obj.datatype is not None):
                return False
        elif (not self.datatype.equals(obj.datatype)):
            return False
        if (self.name is None):
            if (obj.name is not None):
                return False
        elif (not self.name.equals(obj.name)):
            return False
        return False
