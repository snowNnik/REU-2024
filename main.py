import sys
# from edu.asu.cdf.cse365.abac.elements import ABACPolicy, Entity, Permission
# from edu.asu.cdf.cse365.abac.monitor import ABACMonitor
# from edu.asu.cdf.cse365.abac.utils import ABACPolicyLoader
from ABACPolicyLoader import *
from ABACMonitor import *
from ABACPolicy import *
from Permission import *


def check_permission(user_id, object_id, environment_id, permission_id, policy):
    if policy is not None:
        user = policy.get_entity(user_id)
        obj = policy.get_entity(object_id)
        permission = policy.get_permission(permission_id)
        environment = policy.get_entity(environment_id)
        monitor = ABACMonitor(policy)  # creating instance
        result = monitor.check_access(user, obj, environment, permission)
        if result:
            print("Permission GRANTED!")
        else:
            print("Permission DENIED!")


def execute_command(command):
    global policy
    command_parts = command.split(" ")
    if len(command_parts) == 0:
        return
    match command_parts[0]:
        case "load-policy":
            policy = ABACPolicyLoader.load_abac_policy(command_parts[1])
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
    commands = command_line.split(";")
    policy = None
    for command in commands:
        execute_command(command.strip())
