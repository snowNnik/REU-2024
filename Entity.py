class Entity:
    def __init__(self, name, assigned_attributes=None):
        #name is a string used for comparison 
        self.name = name
        self.assigned_attributes = assigned_attributes if assigned_attributes is not None else []

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_assigned_attributes(self):
        return self.assigned_attributes

    def set_assigned_attributes(self, assigned_attributes):
        self.assigned_attributes = assigned_attributes

    def add_assigned_attribute(self, attribute):
        if attribute not in self.assigned_attributes:
            self.assigned_attributes.append(attribute)

    def remove_assigned_attribute(self, attribute):
        self.assigned_attributes.remove(attribute)

    def __str__(self):
        return f"<{self.get_name()}>"
