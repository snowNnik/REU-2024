# Updated attributeInstances, mostly complete with toString and equals to mess around with.

class attributeInstance():
    def __init__(self, category, value):
        self.category = category
        self.value = value
    
    def getCategory(self):
        return self.category

    def getValue(self):
        return self.value
    
    def setCategory(self, new_category):
        self.category = new_category

    def getValue(self):
        return self.value

    def setValue(self, new_value):
        self.value = new_value

    # TODO
    def toString(self):
        return "<" + ">" # Category datatype, category name, value

    def hashCode(self):
        prime = 31
        result = 1
        result = prime * result + (0 if (self.category is None) else self.category.hashCode())
        result = prime * result + (0 if (self.value is None) else self.value.hashCode())
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
        if (self.category is None):
            # TODO Perhaps instead raise an exception here if obj doesn't have category.
            if (obj.category is not None):
                return False
        elif (not self.category.equals(obj.category)):
            return False
        if (self.value is None):
            if (obj.value is not None):
                return False
        elif (not self.value.equals(obj.value)):
            return False
        return False
