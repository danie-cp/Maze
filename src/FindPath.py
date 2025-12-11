#######################################################
#### MazeGame uses a grid of rows X cols to demonstrate
#### pathfinding using A*.
#######################################################
import tkinter as tk
from queue import PriorityQueue, Queue, Empty
import threading
import copy


######################################################
#### A cell stores f(), g() and h() values
#### A cell is either open or part of a wall
######################################################

class Cell:
    #### Initially, arre maze cells have g() = inf and h() = 0
    def __init__(self, x, y, is_wall=False):
        self.x = x
        self.y = y
        self.is_wall = is_wall
        self.g = float("inf")
        self.h = 0
        self.f = float("inf")
        self.parent = None
        

    #### Compare two cells based on their evaluation functions
    def __lt__(self, other):
        return self.f < other.f


######################################################
# A maze is a grid of size rows X cols
######################################################
class MazeGame:
    def __init__(self, root, maze):
        self.root = root
        self.maze = maze
        
        self.rows = len(maze)
        self.cols = len(maze[0])

        #### Start state: (0,0) or top left        
        self.agent_pos = (0, 0)
        
        #### Goal state:  (rows-1, cols-1) or bottom right
        self.goal_pos = (self.rows - 1, self.cols - 1)
        
        self.cells = [[Cell(x, y, maze[x][y] == 1) for y in range(self.cols)] for x in range(self.rows)]
        
        #### The maze cell size in pixels
        self.cell_size = 15
        self.canvas = tk.Canvas(root, width=self.cols * self.cell_size, height=self.rows * self.cell_size, bg='white')
        self.canvas.pack()

        self.draw_maze()

        # x,y for drawing 
        self.draw_x = None
        self.draw_y = None

        # create dummy maze that does not affect main maze 
        self.dummy_maze = copy.deepcopy(self.maze)
    
        # right click to draw obstacles
        self.canvas.bind("<B1-Motion>", self.draw_obstacles)  
        # left click to erase obstacles
        self.canvas.bind("<B3-Motion>", self.erase_obstacles)

        self.queue = Queue()
        self.delivery_order = []
        self.current_index = 0
        self.step = 1
        self.delivery_algorithm = "A*"
        self.root.after(100, self.process_updates)

        self.deliveries_reached = 0


    def draw_maze(self):
        for x in range(self.rows):
            for y in range(self.cols):
                match self.maze[x][y]:
                    case 1:
                        color = 'black'          #Wall
                    case 0: 
                        color = 'white'          #Hallway
                    case 2:
                        color = 'grey'           #Admissions
                    case 3:
                        color = 'red'            #General Ward
                    case 4:
                        color = 'yellow'         #Emergency
                    case 5: 
                        color = 'lightblue'      #Maternity Ward
                    case 6: 
                        color = 'pink'           #Surgical Ward
                    case 7:
                        color = 'darkgreen'      #Oncology
                    case 8:
                        color = 'brown'          #ICU
                    case 9: 
                        color = 'indigo'         #Isolation Ward
                    case 10:
                        color = 'lime green'     #Pediatric Ward
                    case 11:
                        color = 'purple'         #Burn Ward
                    case 12:
                        color = 'orange'         #Hematology 
                    case 13:
                        color = 'olive drab'          #Medical Ward
                
                self.canvas.create_rectangle(y * self.cell_size, x * self.cell_size, (y + 1) * self.cell_size, (x + 1) * self.cell_size, fill=color)


    ############################################################
    #### Manhattan distance
    ############################################################
    def heuristic(self, pos):
        return (abs(pos[0] - self.goal_pos[0]) + abs(pos[1] - self.goal_pos[1]))
    
    # Calls find_path in a separate thread
    def start_find_path(self, start, goal, delivery_algorithm="A*"):
        threading.Thread(target=self.find_path, args=(start, goal, delivery_algorithm), daemon=True).start()

    # Works with the queue to determine further actions
    def process_updates(self):
        try:
            while True:
                update = self.queue.get_nowait()
                if update == "Done":
                    print("Goal reached!")

                    #tracks how many deliveries were successfully reached
                    self.deliveries_reached -= 1

                    # Reconstruct the path
                    self.reconstruct_path()

                    if(self.deliveries_reached ==0):
                        print("Success: All deliveries completed")

                elif update == "Goal not reachable":
                    print("Goal not reachable from the given start location.")

                    next_goal_index = self.current_index + self.step
                    # Return if the final goal is unreachable, which prevents infinite loop
                    if next_goal_index >= len(self.delivery_order) - 1:
                        print("Final goal unreachable — deliveries terminated.")

                        if (self.deliveries_reached > 0 and self.deliveries_reached != len(self.delivery_order)-1):
                            print(f"PARTIAL SUCCESS: {self.deliveries_reached} deliveries uncompleted")
                        if (self.deliveries_reached == len(self.delivery_order)-1):
                            print("FAILURE: No deliveries completed")
                        return

                    # Increase step to skip to the next delivery location
                    self.step += 1
                    
                    # Delay next pathfinding
                    self.root.after(500, self.start_next_delivery)

        except Empty:
            pass

        # Keep polling the queue
        self.root.after(100, self.process_updates)


    def reconstruct_path(self):
        # Store drawn path to change colors later
        self.drawn_path = []
        
        # Reconstruct path without animating. The original method drew the path in reverse and without any delay between squares
        path = []
        current_cell = self.cells[self.goal_pos[0]][self.goal_pos[1]]
        while current_cell.parent:
            path.append(current_cell)
            current_cell = current_cell.parent
        path.reverse()

        # Draw each square individually and with a delay
        def draw_next(index):
            if index >= len(path) - 1:

                # Once the path is done drawing, mark the goal teal and start the next delivery
                self.canvas.create_rectangle(self.goal_pos[1] * self.cell_size, self.goal_pos[0] * self.cell_size, (self.goal_pos[1] + 1) * self.cell_size, (self.goal_pos[0] + 1) * self.cell_size, fill='teal')

                # Increment current index and reset step
                self.current_index += self.step
                self.step = 1

                for square in self.drawn_path:
                    self.canvas.itemconfig(square, fill='dark slate gray')

                self.start_next_delivery()
                return
            
            elif index >= len(path) - 2:
                drawn_end_before_goal = self.canvas.create_rectangle(self.goal_pos[1] * self.cell_size, self.goal_pos[0] * self.cell_size, (self.goal_pos[1] + 1) * self.cell_size, (self.goal_pos[0] + 1) * self.cell_size, fill='dark blue')
                # Store last drawn square before goal
                self.drawn_path.append(drawn_end_before_goal)
                
                

            cell = path[index]
            x, y = cell.x, cell.y

            drawn_cell = self.canvas.create_rectangle(y * self.cell_size, x * self.cell_size, (y + 1) * self.cell_size, (x + 1) * self.cell_size, fill='dark blue')
            
            #store drawn square
            self.drawn_path.append(drawn_cell)
            self.maze[x][y] = 15

            # Schedule next cell
            self.root.after(200, lambda: draw_next(index + 1))

        # Start animation
        draw_next(0)



    # Called once reconstruct path is complete
    def start_next_delivery(self):

        # Only pathfind if there are remaining deliveries
        if self.current_index + 1 < len(self.delivery_order):
            start = self.delivery_order[self.current_index]
            next_goal_index = self.current_index + self.step
            
            # Disregard step value if it exceeds the delivery order length
            if next_goal_index >= len(self.delivery_order) - 1:
                goal = self.delivery_order[-1]
            else:
                goal = self.delivery_order[self.current_index + self.step]

            print(f"Starting next pathfinding from {start} to {goal}")
            # Schedule find_path with a short delay to allow GUI update
            self.root.after(4000, lambda: self.start_find_path(start, goal, self.delivery_algorithm))
        else:             
            if (self.deliveries_reached >0 and self.deliveries_reached != len(self.delivery_order)):
                print(f"PARTIAL SUCCESS: {self.deliveries_reached} deliveries uncompleted")

            print("Done.")


    ############################################################
    #### Pathfinding Algorithm
    ############################################################
    def find_path(self, start, goal, delivery_algorithm):
        self.agent_pos = start
        self.goal_pos = goal

        # Marks the goal point to be reached 
        self.canvas.create_rectangle(self.goal_pos[1] * self.cell_size, self.goal_pos[0] * self.cell_size, (self.goal_pos[1] + 1) * self.cell_size, (self.goal_pos[0] + 1) * self.cell_size, fill='Fuchsia')


        #Starting location is invalid if it is out of bounds 
        if start[0] < 0 or start[0] >= self.rows or start[1] >= self.cols or start[1] <0:
            print("Invalid Start Location: Out of Bounds.")
            self.agent_pos = (23,1)
            start = (23,1)
            print("Defaults to charging point.")

        # Starting location is invalid if it is a wall cell
        if self.maze[start[0]][start[1]] == 1 or self.cells[start[0]][start[1]].is_wall:
            #Only first start location defaults to charging point if invalid 
            if (self.deliveries_reached == len(self.delivery_order)-1):
                print("Invalid Start Location: Wall Cell")
                self.agent_pos = (23,1)
                start = (23,1)
                #secondary checks if charging station is a wall 
                if (self.maze[start[0]][start[1]] == 1 or self.cells[start[0]][start[1]].is_wall):
                    print("Charging station is compromised. Change start location")
                    return
                print("Defaults to charging point.")

        # Reset g, h, f values for all cells
        for row in self.cells:
            for cell in row:
                cell.g = float("inf")
                cell.h = 0
                cell.f = float("inf")
                cell.parent = None

        # Initialize start cell
        self.cells[start[0]][start[1]].g = 0
        self.cells[start[0]][start[1]].h = self.heuristic(start)
        self.cells[start[0]][start[1]].f = self.cells[start[0]][start[1]].h

        open_set = PriorityQueue()
        open_set.put((0, self.agent_pos))

        goal_flag = False

        while not open_set.empty():
            current_cost, current_pos = open_set.get()
            current_cell = self.cells[current_pos[0]][current_pos[1]]

            if current_pos == self.goal_pos:
                # Notify main thread to draw path
                self.queue.put("Done")
                goal_flag = True
                break

            # Explore neighbors
            #### Agent goes E, W, N, and S whenever possible
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:

                new_pos = (current_pos[0] + dx, current_pos[1] + dy)

                if 0 <= new_pos[0] < self.rows and 0 <= new_pos[1] < self.cols and not self.cells[new_pos[0]][new_pos[1]].is_wall:
                
                    #### The cost of moving to a new position is 1 unit
                    new_g = current_cell.g + 1
                    
                    if new_g < self.cells[new_pos[0]][new_pos[1]].g:
                        ### Update the path cost g()
                        self.cells[new_pos[0]][new_pos[1]].g = new_g
                        
                        ### Update the heurstic h()
                        self.cells[new_pos[0]][new_pos[1]].h = self.heuristic(new_pos)
                        
                        ### Update the evaluation function for the cell n: f(n) = g(n) + h(n)
                        # Conditionally update f based on the selected algorithm
                        if delivery_algorithm == "A*":
                            self.cells[new_pos[0]][new_pos[1]].f = new_g + self.cells[new_pos[0]][new_pos[1]].h
                        else:
                            self.cells[new_pos[0]][new_pos[1]].f = new_g
                        self.cells[new_pos[0]][new_pos[1]].parent = current_cell
                        
                        #### Add the new cell to the priority queue
                        open_set.put((self.cells[new_pos[0]][new_pos[1]].f, new_pos))

        if not goal_flag:
            self.queue.put("Goal not reachable")


    ############################################################
    #### Create Obstacles
    ############################################################

    def draw_obstacles(self,event):
        #convert x,y coordinates from mouse pixel into cell size
        self.draw_x = int(event.x / self.cell_size)
        self.draw_y = int(event.y / self.cell_size)

        if 0 <= self.draw_x  < self.rows and 0 <= self.draw_y < self.cols:    
            # Set the dummy maze value to 14 and a wall
            self.dummy_maze[self.draw_y][self.draw_x] = 14
            self.cells[self.draw_y][self.draw_x].is_wall = True
             # Draw wall on the canvas
            self.canvas.create_rectangle(self.draw_x * self.cell_size, self.draw_y * self.cell_size, (self.draw_x + 1) * self.cell_size, (self.draw_y + 1) * self.cell_size, fill='darkgoldenrod')

   ############################################################
   #### Deletes Obstacles
   ############################################################

    def erase_obstacles(self,event):
         # Convert x,y coordinates from mouse pixel into cell size
        self.draw_x = int(event.x / self.cell_size)
        self.draw_y = int(event.y / self.cell_size)

        if 0 <= self.draw_x  < self.rows and 0 <= self.draw_y < self.cols:
            # Erase only when the point is a obstacle
            if self.dummy_maze[self.draw_y][self.draw_x] == 14: 
                self.cells[self.draw_y][self.draw_x].is_wall = False
                # Erases wall on the canvas and replace it with its orginal color 
                colors = {
                    0: "white",
                    1: "black",
                    2: "grey",
                    3: "red",
                    4: "yellow",
                    5: "lightblue",
                    6: "pink",
                    7: "darkgreen",
                    8: "brown",
                    9: "indigo",
                    10: "lime green",
                    11: "purple",
                    12: "orange",
                    13: "olive drab",
                    14: "darkgoldenrod",
                    15: "dark blue"
                }        
                self.canvas.create_rectangle(self.draw_x * self.cell_size, self.draw_y * self.cell_size, (self.draw_x + 1) * self.cell_size, (self.draw_y + 1) * self.cell_size, fill= colors.get(self.maze[self.draw_y][self.draw_x]))

                # If point was orginally a wall, reverts back to true 
                if self.maze[self.draw_y][self.draw_x] == 1:
                    self.cells[self.draw_y][self.draw_x].is_wall = True








