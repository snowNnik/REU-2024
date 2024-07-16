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

def check_permission(user_id, object_id, environment_id, permission_id, policy, row, col):
    if policy is not None:
        user = policy.get_entity(user_id)
        obj = policy.get_entity(object_id)
        permission = policy.get_permission(permission_id)
        environment = policy.get_entity(environment_id)
        monitor = ABACMonitor(policy)  # creating instance
        result = monitor.check_access(user, obj, environment, permission, row,col)
        if result:
            #print("Permission GRANTED!")
            return 1
        else:
            #print("Permission DENIED!")
            return 0
def build_grid(user_id, environment_id, permission_id, rows, columns, policy):
    if policy is not None:
        global grid 
        grid = []
        for row in range(int(rows)):
            grid.append([])
            for col in range(int(columns)):
                object_id = "Grid" + str(row) + "x" + str(col)
                grid[row].append(check_permission(user_id, object_id, environment_id, permission_id, policy,row,col))
  
def execute_command(command):
    global policy
    global path
    command_parts = command.split(" ")
    if len(command_parts) == 0:
        return
    match command_parts[0]:
        case "load-policy":
            #print(command_parts[1])
            policy = ABACPolicyLoader.load_abac_policy(command_parts[1])
        case "build-grid":
            rowsAndColums = command_parts[4].strip()[1:-1]
            rowsAndColums = rowsAndColums.split(",")
            row = int(rowsAndColums[0])
            colmun = int(rowsAndColums[1])
            build_grid(command_parts[1], command_parts[2],command_parts[3],rowsAndColums[0],rowsAndColums[1], policy)
        case "make-path":
            startPos = command_parts[1].strip()[1:-1].split(",")
            startPos = [eval(x) for x in startPos]
            destPos = command_parts[2].strip()[1:-1].split(",")
            destPos = [eval(x) for x in destPos]
            path = a_star_search(grid, startPos,destPos)
            
        case "show-policy":
            print(policy)
        case "check-permission":
            check_permission(
                command_parts[1], command_parts[2], command_parts[3], command_parts[4], policy)
        case "add-entity":
            policy.add_entity(command_parts[1])
        case "remove-entity":
            policy.remove_entity(command_parts[1])
        case "add-attribute":
            policy.add_attribute_declaration(
                command_parts[1], command_parts[2])
        case "remove-attribute":
            policy.remove_attribute_declaration(command_parts[1])
        case "add-permission":
            policy.add_permission(command_parts[1])
        case "remove-permission":
            policy.remove_permission(command_parts[1])
        case "add-attributes-to-permission":
            policy.add_permission_to_attribute(command_parts)
        case "remove-attribute-from-permission":
            policy.remove_attribute_from_permission(
                command_parts[1], command_parts[2], command_parts[3])
        case "add-attribute-to-entity":
            policy.add_attribute_to_entity(
                command_parts[1], command_parts[2], command_parts[3])
        case "remove-attribute-from-entity":
            policy.remove_attribute_from_entity(
                command_parts[1], command_parts[2], command_parts[3])
        case _:
            print(f"Unrecognized command: {command_parts[0]}", file=sys.stderr)


if __name__ == "__main__":
    command_line = " ".join(sys.argv)
    command_line = command_line[8:]
    command_line = "../REU-2024/inputs/" + str(command_line)
    commandFile = open(command_line, "r")
    commands = commandFile.read().split(";")
    policy = None
    for command in commands:
        execute_command(command.strip())
    print(' ')
    for line in grid:
        print(line)
    showGrid(grid, path)
    
