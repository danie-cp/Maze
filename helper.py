import sys

def parse_text(file_name):
    try:
        with open(file_name, 'r') as file:
            content = file.read().splitlines()
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        return None, None, None
    
    #checks if file is empty
    if not content:
        raise ValueError("Input file is empty.")
    
    delivery_algorithm = content[0].removeprefix("Delivery algorithm:").strip()
    start_location = content[1].removeprefix("Start location:").strip().replace("(", "").replace(")", "")
    delivery_locations = content[2].removeprefix("Delivery locations:").strip()

    #checks if inputted data is valid
    if delivery_algorithm != "A*" and delivery_algorithm != "Dijkstra's":
        print("Invalid Delivery Algorithm. Defaults to A*")
        delivery_algorithm = "A*"

    if start_location == "":
        print("Error: Start Location not provided. Defaults to charging point")
        start_location = '23, 1'

    if not delivery_locations:
        raise ValueError("Delivery Locations not provided")

    return delivery_algorithm, start_location, delivery_locations

def prioritize_locations(start_location, locations, DR_dict, goal_rooms, maze):
    # Initial check to see if locations list is empty
    if not locations:
        return []

    p_current = False
    start = []
    c = 0

    while c < len(locations):
        if locations[c] not in DR_dict:
            print(f"Error: Delivery location {locations[c]} not found in DR_dict.")
            locations.pop(c)
        else:
            c += 1  

    # Secondary check to see if filtered locations list is empty
    if not locations:
        print("No valid delivery locations found after checking DR_dict.")
        return []

    # Sort list alphabetically
    # requests of the same ward are grouped together 
    # Different wards of the same priorityare prioritized alphabetically.
    locations.sort()

    # Using insertion sort, the requests are ordered based on priority 
    for i in range(1, len(locations)):    
        j = i - 1
        while j >= 0 and DR_dict[locations[j]] < DR_dict[locations[j + 1]]:
            locations[j], locations[j + 1] = locations[j + 1], locations[j]
            j -= 1 

    start = list(start_location)

    # Dictionary to store single-room wards
    single_room ={
    "General Ward": 3,
    "Maternity Ward": 5,
    "ICU": 8,
    "Burn Ward": 11,
    "Hematology": 12,
    "Medical Ward": 13
    }


    # Move a ward's priority to the top of the delivery list if ward has multiple requests and agent's start location is in a room with ward's delivery location
    for key, value in goal_rooms.items():
        if start_location in value and locations.count(key) > 1:
            p_current = True
            current = key
            
            
    for key, value in single_room.items():
        if value == maze[start[0]][start[1]] and locations.count(key) > 1:
            p_current = True
            current = key

    if p_current:
        count = 0
        
        while current in locations:
            locations.remove(current)
            count += 1
            
        for a in range(count):
            locations = [current] + locations

    return locations


