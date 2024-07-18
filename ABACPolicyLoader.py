from typing import List

from Permission import *
from AttributeDeclaration import *
from AttributeInstance import *
from PARelation import *
from AARelation import *
from ABACPolicy import *
from ABACMonitor import *


class ABACPolicyLoader:
    @staticmethod
    def read_permissions(perms_line: str) -> List[Permission]:
        result = []
        perms = perms_line.split(";")
        for perm_str in perms:
            perm_str = perm_str.strip()[1:-1]
            permission = Permission(perm_str)
            result.append(permission)
        return result

    @staticmethod
    def read_attribute_declarations(attrs_line: str) -> List[AttributeDeclaration]:
        result = []
        attrs = attrs_line.split(";")
        # print("Attribute Declaration")
        for attr in attrs:
            # print(attr)
            attr = attr.strip()[1:-1]
            parts = attr.split(",")
            print(parts)
            declaration = AttributeDeclaration(
                parts[1].strip(), parts[0].strip())
            result.append(declaration)
            # print("     " + str(declaration))
        return result

    @staticmethod
    def read_entities(entities_line: str) -> List[Entity]:
        result = []
        entities = entities_line.split(";")
        # print("Entity Declaration")
        for entity in entities:
            entity = entity.strip()[1:-1]
            # print("     " + entity)
            new_entity = Entity(entity)
            result.append(new_entity)
        return result

    @staticmethod
    def get_declaration(attribute_name: str, declarations_list: List[AttributeDeclaration]) -> AttributeDeclaration:
        for declaration in declarations_list:
            if declaration.name == attribute_name:
                return declaration
        return None

    @staticmethod
    def read_attribute_instances(attributes_line: str, declarations_list: List[AttributeDeclaration]) -> List[AttributeInstance]:
        def mySort(e):
            return e.get_declaration().get_name() == "userName"
        exclusionZoneExists= False
        result = []
        radius = ""
        type = ""
        attributes = attributes_line.split(";")
        # print(attributes)
        for attribute in attributes:
            # print("     " + attribute)
            attribute = attribute.strip()[1:-1]
            parts = attribute.split(",")
            name = parts[0].strip()
            value = parts[1].strip()
            declaration = ABACPolicyLoader.get_declaration(name, declarations_list)
            result.append(AttributeInstance(declaration, value))
            if(declaration.get_name() == "exclusionZone" and not(exclusionZoneExists)): #if the current object is exclusion
                exclusionZone = value.split("!")#split into radius and value
                radius = int(exclusionZone[0].strip()) #radius is radius of the zone
                exclusionValue= exclusionZone[1].strip() #value is the value we will give to the attribute which will determine whether or not its allowed in
                exclusionZoneExists= True
        result.sort(key=mySort, reverse=True)
        if(exclusionZoneExists==True):
            permission_Attributes = pa_relation.get_dictionary()
            def addPerm(a,b):
                if(str("Grid"+str(a)+"x"+str(b)) in permission_Attributes.keys()):#checks if the grid position is in keys
                    if(exclusionValue == "D"): #if the value is denial add Denial to everything so noone is allowed in
                        permission = ABACPolicyLoader.get_permission("nonEntry", permissions)
                        if(not(permission in permission_Attributes[str("Grid"+str(a)+"x"+str(b))])):
                            permission_Attributes[str("Grid"+str(a)+"x"+str(b))][permission] = [[AttributeInstance(AttributeDeclaration("userName","String"),str("Grid"+str(a)+"x"+str(b)))]]
                        else:
                            for entry in permission_Attributes[str("Grid"+str(a)+"x"+str(b))][permission]: 
                                entry.append(AttributeInstance(AttributeDeclaration("Denied","Boolean"),True))#for each entry permission list related to that grid space add the  attribute
                    else:#else they can only enter if they are owned by the value set by ExclusionZone
                        permission = ABACPolicyLoader.get_permission("Entry", permissions)
                        for entry in permission_Attributes[str("Grid"+str(a)+"x"+str(b))][permission]:
                            entry.append(AttributeInstance(AttributeDeclaration("ownedBy","String"),exclusionValue))
            position = result[0].get_value().split("x") # grabs the location data of the current attributes
            row = int(str(position[0])[4:]) 
            column = int(position[1])
            for x in range(-radius,radius+1):#goes through each square to add the permissions
                for y in range(-radius,radius+1):
                    addPerm(row+x,column+y)
        return result
       

    @staticmethod
    def get_permission(permission_name: str, permissions: List[Permission]) -> Permission:
        for permission in permissions:
            if permission.name == permission_name:
                return permission
        return None

    @staticmethod
    def get_entity(entity_name: str, entities: List[Entity]) -> Entity:
        for entity in entities:
            if entity.name == entity_name:
                return entity
        return None

    @staticmethod
    def read_pa(pa_line: str, permissions: List[Permission], attribute_declarations_list: List[AttributeDeclaration], instances: List[AttributeInstance]) -> PARelation:
        result = PARelation() #Dictionary in Place of PARelation
        entries = pa_line.split("-")
        # print("Permission Attributes")
        for entry in entries:
            parts = entry.split(":")
            attributes = parts[0].strip()
            permission_name = parts[1].strip()
            instances = ABACPolicyLoader.read_attribute_instances(attributes, attribute_declarations_list)
            permission = ABACPolicyLoader.get_permission(permission_name, permissions)
            result.add_relation_entry(permission, instances)
        return result

    @staticmethod
    def mix_attribute_instance_lists(original_list: List[AttributeInstance], new_list: List[AttributeInstance]) -> List[AttributeInstance]:
        for instance in new_list:
            if instance not in original_list:
                original_list.append(instance)
        return original_list

    @staticmethod
    def read_aa(aa_line: str, entities: List[Entity], attribute_declarations_list: List[AttributeDeclaration], instances: List[AttributeInstance],permission =None) -> AARelation:
        result = AARelation()
        entries = aa_line.split("-")
        for entry in entries:
            parts = entry.split(":")
            entity_name = parts[1].strip()[1:-1]
            # print("Entity Attributes " + entity_name)
            attributes = parts[0].strip()
            user_attributes = ABACPolicyLoader.read_attribute_instances(attributes, attribute_declarations_list)
            instances = ABACPolicyLoader.mix_attribute_instance_lists( instances, user_attributes)
            entity = ABACPolicyLoader.get_entity(entity_name, entities)
            result.add_relation_entry(entity, user_attributes)
        return result

    @staticmethod
    def load_abac_policy(filename: str) -> ABACPolicy:
        def mySort(e):
            return e.get_name() != "Entry"
        entities = None
        attribute_declarations = None
        attribute_instances = []
        global permissions
        permissions = None
        global pa_relation
        pa_relation = None
        aa_relation = None
        filename = "../REU-2024/inputs/" + str(filename)
        with open(filename, "r") as file:
            for line in file:
                parts = line.split("=")
                if parts[0].strip() == "ATTRS":
                    attribute_declarations = ABACPolicyLoader.read_attribute_declarations(
                        parts[1])
                elif parts[0].strip() == "PERMS":
                    permissions = ABACPolicyLoader.read_permissions(parts[1])
                    permissions.sort(key=mySort)
                elif parts[0].strip() == "ENTITIES":
                    entities = ABACPolicyLoader.read_entities(parts[1])
                elif parts[0].strip() == "PA":
                    pa_relation = ABACPolicyLoader.read_pa( parts[1], permissions, attribute_declarations, attribute_instances)
                elif parts[0].strip() == "AA":
                    aa_relation = ABACPolicyLoader.read_aa(parts[1], entities, attribute_declarations, attribute_instances,permissions[0])
        return ABACPolicy(entities, permissions, attribute_declarations, attribute_instances, pa_relation, aa_relation)