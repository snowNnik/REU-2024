from typing import List

class PARelation:
    def __init__(self):
        self.relation_table = {}

    def add_relation_entry(self, permission, instances):
        entries = self.relation_table
        if(not(str(instances[0].get_value()) in entries.keys())):
            entries[str(instances[0].get_value())] = {}
        if(not(permission in entries[str(instances[0].get_value())].keys())):
            entries[str(instances[0].get_value())][permission] = []
        entries[str(instances[0].get_value())][permission].append(instances)

    def get_entries(self, permission,Gridpos,col=None):
        if col is None:
            return self.relation_table[Gridpos][permission]
        else:
            return self.relation_table["Grid"+str(Gridpos)+"x"+str(col)][permission]
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