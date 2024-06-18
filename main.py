from user import User
from zone import Zone

def main():
    # Base testcases
    user_attributes = {"color": "blue", "weight": 10}
    user = User(user_attributes)
    zone_attributes = {"color": "blue", "weight": 10}
    zone = Zone(0, 0, zone_attributes)
    print("If matching attributes:", user.isAllowed(zone))

    zone.addAttributes({"height": 11})
    print("Missing attribute:", user.isAllowed(zone))

    user.addAttributes({"height": 12})
    print("Mismatching attribute:", user.isAllowed(zone))

    height = 10
    width =  10
    matrix = [[None]*width]*height
    for r in range(height):
        for c in range(width):
            matrix[r][c] = Zone(r, c)

    print(matrix)

if __name__ == "__main__":
    main()