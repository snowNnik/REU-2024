from typing import List

#  ALL GOOD WITH THIS FILE

class Permission:
    name = ''
    related_attributes = []
    #     def __init__(self, name: str, related_attributes: List['AttributeInstance'] = None):

    def __init__(self, name: str, related_attributes=None):
        self.name = name
        self.related_attributes = related_attributes if related_attributes is not None else []

    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str):
        self.name = name

    def get_related_attributes(self):
        return self.related_attributes

    def set_related_attributes(self, related_attributes):
        self.related_attributes = related_attributes

    def add_related_attribute(self, attribute):
        if attribute not in self.related_attributes:
            self.related_attributes.append(attribute)

    def add_related_attributes(self, attributes):
        for attribute in attributes:
            self.add_related_attribute(attribute)

    def remove_related_attribute(self, attribute):
        self.related_attributes.remove(attribute)

# Written as override in Java
    def __str__(self) -> str:
        return f"<{self.name}>"

