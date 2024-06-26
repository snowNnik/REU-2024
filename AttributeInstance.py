class AttributeInstance:
    def __init__(self, declaration, value):
        self.declaration = declaration
        self.value = value

    def get_declaration(self):
        return self.declaration

    def set_declaration(self, declaration):
        self.declaration = declaration

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

    def __str__(self):
        return f"<{self.get_declaration().get_datatype()}, {self.get_declaration().get_name()}, {self.get_value()}>"

    def __hash__(self):
        return hash((self.declaration, self.value))

    def __eq__(self, other):
        if not isinstance(other, AttributeInstance):
            return False
        return self.declaration == other.declaration and self.value == other.value
