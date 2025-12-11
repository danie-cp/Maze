import tkinter as tk
import sys
import os
import tkinter as tk

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from FindPath import MazeGame
from helper import parse_text, prioritize_locations

# Hospital Maze
maze = [
  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 1, 5, 5, 5, 1, 5, 1, 5, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 1, 5, 5, 5, 5, 5, 5, 5, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 1, 5, 5, 5, 1, 5, 5, 5, 5, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [1, 1, 1, 1, 1, 1, 5, 1, 5, 1, 5, 5, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [1, 1, 1, 1, 5, 1, 5, 5, 5, 1, 1, 5, 1, 3, 1, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 1, 3, 1, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [1, 1, 1, 1, 5, 5, 5, 5, 5, 5, 1, 1, 1, 3, 1, 3, 3, 1, 3, 3, 1, 3, 3, 1, 1, 1, 3, 1, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [1, 1, 1, 1, 5, 5, 5, 1, 5, 5, 5, 5, 1, 3, 1, 3, 3, 1, 3, 3, 1, 3, 3, 1, 3, 1, 3, 1, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [1, 1, 1, 1, 1, 5, 5, 1, 1, 3, 3, 1, 1, 3, 1, 1, 3, 1, 3, 1, 1, 3, 1, 1, 3, 3, 3, 3, 3, 1, 0, 1, 4, 1, 4, 4, 1, 2, 1, 0],
  [1, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 1, 4, 1, 4, 4, 1, 2, 1, 0],
  [1, 0, 0, 0, 1, 9, 1, 1, 3, 1, 3, 1, 1, 3, 3, 3, 1, 1, 1, 3, 1, 3, 1, 3, 3, 1, 3, 1, 1, 1, 0, 1, 1, 1, 4, 4, 1, 1, 1, 0],
  [1, 0, 0, 0, 1, 9, 9, 1, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 1, 3, 1, 3, 1, 3, 3, 1, 3, 1, 9, 9, 0, 4, 4, 1, 4, 4, 1, 2, 2, 0],
  [1, 0, 0, 0, 1, 1, 1, 1, 1, 3, 3, 3, 1, 3, 3, 3, 1, 3, 1, 3, 1, 3, 1, 3, 3, 1, 3, 1, 9, 1, 0, 1, 1, 1, 4, 4, 1, 2, 1, 0],
  [1, 0, 0, 0, 0, 1, 9, 9, 1, 1, 1, 3, 1, 3, 3, 3, 1, 1, 1, 3, 1, 3, 1, 3, 3, 1, 3, 1, 9, 1, 0, 4, 4, 1, 4, 4, 1, 2, 1, 0],
  [1, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 9, 1, 0, 1, 1, 1, 4, 4, 1, 2, 2, 0],
  [1, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 3, 1, 3, 1, 4, 1, 9, 9, 1, 0, 4, 4, 4, 4, 4, 1, 1, 1, 0],
  [1, 0, 0, 0, 0, 1, 7,1, 1, 1, 3, 1, 3, 1, 3, 1, 11,1, 3, 3, 1, 3, 1, 3, 4, 4, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 2, 2, 0],
  [1, 0, 0, 0, 0, 1, 7,1, 7,1, 3, 1, 3, 1, 3, 1, 11,1, 1, 1, 1, 1, 1, 3, 1, 4, 1, 4, 4, 4, 0, 1, 8, 1, 2, 2, 2, 2, 1, 0],
  [1, 0, 0, 0, 0, 1, 7,7,7,1, 1, 1, 1, 1, 1, 1, 11,11,11,1, 3, 3, 3, 3, 1, 4, 1, 4, 4, 4, 0, 8, 8, 1, 1, 1, 1, 1, 1, 0],
  [1, 0, 0, 0, 0, 1, 7,1, 7,1, 11,11,11,11,11,11,11,1, 1, 1, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 0, 1, 8, 8, 8, 8, 8, 8, 1, 0],
  [1, 0, 0, 0, 0, 1, 7,1, 7,1, 11,11,11,11,11,11,11,1, 3, 3, 3, 3, 1, 3, 1, 9, 1, 7,7,1, 0, 1, 8, 1, 8, 8, 8, 8, 1, 0],
  [1, 0, 0, 0, 0, 1, 7,1, 7,1, 11,1, 1, 1, 1, 11,1, 1, 1, 1, 1, 1, 1, 3, 1, 9, 1, 7,1, 1, 0, 1, 1, 1, 8, 1, 1, 1, 1, 0],
  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 8, 1, 0],
  [1, 0, 0, 0, 0, 0, 1, 9, 1, 7, 1, 1, 2, 1, 1, 1, 1, 1, 12, 1, 1, 1, 1, 0, 1, 1, 6, 1, 1, 1, 0, 0, 1, 8, 8, 8, 8, 8, 1, 0],
  [1, 1, 1, 1, 0, 0, 1, 9, 1, 7,1, 2, 2, 2, 2, 1, 12,12,12,12,12,12,1, 0, 1, 6, 6, 6, 1, 7, 7, 1, 1, 1, 1, 1, 1, 1, 1, 0],
  [0, 0, 0, 1, 0, 0, 1, 1, 1, 7,1, 1, 1, 2, 2, 1, 12,12,12,12,1, 1, 1, 0, 1, 6, 1, 6, 1, 7, 7, 1, 7, 7, 1, 7, 7, 1, 0, 0],
  [0, 0, 0, 1, 0, 0, 1, 7,7,7,7,7,1, 2, 2, 1, 12,12,12,12,1, 10,10, 0, 6, 6, 6, 6, 1, 1, 7, 1, 7, 1, 1, 7, 7, 1, 0, 0],
  [0, 0, 0, 1, 0, 0, 1, 1, 1, 7,1, 7,1, 1, 1, 1, 12,12,12,12,1, 10,10, 0, 1, 6, 1, 6, 1, 7, 7, 7, 7, 7, 7, 7, 7, 7, 0, 0],
  [0, 0, 0, 1, 0, 0, 1, 7,7,7,1, 7,1, 10,10,1, 12,12,12,12,1, 10,1, 0, 1, 6, 1, 6, 1, 1, 7, 7, 7, 7, 7, 7, 7, 1, 0, 0],
  [0, 0, 0, 1, 0, 0, 1, 7,7,7,1, 1, 1, 10,10,1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 7, 7, 7, 7, 7, 7, 7, 7, 1, 0, 0],
  [0, 0, 0, 1, 0, 0, 7, 7,7,7,1, 10,1, 10,10,10,10,10,1, 10,1, 10,1, 0, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
  [0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 10,1, 1, 10,10,10,1, 1, 10,1, 10,1, 0, 1, 1, 6, 6, 6, 6, 6, 6, 6, 6, 1, 6, 6, 1, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 1, 0, 0],
  [0, 0, 0, 1, 0, 1, 7,1, 1, 10,1, 10,1, 10,1, 10,1, 10,1,10, 1, 10,1, 10,1, 6, 1, 13,1, 6, 1, 13,1, 6, 1, 6, 1, 1, 0, 0],
  [0, 0, 0, 1, 0, 1, 7,1, 10,10,1, 10,1, 10,10,10,1, 10,10,10,10,10,1, 10,1, 6, 1, 13,1, 1, 1, 13,1, 6, 6, 6, 6, 1, 0, 0],
  [0, 0, 0, 1, 0, 1, 1, 1, 10,10,1, 10,10,1, 1, 10,1, 10,1, 1, 1, 10,1, 10,1, 6, 1, 13,13,1, 13,13,1, 6, 6, 6, 6, 1, 0, 0],
  [0, 0, 0, 1, 0, 0, 0, 1, 10,10,1, 10,10,1, 10,10,1, 10,10,1, 10,10,1, 10,1, 6, 1, 13,13,1, 13,13,1, 6, 6, 6, 6, 1, 0, 0],
  [0, 0, 0, 1, 9, 1, 1, 1, 10,10,1, 10,10,1, 10,10,1, 10,10,1, 10,10,1, 10,1, 6, 1, 13,13,13,13,13,1, 6, 6, 6, 6, 1, 0, 0],
  [0, 0, 0, 1, 9, 9, 9, 1, 10,10,1, 10,10,1, 10,10,1, 10,10,1, 10,10,1, 10,1, 6, 1, 13,13,13,13,13,1, 6, 6, 6, 6, 1, 0, 0],
  [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0]
]

# Dictionary for starting points in each ward
goals = {
    "Admissions": [25,13],
    "General Ward": [12,15],
    "ER": [11,34],
    "Maternity Ward": [5,7],
    "Surgical Ward": [37,34],
    "Oncology": [28,31],
    "ICU": [21,34],
    "Isolation Ward": [38,4],
    "Pediatric Ward": [29,13],
    "Burn Ward": [19,13],
    "Hematology": [25,18],
    "Medical Ward": [38,28]
}

# Dictionary to specify the cells of the ward room with the delivery location inside of it 
# (some wards have multiple rooms with only one room with a delivery location)
goal_rooms = {
    "Pediatric Ward": [
    (29, 13), (29, 14),
    (30, 13), (30, 14),
    (31, 13), (31, 14), (31, 15), (31, 16),(31, 17),
    (32, 14), (32, 15), (32, 16)
    ],
   "Isolation Ward":  [
    (37, 4), 
    (38, 4), (38, 5), (38, 6)
    ],
   "Oncology": [
    (24,29),(24,30),
    (25,29),(25,30),(25,32),(25,33),(25,35),(25,36),
    (26,30),(26,32),(26,35),(26,36),
    (27,29),(27,30),(27,31),(27,32),(27,33),(27,34),(27,35),(27,36),(27,37),
    (28,30),(28,31),(28,32),(28,33),(28,34),(28,35),(28,36),
    (29,29),(29,30),(29,31),(29,32),(29,33),(29,34),(29,35),(29,36)   
    ],
    "Surgical Ward": [
    (30,24), (30,25), (30,26), (30,27),
    (31,26), (31,27), (31,28), (31,29), (31,30), (31,31), (31,32), (31,33), (31,35), (31,36),
    (32,24), (32,25), (32,26), (32,27), (32,28), (32,29), (32,30), (32,31), (32,32), (32,33), (32,34), (32,35), (32,36),
    (33,25), (33,29), (33,33), (33,35), 
    (34,25), (34,33), (34,34), (34,35), (34,36),
    (35,25), (35,33), (35,34), (35,35), (35,36),
    (36,25), (36,33), (36,34), (36,35), (36,36),
    (37,25), (37,33), (37,34), (37,35), (37,36), 
    (38,25), (38,33), (38,34), (38,35), (38,36)   
    ],
   "ER": [
    (8,34), (8,35), 
    (9,34), (9,35), 
    (10,34), (10,35), 
    (11,34), (11,35), 
    (12,34), (12,35), 
    (13,34), (13,35), 
    (14,34), (14,35), 
    (15,34), (15,35),
    (16,31), (16,32), (16,33), (16,34), (16,35)
    ],
    "Admissions": [
    (23, 12), 
    (24, 11), (24, 12), (24, 13), (24, 14),
    (25, 13), (25, 14),
    (26, 13), (26, 14)
    ],
}

# Dictionary for delivery order sorting
DR_dict = {'ICU': 5, 'ER': 5, 'Oncology': 5, 'Burn Ward': 5, 'Surgical Ward': 4, 'Maternity Ward': 4, 'Hematology': 3, 'Pediatric Ward': 3, 'Medical Ward': 2, 'General Ward': 2, 'Admissions': 1, 'Isolation Ward': 1}

# Startup menu for program
while True:
    print("\nChoose input file: \n1: inputfile1.txt\n2: inputfile2.txt\n3: inputfile3.txt\n4: inputfile4.txt\n5: inputfile5.txt")
    choice = input("\nEnter 1, 2, 3, 4, or 5: ").strip()

    input_files = {
        "1": "inputfile1.txt",
        "2": "inputfile2.txt",
        "3": "inputfile3.txt",
        "4": "inputfile4.txt",
        "5": "inputfile5.txt"
    }

    input_file = input_files.get(choice)
    if not input_file:
        print("\nInvalid input, please enter 1, 2, 3, 4, or 5.")
        continue

    try:
        delivery_algorithm, start_location, delivery_locations = parse_text(input_file)
    except Exception as e:
        print(f"\nError parsing input file: {e}")
        continue

    # Process start location
    try:
        start_location = tuple(int(coord) for coord in start_location.strip().split(", "))
    except ValueError:
        print("\nInvalid start location format. Please fix the input file.")
        continue

    # Turn the delivery locations string into a list
    delivery_locations = delivery_locations.strip().split(", ")
    if not delivery_locations:
        print("\nError: No delivery locations provided. Please fix the input file.")
        continue

    # Prioritize delivery locations
    delivery_order = prioritize_locations(start_location, delivery_locations, DR_dict, goal_rooms, maze)
    if not delivery_order:
        print("\nError: No valid delivery locations found after checking DR_dict. Please fix the input file.")
        continue

    # If all checks pass, break out of the loop
    break

def start_pathfinding():
    print(delivery_order)
    ordered_points = [start_location] + [tuple(goals[name]) for name in delivery_order if name in goals]
    if len(ordered_points) < 2:
        print("Not enough valid delivery points to start pathfinding.")
        return
    print(ordered_points)

    game.delivery_order = ordered_points
    game.delivery_algorithm = delivery_algorithm
    game.current_index = 0
    start = game.delivery_order[0]
    goal = game.delivery_order[1]
    game.start_find_path(start=start, goal=goal, delivery_algorithm=delivery_algorithm)
    game.deliveries_reached = len(delivery_order)  

root = tk.Tk()
root.title("Hospital Maze")

game = MazeGame(root, maze)

root.after(3000, start_pathfinding)

root.mainloop()