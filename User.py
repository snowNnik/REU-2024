from typing import List
from Entity import *


class User(Entity):
    def __init__(self, name, assigned_attributes=None):
        self.name = name
        self.assigned_attributes = assigned_attributes or []
