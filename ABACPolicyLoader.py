from typing import List

from Permission import *
from AttributeDeclaration import *
from AttributeInstance import *
from PARelation import *
from AARelation import *
from ABACPolicy import *


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
        for attr in attrs:
            attr = attr.strip()[1:-1]
            parts = attr.split(",")
            declaration = AttributeDeclaration(
                parts[1].strip(), parts[0].strip())
            result.append(declaration)
        return result

    @staticmethod
    def read_entities(entities_line: str) -> List[Entity]:
        result = []
        entities = entities_line.split(";")
        for entity in entities:
            entity = entity.strip()[1:-1]
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
        result = []
        attributes = attributes_line.split(";")
        for attribute in attributes:
            attribute = attribute.strip()[1:-1]
            parts = attribute.split(",")
            name = parts[0].strip()
            value = parts[1].strip()
            declaration = ABACPolicyLoader.get_declaration(
                name, declarations_list)
            result.append(AttributeInstance(declaration, value))
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
        result = PARelation()
        entries = pa_line.split("-")
        for entry in entries:
            parts = entry.split(":")
            attributes = parts[0].strip()
            permission_name = parts[1].strip()
            instances = ABACPolicyLoader.read_attribute_instances(
                attributes, attribute_declarations_list)
            permission = ABACPolicyLoader.get_permission(
                permission_name, permissions)
            result.add_relation_entry(permission, instances)
        return result

    @staticmethod
    def mix_attribute_instance_lists(original_list: List[AttributeInstance], new_list: List[AttributeInstance]) -> List[AttributeInstance]:
        for instance in new_list:
            if instance not in original_list:
                original_list.append(instance)
        return original_list

    @staticmethod
    def read_aa(aa_line: str, entities: List[Entity], attribute_declarations_list: List[AttributeDeclaration], instances: List[AttributeInstance]) -> AARelation:
        result = AARelation()
        entries = aa_line.split(";")
        for entry in entries:
            parts = entry.split(":")
            entity_name = parts[0].strip()[1:-1]
            attributes = parts[1].strip()
            user_attributes = ABACPolicyLoader.read_attribute_instances(
                attributes, attribute_declarations_list)
            instances = ABACPolicyLoader.mix_attribute_instance_lists(
                instances, user_attributes)
            entity = ABACPolicyLoader.get_entity(entity_name, entities)
            result.add_relation_entry(entity, user_attributes)
        return result

    @staticmethod
    def load_abac_policy(filename: str) -> ABACPolicy:
        entities = None
        attribute_declarations = None
        attribute_instances = []
        permissions = None
        pa_relation = None
        aa_relation = None

        with open(filename, "r") as file:
            for line in file:
                parts = line.split("=")
                if parts[0].strip() == "ATTRS":
                    attribute_declarations = ABACPolicyLoader.read_attribute_declarations(
                        parts[1])
                elif parts[0].strip() == "PERMS":
                    permissions = ABACPolicyLoader.read_permissions(parts[1])
                elif parts[0].strip() == "ENTITIES":
                    entities = ABACPolicyLoader.read_entities(parts[1])
                elif parts[0].strip() == "PA":
                    pa_relation = ABACPolicyLoader.read_pa(
                        parts[1], permissions, attribute_declarations, attribute_instances)
                elif parts[0].strip() == "AA":
                    aa_relation = ABACPolicyLoader.read_aa(
                        parts[1], entities, attribute_declarations, attribute_instances)

        return ABACPolicy(entities, permissions, attribute_declarations, attribute_instances, pa_relation, aa_relation)
