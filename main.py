import sys
# from edu.asu.cdf.cse365.abac.elements import ABACPolicy, Entity, Permission
# from edu.asu.cdf.cse365.abac.monitor import ABACMonitor
# from edu.asu.cdf.cse365.abac.utils import ABACPolicyLoader
from ABACPolicyLoader import *
from ABACMonitor import *
from ABACPolicy import *
from Permission import *
from pathing import *
from graph import *

def check_permission(user_id, object_id, environment_id, permission_id, policy, row, col):#checks whether or user-id has access to do permission on the object_id
    if policy is not None:#if policy exsists 
        user = policy.get_entity(user_id) #the user entity is retrieved
        obj = policy.get_entity(object_id)#the object entity being acted on is retrieved
        permission = policy.get_permission(permission_id)#the relevant permission is retrieved
        environment = policy.get_entity(environment_id)#the environment is retrieved
        monitor = ABACMonitor(policy)  # creating instance of ABACMonitor
        result = monitor.check_access(user, obj, environment, permission, row,col)#
        #print(result)
        if result:
            # print("Permission GRANTED!")
            return 1
        else:
            # print("Permission DENIED!")
            return 0
    else:
       raise Exception("policy not found")
def build_grid(user_id, environment_id, rows, columns, policy):#creates the grid that the drone will navigate through where a 1 symbolizes where the drone is allow to go and
    #0 represents where the drone cannot go
    if policy is not None:#
        global grid 
        grid = []
        for row in range(int(rows)):#For every row and column specified in the input file check to see if the user has permission to enter the square or not
            new_row = []
            for col in range(int(columns)):
                object_id = "Grid" + str(row) + "x" + str(col) 
                #print(policy.get_permission('nonEntry'))
                if(policy.get_pa_relation().get_entries(policy.get_permission('nonEntry') ,object_id) != None):#if nonEntry is in the PARelation's dictionary entry at the 
                    #key of ""Grid" + str(row) + "x" + str(col)"" then check to see if the drone should be denied entry before we consider whether it can enter
                    
                    nonEntry = check_permission(user_id,object_id, environment_id, 'nonEntry', policy,row,col) #check to see if there are attributes such that the user
                    #cannot enter the square
                    if nonEntry:#if there are are attributes such that prevent the user from entering the property then add 0 to the grid in place   
                        new_row.append(0)
                        continue
                if(policy.get_pa_relation().get_entries(policy.get_permission('Entry'),object_id)!= None):#if there are attributes in PARelation
                    new_row.append(check_permission(user_id, object_id, environment_id, 'Entry', policy,row,col)) #append either 1 or 0 depending on whether or not you can endter the square
                else:#ootherwise the drone isn't allowed to enter the property
                    new_row.append(0)
            grid.append(new_row)#append the row to the grid
    else:# no policy detected
        raise Exception("No Policy")
