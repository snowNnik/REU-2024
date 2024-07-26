from User import *
from Environment import *


class Entity:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class AttributeDeclaration:
    def __init__(self, name, attr_type):
        self.name = name
        self.attr_type = attr_type


class AttributeInstance:
    def __init__(self, declaration, value):
        self.declaration = declaration
        self.value = value

    def __str__(self):
        return f"{self.declaration.name}={self.value}"

    def __eq__(self, other):
        if isinstance(other, AttributeInstance):
            return (self.declaration.name == other.declaration.name and
                    self.value == other.value)
        return False


class AARelation:
    class AARelationEntry:
        def __init__(self, entity, attributes):
            #Entity object
            self.entity = entity
            #List of Attribute Objects connected to the entity to be used for accessing purposes
            self.attributes = attributes

        def __str__(self):
            return f"{self.entity}: {', '.join(str(attr) for attr in self.attributes)};"

    def __init__(self):#creates an empty dictionary
        self.relation_table = {}

    def add_relation_entry(self, entity, attributes):#adds attributes to the relation table  
  
        if entity.name in self.relation_table:#if the entity is already in an AARelationEntry in the table, add the attributes to that entry in the table 
            self.relation_table[entity.name].attributes.extend(attributes)
        else: #other wise create the entry with entity.name as the key and create the AAReltaionEntry with the entity object and the List of AttributesInstances objects 
            self.relation_table[entity.name] = self.AARelationEntry(entity, attributes)
    
    #Unused
    def get_attributes(self, entity):
        entry = self.relation_table.get(entity.name)
        return entry.attributes if entry else None
    #unused
    def are_related(self, entity, attribute):
        entry = self.relation_table.get(entity.name)
        return attribute in entry.attributes if entry else False
    
    def __str__(self):
        return "\n".join(str(entry) for entry in self.relation_table.values())

    def remove_attribute(self, attribute):
        for key in list(self.relation_table.keys()):
            entry = self.relation_table[key]
            entry.attributes = [
                attr for attr in entry.attributes if attr != attribute]
            if not entry.attributes:
                del self.relation_table[key]

    def remove_attribute_from_entity(self, entity, attribute):
        entry = self.relation_table.get(entity.name)
        if entry:
            entry.attributes = [
                attr for attr in entry.attributes if attr != attribute]

    def remove_relation_entries(self, entity):
        if entity.name in self.relation_table:
            del self.relation_table[entity.name]


if __name__ == "__main__":
    role_attr_decl = AttributeDeclaration("role", "String")
    role_attr_student = AttributeInstance(role_attr_decl, "Student")
    role_attr_professor = AttributeInstance(role_attr_decl, "Professor")

    current_time_attr = AttributeInstance(
        AttributeDeclaration("currentTime", "AbstractTime"), "withinOH")

    carlos = User("Carlos")
    josie = User("Josie")
    environment = Environment("ENV")

    aa_relation = AARelation()

    aa_relation.add_relation_entry(josie, [role_attr_student])
    aa_relation.add_relation_entry(carlos, [role_attr_professor])
    aa_relation.add_relation_entry(environment, [current_time_attr])

    print(aa_relation.are_related(josie, role_attr_student))
    print(aa_relation.are_related(josie, role_attr_professor))
    print(aa_relation.are_related(carlos, role_attr_student))
    print(aa_relation.are_related(carlos, role_attr_professor))
    print(aa_relation.are_related(environment, current_time_attr))
    print(aa_relation.are_related(environment, role_attr_student))
