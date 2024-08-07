from typing import List

class PARelation:
    def __init__(self):
        #creates an empty dictionary which will have it's keys be the names of properties which the user is trying to enter, which will access another dictionary whose keys
        #are the different permissions associated with the property like Entry and nonEntry which hold the attributes associated with those permsions
        self.relation_table = {}

    def add_relation_entry(self, permission, instances):
        entries = self.relation_table 
        if(not(str(instances[0].get_value()) in entries.keys())):#if the username of the property isn't already a keyin the dictionary then create an empty dictionary with that as
            #its key
            entries[str(instances[0].get_value())] = {}
        if(not(permission in entries[str(instances[0].get_value())].keys())):#if the permission is not already a key under the gridspace's username then create an empty list
            #in the nested dictionary with the permission as it's key
            entries[str(instances[0].get_value())][permission] = []
        entries[str(instances[0].get_value())][permission].append(instances) #add the instaces to the list inside the dictionary where the permissions are keys inside the dictonary where
        #the usernames of grid spaces are keys

    def get_entries(self, permission,Gridpos,col=None):
        if col is None:
            if(Gridpos in self.relation_table.keys()):
                if(permission in self.relation_table[Gridpos].keys()):
                   return self.relation_table[Gridpos][permission]
                else:
                    return None
            else:
                return None
        else:
            if("Grid"+str(Gridpos)+"x"+str(col) in self.relation_table.keys() ):
                if(permission in self.relation_table["Grid"+str(Gridpos)+"x"+str(col)].keys()):
                    return self.relation_table["Grid"+str(Gridpos)+"x"+str(col)][permission]
            else:
                return None
    def get_dictionary(self):
        entries = self.relation_table
        return entries
    # unsure if correct, not completely sure what the purpose of this function is.
    def are_related(self, permission, attributes):
        entries = self.relation_table.get(permission.get_name())
        if entries is None:
            return False
        for entry in entries:
            entry.sort()
            attributes.sort()
            if entry == attributes:
                return True
        return False

    def __str__(self):
        builder = []
        for key in self.relation_table.keys():
            for entry in self.relation_table[key]:
                builder.append(str(entry))
                builder.append("\n")
        return "".join(builder)

    # might just be completely broken
    def remove_attribute_from_entry(self, permission, attribute):
        entries = self.relation_table.get(permission.get_name())
        if entries is None:
            return
        removable_entries = []
        for entry in entries:
            if attribute in entry:
                entry.remove(attribute)
            if len(entry) == 0:
                removable_entries.append(entry)
        for entry in removable_entries:
            entries.remove(entry)
        if len(entries) == 0:
            del self.relation_table[permission.get_name()]

    #TODO
    def remove_attribute_from_all_entries(self, attribute):
        for key in self.relation_table.keys():
            entries = self.relation_table[key]
            removable_entries = []
            for entry in entries:
                if attribute in entry.attributes:
                    entry.attributes.remove(attribute)
                if len(entry.attributes) == 0:
                    removable_entries.append(entry)
            for entry in removable_entries:
                entries.remove(entry)
            if len(entries) == 0:
                del self.relation_table[key]


    def remove_relation_entries(self, permission):
        del self.relation_table[permission.get_name()]