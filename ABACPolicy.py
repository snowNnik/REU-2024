from Entity import *
from AttributeDeclaration import *
from AttributeInstance import *
from Permission import *


class ABACPolicy:
    def __init__(self, entities, permissions, attribute_declarations, attribute_instances, pa_relation, aa_relation):
        self.entities = entities
        self.permissions = permissions
        self.attribute_declarations = attribute_declarations
        self.attribute_instances = attribute_instances
        self.pa_relation = pa_relation
        self.aa_relation = aa_relation

    def add_entity(self, entity_name):
        if self.get_entity(entity_name) is None:
            self.entities.append(Entity(entity_name))

    def remove_entity(self, entity_name):
        entity = self.get_entity(entity_name)
        if entity is not None:
            self.entities.remove(entity)
            self.aa_relation.remove_relation_entries(entity)

    def get_attribute_instances(self, attribute_declaration):
        result = []
        for instance in self.attribute_instances:
            if instance.get_declaration() == attribute_declaration:
                result.append(instance)
        return result

    def add_attribute_declaration(self, name, datatype):
        if self.get_attribute_declaration(name) is None:
            self.attribute_declarations.append(
                AttributeDeclaration(name, datatype))

    def remove_attribute_declaration(self, name):
        attribute_decl = self.get_attribute_declaration(name)
        if attribute_decl is not None:
            self.attribute_declarations.remove(attribute_decl)
            for instance in self.get_attribute_instances(attribute_decl):
                self.aa_relation.remove_attribute(instance)
                self.pa_relation.remove_attribute_from_all_entries(instance)

    def get_attribute_declaration(self, name):
        for declaration in self.attribute_declarations:
            if declaration.get_name() == name:
                return declaration
        return None

    def get_entity(self, entity_name):
        for entity in self.entities:
            if entity.get_name() == entity_name:
                return entity
        return None

    def add_attribute_instance(self, attribute_name, attribute_value):
        attribute_decl = self.get_attribute_declaration(attribute_name)
        if attribute_decl is not None:
            instance = AttributeInstance(attribute_decl, attribute_value)
            self.attribute_instances.append(instance)
            return instance
        return None

    def add_attribute_to_entity(self, entity_name, attribute_name, attribute_value):
        entity = self.get_entity(entity_name)
        if entity is not None:
            instance = self.add_attribute_instance(
                attribute_name, attribute_value)
            if instance is not None:
                attributes = [instance]
                self.aa_relation.add_relation_entry(entity, attributes)

    def get_attribute_instance(self, entity, attribute_name, attribute_value):
        instances = self.aa_relation.get_attributes(entity)
        for instance in instances:
            if instance.get_declaration().get_name() == attribute_name and instance.get_value() == attribute_value:
                return instance
        return None

    def remove_attribute_from_entity(self, entity_name, attribute_name, attribute_value):
        entity = self.get_entity(entity_name)
        if entity is not None:
            instance = self.get_attribute_instance(
                entity, attribute_name, attribute_value)
            if instance is not None:
                self.attribute_instances.remove(instance)
                self.aa_relation.remove_attribute_from_entity(entity, instance)

    def add_permission(self, permission_name):
        permission = self.get_permission(permission_name)
        if permission is None:
            permission = Permission(permission_name)
            self.permissions.append(permission)

    def remove_permission(self, permission_name):
        permission = self.get_permission(permission_name)
        if permission is not None:
            self.permissions.remove(permission)
            self.pa_relation.remove_relation_entries(permission)

    def get_permission(self, permission_name):
        for permission in self.permissions:
            if permission.get_name() == permission_name:
                return permission
        return None

    def add_permission_to_attribute(self, args):
        permission_name = args[1]
        permission = self.get_permission(permission_name)
        if permission is not None:
            attribute_entries = []
            for i in range(2, len(args), 2):
                attribute_name = args[i]
                attribute_value = args[i+1]
                attribute_decl = self.get_attribute_declaration(attribute_name)
                if attribute_decl is not None:
                    attribute_instance = AttributeInstance(
                        attribute_decl, attribute_value)
                    self.attribute_instances.append(attribute_instance)
                    attribute_entries.append(attribute_instance)
            self.pa_relation.add_relation_entry(permission, attribute_entries)

    def remove_attribute_from_permission(self, permission_name, attribute_name, attribute_value):
        permission = self.get_permission(permission_name)
        if permission is not None:
            # implementation missing
            pass

    def get_entities(self):#retrieves list of Entity objects
        return self.entities
 
    def set_entities(self, entities):
        self.entities = entities

    def get_attribute_declarations(self):#retrieves list of Attribute_Declarations objects
        return self.attribute_declarations

    def set_attribute_declarations(self, attribute_declarations):
        self.attribute_declarations = attribute_declarations

    def get_attribute_instances(self):#retrieves list of Attribute_Instances objects
        return self.attribute_instances

    def set_attribute_instances(self, attribute_instances):
        self.attribute_instances = attribute_instances

    def get_permissions(self):#retrieves list of Permission objects
        return self.permissions

    def set_permissions(self, permissions):
        self.permissions = permissions

    def get_pa_relation(self):#returns PARelation Object
        return self.pa_relation

    def set_pa_relation(self, pa_relation):
        self.pa_relation = pa_relation

    def get_aa_relation(self):#Returns AARelation
        return self.aa_relation

    def set_aa_relation(self, aa_relation):
        self.aa_relation = aa_relation

    def __str__(self):
        builder = []
        builder.append("ATTRS = ")
        for declaration in self.get_attribute_declarations():
            builder.append(str(declaration))
            builder.append(";")
        builder.append("\n")
        builder.append("PERMS = ")
        for permission in self.get_permissions():
            builder.append(str(permission))
            builder.append(";")
        builder.append("\n")
        builder.append("PA = \n")
        builder.append(str(self.get_pa_relation()))
        builder.append("\n")
        builder.append("AA = \n")
        builder.append(str(self.get_aa_relation()))
        builder.append("\n")
        return "".join(builder)
