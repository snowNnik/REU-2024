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
    def read_permissions(perms_line: str) -> List[Permission]: #Returns a list of all permissions object created by the user in the file
        result = []#perms_line=<permissionName>;<permissionName> Ex: <Entry>;<NonEntry>
        perms = perms_line.split(";") # 
        for perm_str in perms: #iterate through the permissions
            perm_str = perm_str.strip()[1:-1]#Remove < and > 
            permission = Permission(perm_str) #Create the Permission Object with the name perm_str
            result.append(permission) #Adds permission to the List object result
        return result

    @staticmethod
    def read_attribute_declarations(attrs_line: str) -> List[AttributeDeclaration]:#Returns list of AttributeDeclarations objects created by the user in the file
        result = []#attrs_line= <datatype1, name1>; <datatype2, name2> 
        attrs = attrs_line.split(";") # [<datatype1, name1>, <datatype2, name2>]
        # print("Attribute Declaration")
        for attr in attrs:#Creates all of the attriubte_Declaration object and puts them in the result list to be returned
            # print(attr)
            attr = attr.strip()[1:-1] #removes < and >
            parts = attr.split(",") #parts = [datatype1, name1]
            #print(parts)
            declaration = AttributeDeclaration(parts[1].strip(), parts[0].strip()) #creates the attriubte_declaration object out of parts 
            result.append(declaration) #Adds declaration object to the List object result
            # print("     " + str(declaration))
        return result

    @staticmethod
    def read_entities(entities_line: str) -> List[Entity]:#Returns list of Entiy objects created by the user in the file
        result = []#entities_line = "<Entity1>;<Entity2>;<Entity3>""  
        entities = entities_line.split(";")# entites = ["<Entity1>","<Entity2>","<Entity3>"]   
        # print("Entity Declaration")
        for entity in entities: #entity = <Entity1>
            entity = entity.strip()[1:-1] # entity = "Entity1"
            # print("     " + entity)
            new_entity = Entity(entity)# creates Entity object with the name entity
            result.append(new_entity) #appends the new entity to the List result
        return result

    @staticmethod
    def get_declaration(attribute_name: str, declarations_list: List[AttributeDeclaration]) -> AttributeDeclaration: #returns attribute_declaration in the 
        #list of declarations which has the declaration_name which matches the attribute_name entered into the list
        for declaration in declarations_list:
            if declaration.name == attribute_name:
                return declaration
        return None
   
    def addToAttributeList(permission_Attributes, gridName, permission, name, datatype, value):#Adds an attriubte to every attribute in an list of lists of attribute instances
        for entry in permission_Attributes[gridName][permission]: 
                entry.append(AttributeInstance(AttributeDeclaration(name, datatype),value))#for each entry permission list related to that grid space add the  attribute
   
    # To briefly explain why addPerm exists there is an interesting interaction between the attributes of entities and the attributes of permissions, 
    # namely, in order attributes of the entity to affect the permission attributes both the permission attriubtes AND the entity attributes have to be loaded
    # We, for the sake of simplicity, decided to hard code in exclusionZone variable, which represents an exclusion zone around things like airports or military bases
    # where drones/civillian drones obviously can't fly. 
    def addPerm(exclusionValue,permission_Attributes, a,b):#add an attribute to a list "Whethere it be there or not"
                gridName = str("Grid"+str(a)+"x"+str(b))
                if(gridName in permission_Attributes.keys()):#checks if the grid position is in keys
                    if(exclusionValue == "D"): #if the value is denial add Denial to everything so no one is allowed in
                        permission = ABACPolicyLoader.get_permission("nonEntry", permissions) #find the Non-Entry permission
                        if(not(permission in permission_Attributes[gridName].keys())): #if the nonEntry doesn't exist as a key dictionary at the located at  str("Grid"+str(a)+"x"+str(b) then at 
                            #an entry contianing the attriubte Denial using that as a key 
                            permission_Attributes[gridName][permission] = [[AttributeInstance(AttributeDeclaration("userName","String"),str("Grid"+str(a)+"x"+str(b)))]] 
                        else:#Otherwise add it to the list of things to ensure nothing can enter
                            permission_Attributes[gridName][permission].append(AttributeInstance(AttributeDeclaration("userName","String"),str("Grid"+str(a)+"x"+str(b)))) 
                    else:#else they can only enter if they are owned by the value set by ExclusionZone
                        permission = ABACPolicyLoader.get_permission("Entry", permissions) #Grabs the Entry permission object for accessing purposes
                        ABACPolicyLoader.addToAttributeList(permission_Attributes, gridName, permission, "ownedBy", "String", exclusionValue) #adds ownedBy to every entry permission meaning only 
                        #those with the attribute may enter
    @staticmethod
    def read_attribute_instances(attributes_line: str, declarations_list: List[AttributeDeclaration]) -> List[AttributeInstance]: #read attributes from the file 
        #to create attribute instances List which assign entities their attributes and PARelations the attributes required to access those permissions
        def mySort(e):#function used to ensure the userName attribute is first for accessing reasons
            return e.get_declaration().get_name() == "userName"
        result = []
        exclusionZoneradi = [] #List which holds the radius of every exclusionZone
        exclusionZoneValues = [] #List which holds the values of every exclusionZone
        exclusionZoneExists = False
        attributes = attributes_line.split(";") #[<attributeDeclaration1, value1>, <atttributeDeclration2,value2>]
        # print(attributes)
        for attribute in attributes:
            # print("     " + attribute)
            attribute = attribute.strip()[1:-1]#attributeDeclaration1, value1
            parts = attribute.split(",")#[attributeDeclaration1, value1]
            name = parts[0].strip()#attributeDeclaration1
            value = parts[1].strip()#value1
            declaration = ABACPolicyLoader.get_declaration(name, declarations_list)#Gets the declaration that matches the declaration name
            result.append(AttributeInstance(declaration, value))#create AttributeInstance using the declaration and the value and add it to result
            if(declaration.get_name() == "exclusionZone"): #if the current object is exclusionZone 
                exclusionZone = value.split("!")#split into radius and value
                exclusionZoneradi.append(int(exclusionZone[0].strip())) #radius of every exclusionZone
                exclusionZoneValues.append(exclusionZone[1].strip()) #holds every value we will give to the attribute which will determine whether or not its allowed in
                exclusionZoneExists =True
        result.sort(key=mySort, reverse=True)#sorts the List so the "userName" Declaration is first which is where the name of the drone and the property is 
        # the property's name must be denoted by <userName, Grid<row>x<column> >
        if(exclusionZoneExists):
            permission_Attributes = pa_relation.get_dictionary() #Grabs the permission Attribute dictionary to begin adding attributes to entry permission
            position = result[0].get_value().split("x") # grabs the location data of the current attributes
            print(position)
            row = int(str(position[0])[4:]) #grabs the row
            column = int(position[1]) #grabs column
            for entry in range(0,len(exclusionZoneradi)): #for every Exclusion Zone found
                for x in range(-exclusionZoneradi[entry],exclusionZoneradi[entry]+1):#goes through each square in the radius to add the permissions
                    for y in range(-exclusionZoneradi[entry],exclusionZoneradi[entry]+1): 
                        ABACPolicyLoader.addPerm(exclusionZoneValues[entry], permission_Attributes,row+x,column+y)
        return result
       

    @staticmethod
    def get_permission(permission_name: str, permissions: List[Permission]) -> Permission: #returns the Permission object whose name variable matches 
        #permission_name string variable
        for permission in permissions:
            if permission.name == permission_name:
                return permission
        return None

    @staticmethod
    def get_entity(entity_name: str, entities: List[Entity]) -> Entity:#returns the Entity object whose name variable matches 
        #entity_name string variable
        for entity in entities:
            if entity.name == entity_name:
                return entity
        return None

    @staticmethod
    def read_pa(pa_line: str, permissions: List[Permission], attribute_declarations_list: List[AttributeDeclaration], instances: List[AttributeInstance]) -> PARelation:
        result = PARelation() #Dictionary in Place of PARelation
        entries = pa_line.split("-") #Separate Permission attributes are separated by dashes
        #entries should be something like [<declaration,value>; <declaration, value> : Permission, <declaration, value>; <declaration, value> : Permission, ...]
        # print("Permission Attributes")
        for entry in entries: 
            parts = entry.split(":") # splits each entry into attribute instances and permission names
            attributes = parts[0].strip() #<declaration ,value>; <declaration , value> 
            permission_name = parts[1].strip()#Permission
            instances = ABACPolicyLoader.read_attribute_instances(attributes, attribute_declarations_list) #Creates a list of Attribute Instances objects which represents the permissions
            #needed/required not to be present depending on the type of permission (Entry/nonEntry)
            permission = ABACPolicyLoader.get_permission(permission_name, permissions)# retrives the permission 
            result.add_relation_entry(permission, instances) #adds the instance dictionary in it's proper place using .add_relation_entry
        return result

    @staticmethod#not used
    def mix_attribute_instance_lists(original_list: List[AttributeInstance], new_list: List[AttributeInstance]) -> List[AttributeInstance]: #adds attributes from the new list into the 
        #old list if they aren't already in there and returns old list
        for instance in new_list:
            if instance not in original_list:
                original_list.append(instance)
        return original_list

    @staticmethod
    def read_aa(aa_line: str, entities: List[Entity], attribute_declarations_list: List[AttributeDeclaration], instances: List[AttributeInstance],permission =None) -> AARelation:
        #Creates the AARelation associated with the Entity object entered
        
        result = AARelation() #creates an AARelation object which consists of an empty dictionary
        #aa_line = "<datatype1, declarationName1>; <datatype2,declarationName2> : <Entity1> - <datatype3, declarationName3>; <datatype4,declarationName4> : <Entity2> "
        entries = aa_line.split("-") # ["<datatype1, declarationName1>; <datatype2,declarationName2> : Entity1","<datatype3, declarationName3>; <datatype4,declarationName4> : Entity2"]
        for entry in entries:
            parts = entry.split(":")#[<datatype1, declarationName1>; <datatype2,declarationName2>", "<Entity1>"]
            entity_name = parts[1].strip()[1:-1] #entity_name = "Entity"
            # print("Entity Attributes " + entity_name)
            attributes = parts[0].strip() #<datatype1, declarationName1>; <datatype2,declarationName2>
            user_attributes = ABACPolicyLoader.read_attribute_instances(attributes, attribute_declarations_list)#create the entities attribute instance list
            entity = ABACPolicyLoader.get_entity(entity_name, entities)#finds the entity that the attributes are attached to
            result.add_relation_entry(entity, user_attributes) #adds entity and user attribute to AA for later use 
        return result

    @staticmethod
    def load_abac_policy(filename: str) -> ABACPolicy:
        entities = None #holds entities
        attribute_declarations = None #hold attribute declarations (datatype and name)
        attribute_instances = [] #A list of instances which hold (declaration and value)
        global permissions
        permissions = None #holds permission (which are used to hold permission names)
        global pa_relation
        pa_relation = None #holds PARelation which is a dictionary whose first key is the name of the gridspace you are trying to access which holds another dictionary
        #which uses the permission objects as keys, contained within the second dictionary is a list of attributes that serve as the requirements to the associated 
        #permission
        aa_relation = None #holds all the attributes related to a certain object
        filename = "../REU-2024/inputs/" + str(filename) #adds the path to the inputs folder to the file name  
        with open(filename, "r") as file: #opens file to read from
            for line in file: #For every line in file split it into a list based on =  
                parts = line.split("=")
                match parts[0].strip():#if the first element of the list matches the options on the menu then the following code is executed 
                    case  "ATTRS":#Loads attrubte declarations (datatypes and names)
                        attribute_declarations = ABACPolicyLoader.read_attribute_declarations(parts[1]) 
                    case "PERMS":#Loads Permissions (permission_Names)
                        permissions = ABACPolicyLoader.read_permissions(parts[1])
                    case "ENTITIES":# Loads entities 
                        entities = ABACPolicyLoader.read_entities(parts[1])
                    case "PA":#Gives Permissions the attributes to perform the action associated with them, MUST COME BEFORE AA IF MAKING AN EXCLUSIONZONE
                        pa_relation = ABACPolicyLoader.read_pa( parts[1], permissions, attribute_declarations, attribute_instances)
                    case "AA":#gives Entities the attributes they are assigned by the user
                        aa_relation = ABACPolicyLoader.read_aa(parts[1], entities, attribute_declarations, attribute_instances,ABACPolicyLoader.get_permission("Entry", permissions))
        return ABACPolicy(entities, permissions, attribute_declarations, attribute_instances, pa_relation, aa_relation) #returns a completed policy object      