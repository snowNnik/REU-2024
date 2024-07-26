# REU-2024
REU 2024
Input files can be ran in a terminal using the commmand "python main.py input_file.txt". Try it out by running:
    "python main.py Base_Case_Input.txt"
The input file must give commands to main.py. The options for commands can be see in the function "execute_command".
The most important command to give main.py is load-policy. More details about this can be seen in the execute_command function.
load-policy takes a policy txt file. Policy txt files must have very specific structures. Generally they specify attributes on the first line (ATTRS =), permission objects on the second line (PERMS =), permission-attribute relations on the third line(PA =), entity objects on the fourth line (ENTITIES =), and object-attribute relations on the fourth line (AA =). 

ATTRS line should include <String, userName>;<String,exclusionZone>;<String,ownedBy> at least, and any additional attributes can be added as needed. Attributes are styled in the format <datatype, name> with semicolons in between. 

PERMS line should only include <Entry>; <nonEntry>. This line's inclusion was not totally necessary as we could code in the assumed presence of these objects, but we left it in with the intention of keeping our codebase very general in the case of future features being added.

PA line should include all Entry and nonEntry requirements for every grid space. This line is what ties grid space to permissions. It does it in a sort of roundabout way by connecting username as an attribute to Entry. It contains entries formatted as "PARelations". For example "<userName, Grid0x0> : Entry" specifies that the grid space at location 0x0 can always be entered. Multiple attributes in a PARelation should be separated by semicolons(;). We note that this system is very precarious and it would be better practice to have a more specific attribute declaration such as "gridUsername" to prevent a drone from proclaiming its username "Grid0x0" and thereby allowing itself access to every grid space. Remember that our ABAC paradigm puts all attributes of resource(grid space), user(drone), and ENV(environment) into an undifferentiated bag to compare against every entry relation. nonEntry will follow the same format as Entry, but keep in mind that nonEntry will always be checked first, and if it comes up positive then the Entry check will be skipped entirely. Different PARelation entries should be separated by dashes(-).

ENTITIES line should include the <Drone> and all of the gridspaces formatted as <GridROWxCOL> where ROW is row number and COL is col number. Just by convention we usually add <ENV> but we never made use of that feature. Entities should be separated by semicolons(;).

AA line includes all of the relations between objects(such as <Drone>, <Grid0x0>) and their attributes, formated as AARelations. For example a drone and its attributes would be formatted as <userName, Drone>; <classification, Civilian> : <Drone>. Every grid must have a username specified, and the username attribute must be styled the same as its object name. For example object <Grid0x0> must have the attribute specified <userName, Grid0x0>. Additional attributes can be added as needed, separated by semicolons(;). Different AARelations are separated by dashes(-)

The exclusionZone attribute is a hardcoded in feature. To add an exclusion zone to a grid space, it must be included as an attribute of that particular zone in its AARelation. It is formatted <exclusionZone, #!options> where number is a whole number that specifies the radius of the exclusion zone. "options" can be a name such as "Government" which would cause only drones with the attribute <ownedBy, Government> to enter. Setting options to "D" as in <exclusionZone, 3!D> causes a nonEntry PARelation to be added with the grids' username, which means no drone will be able to enter the zone, no matter what attributes they hold. 

The ownedBy attribute is a hardcoded feature to enable our exclusionZone implementation.