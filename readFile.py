class readFile:
    
    # Takes line with the format <XXXXX>; <XXXXX>; <XXXXX>;<XXXXX> and process them into lists
    # in the format of [<XXXXX>, <XXXXX>, <XXXXX>, <XXXXX>]
    def processRaw(self, line):
        raw_list = line.split(';')
        raw_list = [x.strip() for x in raw_list]
        return raw_list

    def readAttributeCategories(self, line):
        categories_raw = self.processRaw(line)
        print(categories_raw)

    def readPermissions(self, line):
        permissions_raw = self.processRaw(line)
        print(permissions_raw)
    
    def readEntities(self, line):
        entities_raw = self.processRaw(line)
        print(entities_raw)

    def getCategory(self, category_name, categories_list):
        print(category_name)

    def readAttributeInstances(self, line, categories_list):
        print(line)

    def getPermission(self, permission_name, permissions_list):
        print(permission_name)

    def getEntity(self, entityName, entity_list):
        print(entityName)

    def readPA(self, line, permissions_list, categories_list, instances_list):
        print(line)

    def mergeLists(self, list1, list2):
        for x in list1:
            if x not in list2:
                list2.append(x)
        return list2
    
    def readAA(self, line, entities_list, categories_list, instances_list):
        print(line)
    
    def loadABACPolicy(self, file_name): 
        entities = None
        categories = None
        instances = None
        permissions = None
        paRelation = None
        aaRelation = None

        with open(file_name, "r") as file:
            for line in file:
                direction = line.split("=")
                direction[0] = direction[0].strip()
                direction[1] = direction[1].strip()
                match direction[0]:
                    case "ATTRS": categories = self.readAttributeCategories(direction[1])
                    case "PERMS" : permissions = self.readPermissions(direction[1])
                    case "ENTITIES": entities = self.readEntities(direction[1])
                    case "PA": paRelation = self.readPA(direction[1], permissions, categories, instances)
                    case "AA": aaRelation = self.readAA(direction[1], entities, categories, instances)


reader = readFile()

reader.loadABACPolicy('input/Example-ASU.txt')
