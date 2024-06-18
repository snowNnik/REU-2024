from user import User
from zone import Zone

def main():
    # Base testcases
    # Testing if the user is allowed into a zone with exact matching attributes. Expect True.
    user_attributes = {"color": "blue", "weight": 10}
    user = User(user_attributes)
    zone_attributes = {"color": "blue", "weight": 10}
    zone = Zone(0, 0, zone_attributes)
    print("If matching attributes:", user.isAllowed(zone), ". Expected True.")

    # Testing if the user is allowed into a zone when the zone has one extra attribute. Expect False.
    zone.addAttributes({"height": 11})
    print("Missing attribute:", user.isAllowed(zone), ". Expected False.")

    # Testing if the user is allowed into a zone when the attributes are there, but mismatching. Expect False.
    user.addAttributes({"height": 12})
    print("Mismatching attribute:", user.isAllowed(zone), ". Expected False.")

    # Testing if the user is allowed into a zone when the user has more attributes. Expect True.
    user.addAttributes({"height": 11, "glasses": "yes"})
    print("User has an extra attribute:", user.isAllowed(zone), ". Expected True.")

    height = 10
    width =  10
    matrix = [[None]*width]*height
    for r in range(height):
        for c in range(width):
            matrix[r][c] = Zone(r, c)

if __name__ == "__main__":
    main()