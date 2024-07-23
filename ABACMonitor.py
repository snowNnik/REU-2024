from typing import List
from Permission import *
from AttributeDeclaration import *
from AttributeInstance import *
from PARelation import *
from AARelation import *
from ABACPolicy import *

class ABACMonitor:
    def __init__(self, policy: ABACPolicy):#creates the policy variables so they can be accessed later to gather up the required attributes for comparisons
        self.policy = policy

    def check_access(self, user: Entity, obj: Entity, environment: Entity, permission: Permission,row,col) -> bool:#retrieves the user's attributes, the object's attributes, and the
        #environment's attributes before sending them to check_access_with_attribute_bag for comparaisonts 
        attribute_bag = []#the list that will hold all of the attributes that will be compared against permission's attributes
        user_attributes = self.policy.aa_relation.get_attributes(user) #grabs all of the attributes inside user's AARelation 
        if user_attributes is not None:#If it's not empty then add user's attributes to attribute bag
            attribute_bag.extend(user_attributes)
        object_attributes = self.policy.aa_relation.get_attributes(obj)#grabs all of the attributes inside the Entity's AARelation 
        if object_attributes is not None:#If it's not empty then add user's attributes to attribute bag
            attribute_bag.extend(object_attributes)
        env_attributes = self.policy.aa_relation.get_attributes(environment)#grabs all of the attributes inside the Evnrionment's AARelation 
        if env_attributes is not None:#If it's not empty then add user's attributes to attribute bag
            attribute_bag.extend(env_attributes)
        return self.check_access_with_attribute_bag(attribute_bag, permission, row, col)#sends attriubte bag to be compared against permission

    def check_access_with_attribute_bag(self, attribute_bag: List[AttributeInstance], permission: Permission, row, col) -> bool:
        #will print everyt comparison to ensure that the proper attributes have been assigned
        '''for entry in self.policy.pa_relation.get_entries(permission, row, col):
            print("Grid" + str(row) + "x" + str(col) + "    " + str(permission) + "     ", end="")
            for x in entry:
                print(str(x), end=" ")
            print(" vs ", end=" ")
            for entry in attribute_bag:
                print(str(entry), end=" ")
            print()'''
        for entry in self.policy.pa_relation.get_entries(permission, row, col): #for every entry associated with the permissions
            if all(attr in attribute_bag for attr in entry): #if every attribute associated is in the PARelation is in the attributebbag return True
                return True
        return False #Otherwise return False 


if __name__ == "__main__":
    write_permission = Permission("writePermission")
    read_permission = Permission("readPermission")
    permissions = [write_permission, read_permission]

    role_attr_decl = AttributeDeclaration("role", "String")
    role_attr_student = AttributeInstance(role_attr_decl, "Student")
    role_attr_professor = AttributeInstance(role_attr_decl, "Professor")

    current_time_decl = AttributeDeclaration("currentTime", "AbstracTime")
    current_time_attr = AttributeInstance(current_time_decl, "withinOH")

    attribute_declarations = [role_attr_decl, current_time_decl]
    attribute_instances = [role_attr_student,
                           role_attr_professor, current_time_attr]

    pa_relation = PARelation()

    readers = [role_attr_student]
    pa_relation.add_relation_entry(read_permission, readers)

    readers = [role_attr_professor]
    pa_relation.add_relation_entry(read_permission, readers)

    writers = [role_attr_professor, current_time_attr]
    pa_relation.add_relation_entry(write_permission, writers)

    print("PARelation:")
    print("------------------------------------------------------")
    print(pa_relation)
    print("------------------------------------------------------")

    carlos = User("Carlos")
    josie = User("Josie")
    obj = Object("file.txt")
    environment = Environment("ENV")

    entities = [carlos, josie, obj, environment]

    aa_relation = AARelation()

    josie_attributes = [role_attr_student]
    aa_relation.add_relation_entry(josie, josie_attributes)

    carlos_attributes = [role_attr_professor]
    aa_relation.add_relation_entry(carlos, carlos_attributes)

    env_attributes = [current_time_attr]
    aa_relation.add_relation_entry(environment, env_attributes)

    print("AARelation:")
    print("------------------------------------------------------")
    print(aa_relation)
    print("------------------------------------------------------")

    policy = ABACPolicy(entities, permissions, attribute_declarations,
                        attribute_instances, pa_relation, aa_relation)

    abac_monitor = ABACMonitor(policy)

    print(f"Can {josie} be granted {read_permission}?")
    print(abac_monitor.check_access(josie, obj, environment, read_permission))

    print(f"Can {josie} be granted {write_permission}?")
    print(abac_monitor.check_access(josie, obj, environment, write_permission))

    print(f"Can {carlos} be granted {write_permission}?")
    print(abac_monitor.check_access(carlos, obj, environment, write_permission))

    print(f"Can {carlos} be granted {read_permission}?")
    print(abac_monitor.check_access(carlos, obj, environment, read_permission))
