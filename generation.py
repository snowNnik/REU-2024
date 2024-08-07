import random

# 14 possible generic attributes. Only ~5 attributes are used in one file, taken by random sample
# Attribute instances are always either just 1 or 0. 
# PA is generated by picking 2 random attributes(from the ~5) per grid tile. Those 2 attributes as assigned to the grid tile with
# a random instance value of either 1 or 0.
# For AA, the drone is given all ~5 attributes with values set to 0. 
possible_attrs = ["size", "noise_level", "weight", "attr1", "attr2", "attr3", "attr4", "attr5", "attr6", "attr7", "attr8", "attr9", "attr10", "attr11", "attr12", "attr13", "attr14"]

def generateGridNames(row, col):
    names = []
    for r in range(row):
        for c in range(col):
            names += ["<Grid" + str(r) + "x" + str(c) + ">"]
    return names
                      
def generateAttributes(list_attributes):
    line = "ATTRS  = <String, userName>; <String, exclusionZone>; <String, droneOwnedBy>;"
    for attr in list_attributes:
        line += "<String, " + str(attr) + ">;"
    return line[:-1] 

def generatePermissions():
    return "PERMS = <Entry>; <nonEntry>"

def generatePAs(row, col, attrs):
    pA = "PA = "
    names = generateGridNames(row, col)
    for name in names:
        leave = random.randint(0, 10)
        curr_attrs = random.sample(attrs, k=1)
        pA += "<userName, " + str(name[1:-1]) + ">;"
        for attr in curr_attrs:
            if leave < 7:
                continue
            random_num = random.randint(0, 1)
            pA += "<" + str(attr) + ", " + str(random_num) + ">;"
        pA = pA[:-1] + " : Entry - "
    pA = pA[:-2]
    return pA

# Give the Drone all 10 attributes. All 0.
def generateAAs(row, col, attrs):
    aA = "AA = " 
    for attr in attrs:
        aA += "<" + str(attr) + ", " + str(0) + ">;"
    aA = aA[:-1] + " : <Drone> - "
    names = generateGridNames(row, col)
    for name in names:
        aA += "<userName, " + str(name[1:-1])  + "> : " + name + " - "
    aA = aA[:-2]
    return aA

def generateEntities(row, col):
    line = "ENTITIES = <Drone>;"
    names = generateGridNames(row, col)
    for name in names:
        line += str(name) + ";"
    return line + "<ENV>"

attrs = random.sample(possible_attrs, k=5)
row = 15
col = 30

f = open("outfile.txt", "w")
f.write(generateAttributes(attrs) + "\n")
f.write(generatePermissions() + "\n")  
f.write(generatePAs(row, col, attrs) + "\n")
f.write(generateEntities(row, col) + "\n")
f.write(generateAAs(row, col, attrs))
f.close()