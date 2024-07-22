class AttributeDeclaration:
    def __init__(self, name: str, datatype: str):#creates the attribute declaration object which stores the name and datatype of an Attribute
        #the name variable is mostly used for comparisons 
        self.name = name
        #data type isn't really used
        self.datatype = datatype

    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str):
        self.name = name

    def get_datatype(self) -> str:
        return self.datatype

    def set_datatype(self, datatype: str):
        self.datatype = datatype

    def __str__(self) -> str:
        return f"<{self.get_datatype()}, {self.get_name()}>"

    def __hash__(self) -> int:
        return hash((self.name, self.datatype))

    def __eq__(self, other: 'AttributeDeclaration') -> bool:
        if not isinstance(other, AttributeDeclaration):
            return False
        return self.name == other.name and self.datatype == other.datatype


# Here comes some code that is not relevant
