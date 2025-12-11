# Hospital Delivery Robot
Implements a pathfinding visualization for a delivery robot operating in a hospital. The robot moves on a 40x40 grid of the hospital, with different numerical values corresponding to each ward. Uses Tkinter for the graphical interface and the A\* or Dijkstra's algorithms to find the optimal delivery routes.

### Requirements: 

Python with Tkinter, which is typically included with Python.

### How to Run

Ensure Python is installed.

#### Clone the repository: 
The program runs with a src folder containing the core files. main.py and the input files can be found outside of the src folder.

Run main.py from your terminal. You must be in the directory of the project folder:

Windows: python main.py

Mac: python3 main.py (at least on Luke's machine this is what works)

Select an Input File: The program will prompt you in the terminal to choose an input file to define the delivery algorithm, start location, and delivery order.

Note: The goal of our program is to ensure that the robot operates optimally even when provided with invalid or incomplete input. If the specified delivery algorithm is unsupported (i.e, not A* or Dijkstra's), the robot nurse defaults to A*. Similarly, if the start location is invalid, the robot initializes at its "charging station" (defined to point (23,1)) in the map by default.

The Tkinter window will then open, show the maze maze and the pathfinding process.

### Maze Key

Different colors indicate different wards:

Value Color Area
<div style="font-size:12px;">
Black: Wall (Impassable)<br>

White: Hallway (Passable)<br>
Grey: Admissions<br>
Red: General Ward<br>
Yellow: ER (Emergency)<br>
Light: Blue Maternity Ward<br>
Pink: Surgical Ward<br>
Dark: Green Oncology<br>
Brown: ICU<br>
Indigo: Isolation Ward<br>
Lime Green: Pediatric Ward<br>
Purple: Burn Ward<br>
Orange: Hematology<br>
Green: Medical Ward<br>
Fuchsia: Current Goal Location<br>
Dark Blue: Calculated Path<br>
Teal: Reached Delivery Location<br>
Dark Goldenrod: User-drawn Obstacle
</div>

### Controls

The program allows for real-time modification of the maze while the pathfinding is active:

Left Click and Drag (<B1-Motion>): Draw obstacles (walls) onto the maze.

Right Click and Drag (<B3-Motion>): Erase user-drawn obstacles.

Note: once the program starts drawing the path on the GUI, user-drawn obstacles will not affect the outcome. User-drawn obstacles only affect the path if drawn in between pathfinding. There is a delay in between pathfinding for the user to draw walls.
This happens because the GUI and pathfinding algorithm do not happen at the same time.

### Core Functionality

1. Delivery Algorithm Selection

The pathfinding can use one of two algorithms, as specified in the input file:

A\*: Uses the Manhattan Distance as a heuristic to estimate the cost to the goal (f(n)=g(n)+h(n)).

Dijkstra's: A shortest-path algorithm based on past cost (f(n)=g(n)).

2. Location Prioritization

The delivery locations from the input file are sorted before pathfinding begins to prioritize critical wards.

Ward Value Priority
<div style="font-size:12px;">
5 (highest): ICU, ER, Oncology, Burn Ward<br>

4 (high): Surgical Ward, Maternity Ward<br>
3 (medium): Hematology, Pediatric Ward<br>
2 (low): Medical Ward, General Ward<br>
1 (lowest): Admissions, Isolation Ward
</div>

Locations with the same priority are sorted alphabetically.

Current Location Priority: If the starting position is inside a ward room with the ward's delivery location and that ward is requested multiple times on the delivery list, that delivery is moved to the top of the order.

3. Pathfinding Execution

Successful Delivery: If a path is found, it is animated, and the goal location is marked teal. The robot then proceeds to the next delivery location in the queue.

Unreachable Delivery: If a path cannot be found (e.g., due to surrounding walls or user-drawn obstacles), the delivery is skipped, and the robot attempts to find a path to the subsequent goal. The program reports this outcome in the console, and the goal remains pink.

File Structure
main.py: Contains the main maze definition, goal coordinates, DR dictionary, input file handling, and initializes the Tkinter GUI and pathfinding.

helper.py: Contains functions for parsing the input file and implementing the location prioritization logic.

FindPath.py: Implements the Cell and MazeGame classes, the A\* / Dijkstra's pathfinding logic, the heuristic function, and the maze visualization/drawing capabilities.

4. Termination Conditions:

Success: All the delivery requests are sucessfully completed

Partial Sucess: Some delivery requests are not completed due to obstacles in the pathway

Failure: None of the delivery requests are completed due to blocked pathways