def execute_command(command):
    global policy  
    global path 
    command_parts = command.split(" ") #splits command into arguments
    if len(command_parts) == 0: #if there are no arguments execute next command
        return
    match command_parts[0]:#First arguement dictates what method to execute
        case "load-policy": #loads the Attributes, Permissions, Entities and assigns Attributes to Permissions and Entities as defined in the file 
            # load-policy policy_file.txt
            if(len(command_parts) >=2 ):
                policy = ABACPolicyLoader.load_abac_policy(command_parts[1]) #the first arguement should be the name of the file setup similar to the Example1.txt file
            else:
                raise IndexError("load-policy command does not have enough inputs")
        case "build-grid":
            # build-grid Drone_id ENV <row#,col#>  
            if(len(command_parts) >= 4):
              if(command_parts[3][0].strip() =="<" and command_parts[3][len(command_parts[3])-1].strip() ==">" and command_parts[3].__contains__(",")):
                  rowsAndColums = command_parts[3].strip()[1:-1].split(",") #grabs the number of rows and columns and separates them into into the row and column numbers to be used to build the gird
                  build_grid(command_parts[1], command_parts[2],rowsAndColums[0],rowsAndColums[1], policy)
              else:
                raise SyntaxError("The build grid command should have the syntax: \"build-grid User_Entity_name Environment_Entity_name <int,int>\" where User_Entity_name is probably the Drone and Environment_ENtity_name represents the drone")
            else:
                raise IndexError("build-grid command does not have enough inputs")
        case "make-path":
            # make-path <from_row#, from_col#> <to_row#, to_col#>
            if(len(command_parts) >= 3):
                if(command_parts[1][0].strip() =="<" and command_parts[1][len(command_parts[1])-1].strip() ==">" and command_parts[1].__contains__(",")):#checks for correct syntax
                    startPos = command_parts[1].strip()[1:-1].split(",")
                    startPos = [eval(x) for x in startPos]
                else:
                    print("SyntaxError: The make-pathcommand should have the syntax: \"make-path <int,int> <int,int>\" and the first coordinate's sytax is wrong")
                if(command_parts[2][0].strip() =="<" and command_parts[2][len(command_parts[2])-1].strip() ==">" and command_parts[2].__contains__(",")):
                    destPos = command_parts[2].strip()[1:-1].split(",")
                    destPos = [eval(x) for x in destPos]
                else:
                    print("SyntaxError: The make-path command should have the syntax: \"make-path <int,int> <int,int>\" and the second coordinate's sytax is wrong")
                try:
                    path = a_star_search(grid, startPos, destPos)
                except NameError:
                    print("main.py line 91 NameError: Either Grid the was not created properly or there was an error in start or end desitnations in make-path")
            else:
                raise IndexError("make-path command does not have enough inputs")

        case "show-policy": # UNUSED
            print(policy)
        case "check-permission": # UNUSED
            check_permission(command_parts[1], command_parts[2], command_parts[3], command_parts[4], policy)
        case "add-entity": # UNUSED
            policy.add_entity(command_parts[1])
        case "remove-entity": # UNUSED
            policy.remove_entity(command_parts[1])
        case "add-attribute": # UNUSED
            policy.add_attribute_declaration(
                command_parts[1], command_parts[2])
        case "remove-attribute": # UNUSED
            policy.remove_attribute_declaration(command_parts[1])
        case "add-permission": # UNUSED 
            policy.add_permission(command_parts[1])
        case "remove-permission": # UNUSED
            policy.remove_permission(command_parts[1])
        case "add-attributes-to-permission": # UNUSED
            policy.add_permission_to_attribute(command_parts)
        case "remove-attribute-from-permission": # UNUSED
            policy.remove_attribute_from_permission(
                command_parts[1], command_parts[2], command_parts[3])
        case "add-attribute-to-entity": # UNUSED
            policy.add_attribute_to_entity(
                command_parts[1], command_parts[2], command_parts[3])
        case "remove-attribute-from-entity": # UNUSED 
            policy.remove_attribute_from_entity(
                command_parts[1], command_parts[2], command_parts[3])
        case _:
            print(f"Unrecognized command: {command_parts[0]}", file=sys.stderr)


if __name__ == "__main__":
    command_line = " ".join(sys.argv)#Grab the command line input
    command_line = command_line[8:]# skip the main.py part of the command line command 
    command_line = "../REU-2024/inputs/" + str(command_line) #redrect to the folders
    try:
        commandFile = open(command_line, "r") # opens the file which was referenced by command line
        commands = commandFile.read().split(";") #reads the line of the file and splits it into commands (seen in the execute_command Menu) spaced out between ; See Example1_Input.txt as an example
        policy = None # holds policy for later use
        for command in commands: #for every command strip out the spaces and run execute command
            execute_command(command.strip())
        print(' ') # Space
        for line in grid: #prints each line in the girds 1s represent areas the drone can enter, 0s represent spaces the drone cannot enter 
            print(line) 
        showGrid(grid, path) #draws a grid and path of the drone in a 2D grid in a tk drawing where the green spaces represent places the drone is allowed to enter, 
        # red spaces represent where the drone is not allowed to enter and a blue represents the drone's path 
    except FileNotFoundError:
        print("main.py line 133-143 FileNotFoundError: Flie not Found")
    except NameError:
        print("main.py line 133-143 NameError: either build-grid or make-path was not called correctly")