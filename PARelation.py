# PARelation class links permissions to attribute instances.

class PARelation():
    def __init__(self):
        self.relationTable = {}

    def addRelationEntry(self, permission, instances):
        perm_name = permission.getName()
        if perm_name not in self.relationTable.keys():
            self.relationTable[perm_name] = instances
        else:
            curr_instances = self.relationTable[perm_name]
            for instance in instances:
                if instance not in curr_instances:
                    curr_instances += [instance]
            self.relationTable[perm_name] = curr_instances
        
