'''
Created on Jan 10, 2021

@author: matt0
'''

import random
import math
from operator import itemgetter
from pip._vendor.msgpack.fallback import xrange

PUZZLE_TYPE = 8
MAT_SIZE = int(math.sqrt(PUZZLE_TYPE + 1))

class PriorityQueue(object):

    def __init__(self):
        self.elements = []
        self.max_elements = 0

    def get_max_elements(self):
        return self.max_elements
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, h=0, g=0, priority=0):
        self.elements.append((priority, h, g, item))
        self.elements.sort(key=itemgetter(0))
        self.max_elements = self.max_elements if self.max_elements > len(self.elements) else len(self.elements)

    def get_item(self):
        return self.elements.pop(0)

class Problem(object):

    def __init__(self, initial_state=None):
        self.initial_state = initial_state
        self.goal_state = self.get_goal()
        self.explored = []

    def goal_test(self, node):
        self.explored.append(node)
        return node == self.goal_state

    def get_level(self):
        return len(self.explored);

    def is_explored(self, node):
        return node in self.explored

    def get_current_state(self):
        return self.initial_state

    def get_goal_state(self):
        return self.goal_state

    def get_goal(self):
        goal = []
        goal.append(-1)
        for x in xrange(1, PUZZLE_TYPE + 1):
            goal.append(x)
        
        return goal

    def print_current_board(self):
        print_board(self.initial_state)


"""
Print the current state of board
"""
def print_board(mat):
    print("\nBoard:")
    print( "*" * 5 * MAT_SIZE)
    for index, val in enumerate(mat):
        if (index + 1) % MAT_SIZE == 0:
            print(val if val != -1 else "x")
        else:
            print(val) if val != -1 else "x", " ",
    print("*" * 5 * MAT_SIZE)
    return

"""
Check if move up operation is possible
"""
def can_move_up(mat):
    return True if mat.index(-1) >= MAT_SIZE else False

"""
Check if move down operation is possible
"""
def can_move_down(mat):
    return True if mat.index(-1) < PUZZLE_TYPE + 1 - MAT_SIZE else False

"""
Check if move left operation is possible
"""
def can_move_left(mat):
    return False if mat.index(-1) % MAT_SIZE == 0 else True

"""
Check if move right operation is possible
"""
def can_move_right(mat):
    return False if mat.index(-1) % MAT_SIZE == MAT_SIZE - 1 else True

"""
Performs the move up operation
"""
def move_x_up(mat):
    if can_move_up(mat):
        index = mat.index(-1)
        mat[index - MAT_SIZE], mat[index] = mat[index], mat[index - MAT_SIZE]
        return mat
    return None

"""
Performs the move down operation
"""
def move_x_down(mat):
    if can_move_down(mat):
        index = mat.index(-1)
        mat[index + MAT_SIZE], mat[index] = mat[index], mat[index + MAT_SIZE]
        return mat
    return None

"""
Performs the move left operation
"""
def move_x_left(mat):
    if can_move_left(mat):
        index = mat.index(-1)
        mat[index - 1], mat[index] = mat[index], mat[index - 1]
        return mat
    return None

"""
Performs the move down operation
"""
def move_x_right(mat):
    if can_move_right(mat):
        index = mat.index(-1)
        mat[index + 1], mat[index] = mat[index], mat[index + 1]
        return mat
    return None

"""
General search algorithm
"""
def general_search(problem, queueing_func):
    nodes = PriorityQueue()
    nodes.put(problem.get_current_state())
    while not nodes.empty():
        entire_node = nodes.get_item()
        node = entire_node[3]
        if problem.goal_test(node): 
            return entire_node[2], problem.get_level()
        queueing_func(nodes, expand(entire_node, problem))
        
    
"""
Expands the current node using all the operators and returns the queue.
"""
def expand(node, problem):
    all_nodes = PriorityQueue()
    node1 = move_x_up(node[3][:])
    node2 = move_x_down(node[3][:])
    node3 = move_x_left(node[3][:])
    node4 = move_x_right(node[3][:])
    if node1 and not problem.is_explored(node1):
        all_nodes.put(node1, 0, node[2] + 1, 0)
    if node2 and not problem.is_explored(node2):
        all_nodes.put(node2, 0, node[2] + 1, 0)
    if node3 and not problem.is_explored(node3):
        all_nodes.put(node3, 0, node[2] + 1, 0)
    if node4 and not problem.is_explored(node4):
        all_nodes.put(node4, 0, node[2] + 1, 0)
    return all_nodes


"""
Calculates the heuristic using the misplaced tile.
"""
def calculate_misplaced(node):
    count = 0
    for i in xrange(PUZZLE_TYPE):
        if i+1 != node[i+1]:
            count += 1
    return count

