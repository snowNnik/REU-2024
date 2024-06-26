from typing import List


class PARelationEntry:
    def __init__(self, permission, attributes):
        self.permission = permission
        self.attributes = attributes

    def __str__(self):
        builder = []
        for attribute in self.attributes:
            builder.append(str(attribute))
            builder.append(", ")
        builder.append(": ")
        builder.append(str(self.permission))
        builder.append(";")
        return "".join(builder)
