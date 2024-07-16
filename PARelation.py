from typing import List

from PARelationEntry import *


class PARelation:
    def __init__(self):
        self.relation_table = {}

    def add_relation_entry(self, permission, instances):
        entries = self.relation_table.get(permission.get_name())
        if entries is None:
            entries = []
            self.relation_table[permission.get_name()] = entries
        entries.append(PARelationEntry(permission, instances))

    def get_entries(self, permission):
        if permission.get_name() in self.relation_table.keys():
            return self.relation_table.get(permission.get_name())
        else:
            return []

    def are_related(self, permission, attributes):
        entries = self.relation_table.get(permission.get_name())
        if entries is None:
            return False
        for entry in entries:
            if entry.attributes == attributes:
                return True
        return False

    def __str__(self):
        builder = []
        for key in self.relation_table.keys():
            for entry in self.relation_table[key]:
                builder.append(str(entry))
                builder.append("\n")
        return "".join(builder)

    def remove_attribute_from_entry(self, permission, attribute):
        entries = self.relation_table.get(permission.get_name())
        if entries is None:
            return
        removable_entries = []
        for entry in entries:
            if attribute in entry.attributes:
                entry.attributes.remove(attribute)
            if len(entry.attributes) == 0:
                removable_entries.append(entry)
        for entry in removable_entries:
            entries.remove(entry)
        if len(entries) == 0:
            del self.relation_table[permission.get_name()]

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