"""
Calculates the heuristic using the manhattan distance.
"""
def manhattan_distance(node):
    count = 0
    for i in xrange(1,PUZZLE_TYPE+1):
        index = node.index(i)
        row_diff = abs((i / MAT_SIZE) - (index / MAT_SIZE))
        col_diff = abs((i % MAT_SIZE) - (index % MAT_SIZE))
        count += (row_diff + col_diff)
    return count

"""
Calculates the heuristic using linear conflict and the manhattan distance.
"""
def linear_manhattan_distance(node):
    count = 0
    for i in xrange(1,PUZZLE_TYPE+1):
        index = node.index(i)
        row_diff = abs((i / MAT_SIZE) - (index / MAT_SIZE))
        col_diff = abs((i % MAT_SIZE) - (index % MAT_SIZE))
        count += (row_diff + col_diff)

    for i in xrange(1,PUZZLE_TYPE+1):
        index = node.index(i)
        row_diff = abs((i / MAT_SIZE) - (index / MAT_SIZE))
        col_diff = abs((i % MAT_SIZE) - (index % MAT_SIZE))
        if (row_diff == 0 and col_diff != 0): #correct row
            for col in range(i % MAT_SIZE + 1, MAT_SIZE):
                if index > node.index(i + col):
                    count += 2
        elif (col_diff == 0 and row_diff != 0): #correct col
            for row in range(i // MAT_SIZE + 1, MAT_SIZE):
                if index > node.index(i % MAT_SIZE + (row * MAT_SIZE)):
                    count += 2

            

    return count


"""
Queueing function for Misplaced Tile Heuristic.
"""
def misplaced_tile_heuristic(nodes, new_nodes):
    while not new_nodes.empty():
        node = new_nodes.get_item()
        nodes.put(node[3], calculate_misplaced(node[3]), node[2], calculate_misplaced(node[3]) + node[2])

"""
Queueing function for Manhattan Distance Heuristic.
"""
def manhattan_distance_heuristic(nodes, new_nodes):
    while not new_nodes.empty():
        node = new_nodes.get_item()
        nodes.put(node[3], manhattan_distance(node[3]), node[2], manhattan_distance(node[3]) + node[2])

"""
Queueing function for Linear Conflict + Manhattan Distance Heuristic.
"""
def linear_manhattan_distance_heuristic(nodes, new_nodes):
    while not new_nodes.empty():
        node = new_nodes.get_item()
        nodes.put(node[3], linear_manhattan_distance(node[3]), node[2], linear_manhattan_distance(node[3]) + node[2])



if __name__ == "__main__":
    
    #opening file for results
    fo = open("results.txt","w")

    fo.write("{:d} Puzzle Results\n".format(PUZZLE_TYPE))
    fo.write("_"*201 + "\n")
    fo.write("|  index  | {:^28s} | {:^10} | {:^10} | {:^10} | {:^10} | {:^10} | {:^10} |\n".format("Puzzle","H1: Misplaced Steps", "H1: Misplaced Expanded", "H2: Manhattan Steps", "H2: Manhattan Expanded", "H3: Linear + Manhattan Steps", "H3: Linear + Manhattan Expanded"))

    #creating random puzzle
    #repeating heuristics for x random puzzles
    for k in range(10):
        #generate puzzle
        mat = []
        mat.append(-1)
        for i in range(1,PUZZLE_TYPE+1):
            mat.append(i)
        random.shuffle(mat)

        #check solvability before inputting into algorithms, only solvable if count is even
        count = 0
        for i in range(PUZZLE_TYPE+1):
            for j in range(i,PUZZLE_TYPE+1):
                if(mat[i] != -1):
                    if(mat[i] > mat[j] and mat[j] != -1):
                        count +=1
        while(count % 2 != 0):
            random.shuffle(mat)
            count = 0
            for i in range(PUZZLE_TYPE+1):
                for j in range(i,PUZZLE_TYPE+1):
                    if(mat[i] != -1):
                        if(mat[i] > mat[j] and mat[j] != -1):
                            count +=1

        #starting the algorithms
        h1 = Problem(mat)
        h2 = Problem(mat)
        h3 = Problem(mat)
        depth1,level1 = general_search(h1, misplaced_tile_heuristic)
        depth2,level2 = general_search(h2, manhattan_distance_heuristic)
        depth3,level3 = general_search(h3,linear_manhattan_distance_heuristic)

        print(k)

        fo.write("|{:^9d}| {:^12s} | {:^19} | {:^22} | {:^19} | {:^22} | {:^28} | {:^31} |\n".format(k,str(mat),depth1,level1,depth2,level2,depth3,level3))

    


    fo.close()
