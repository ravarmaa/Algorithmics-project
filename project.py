from pykkar import *
import random as rnd
import time

def generate(r,c,start, finish): # Randomized Prim's algorithm
    start = [start,start]
    tries = [[0,0], [0,1], [0,-1], [1, 0], [-1, 0]]
    lst = []
    for i in range(r):
        temp = []
        for j in range(c):
            temp.append('#')
        lst.append(temp)

    
    queue = [start]
    while queue:
        node = queue.pop(rnd.randint(0,len(queue)-1))
        if lst[node[0][0]][node[0][1]] == ' ':
            continue
        
        lst[node[0][0]][node[0][1]] = ' '
        lst[node[1][0]][node[1][1]] = ' '
        nbrs = [[0, 2], [2, 0], [0, -2], [-2, 0]]
        rnd.shuffle(nbrs)
        
        for i in range(len(nbrs)):
            
            if 0 <= node[0][0] + nbrs[i][0] <= r and 0 <= node[0][1] + nbrs[i][1] <= c:
                nbr = [node[0][0] + nbrs[i][0], node[0][1] + nbrs[i][1]]
                passage = [node[0][0] + nbrs[i][0]//2, node[0][1] + nbrs[i][1]//2]
            else:
                continue
            
            if lst[nbr[0]][nbr[1]] == '#':
                queue.append([nbr,passage])

    lst[start[0][0]][start[0][1]] = '>'

    for i in range(len(tries)):
        if lst[finish[0] + tries[i][0]][finish[1] + tries[i][1]] != '#':
            lst[finish[0] + tries[i][0]][finish[1] + tries[i][1]] = 'b'
            end = [finish[0] + tries[i][0], finish[1] + tries[i][1]]
            break

    # Getting the matrix of the map for A* and string for world generation
    
    maze = ''''''
    for i in range(len(lst)):
        lst[i].append('#')
        maze += "".join(lst[i]) + "\n"
    last_row = ['#' for i in range(c+1)]
    lst.append(last_row)
    maze += (c+1)*"#"
    return maze, lst, end

def left():
    right()
    right()
    right()
    
def turn():
    right()
    right()

def random_mouse():
    while not is_box():
        clear = []
        for i in range(4): # Gather info
            if i != 2:        
                if not is_wall() and not is_painted() and not is_cone():
                    clear.append(i)
            right()

        if len(clear) > 0: # Get random path
            go = rnd.choice(clear)
        else:
            go = 2 # If no other possibility, go back

        for i in range(go): # Turn
            right()
        step()    
            

def wall_follow(): # Wall following algorithm
    while not is_box():
        right()
        if is_wall():
            left()
        else:
            step()
            
        if is_box():
            break
        
        if is_wall():
            left()
        else:
            step()

def get_dirs():
    dirs = 0
    clear = []
    painted = []
    for i in range(4): # Gather info
        if i != 2:
            if not is_wall():
                dirs += 1
                if not is_cone():
                    if not is_painted():
                        clear.append(i)
                    else:
                        painted.append(i)
        right()

    if len(clear) > 0: # If possible, go to unvisited path
        go = rnd.choice(clear)
    elif len(painted) > 0:
        go = rnd.choice(painted)
    else:
        go = 2 # If no other possibility, go back
            
    return dirs, go
    
def Tremaux(): # Trémaux's algorithm
    last = 0
    while not is_box():
        dirs, go = get_dirs()
            
        if dirs >= 2:
            turn()
            if not is_painted() and not is_wall(): # Paint the tile behind you
                paint()
            elif is_painted() and (last > 2 or last == 0): # If already painted, put a cone
                put()
            turn()

            for i in range(go): # Turn to the next path
                right()

            if is_painted(): # If the path has been partially explored once, put cone
                put()
            else:
                paint() # Otherwise mark the first time entrance to the path
            last = 0

        else:
            for i in range(go): # Turn to the next path
                right()
            last += 1
            
        if not is_wall():
            step()
                


def H(loc, fin): # Heuristic function 
    return abs(loc[0]-fin[0]) + abs(loc[1]-fin[1])

def a_star():
    node = [H(s, end), s, 0, H(s, end)] # score, location, actual cost, heuristic
    visited = []
    queue = [node]
    dirs = [[0,1], [1,0], [0,-1], [-1,0]]
    paths = {}
    count = 0
    while node[3] > 1:
        visited.append(node[1])
        nextNodes = []
        for i in range(len(dirs)):
            nbr = info[node[1][0] + dirs[i][0]][node[1][1] + dirs[i][1]]
            if nbr == ' ' or nbr == 'b': # Get all next valid nodes, append to queue
                nextNode = [H(node[1], end) + node[3], [node[1][0] + dirs[i][0], node[1][1] + dirs[i][1]], node[2]+1, H(node[1], end)]
                if nextNode[1] not in visited and nextNode not in queue:
                    queue.append(nextNode)
                    nextNodes.append(nextNode[1])
        
        paths[count] = nextNodes            
        queue.sort()
        
        node = queue.pop(0)
        count += 1
        
    # Extract path from all visited nodes

    path = []
    last = end
    vals = list(paths.values())
    
    while True:
        path.append(last)
        if last == s:
            break
        
        for i in range(len(vals)):
            if last in vals[i]:
                nr = i
                break
            
        last = visited[nr]

    path = path[::-1]
    
    # Get movement instructions from path
    NWSE = ['N', 'W', 'S', 'E']
    dif = [[-1,0], [0,-1], [1,0], [0,1]]

    mat = [[0, 3, 2, 1],
            [1, 0, 3, 2],
            [2, 1, 0, 3],
            [3, 2, 1, 0]]

    for i in range(1,len(path)):
        d = [path[i][0]-path[i-1][0], path[i][1]-path[i-1][1]]
        row = dif.index(d)
        col = NWSE.index(get_direction())
        
        for i in range(mat[col][row]):
            right()
        step()


        
nr = 10
while True:
    while True:
        print("Insert 1 to generate.")
        print("Insert 2 to edit the maze size.")
        print("Insert 3 to edit the start/end coordinates.")
        try:
            choose = int(input("--> "))
        except:
            print("Something went wrong!\n")
            continue
        if 0 < choose < 4:
            break
        else:
            print("Invalid value, try again.\n")
            continue
        
    if choose == 2:
        while True:
            try:
                rows = int(input("Insert an even number of rows in the maze grid (2 - 20): \n"))
            except:
                print("Something went wrong!\n")
                continue
            if 2 <= rows <= 20 and rows % 2 == 0:
                break
            else:
                print("Invalid value, try again.\n")
                
        while True:
            try:
                cols = int(input("Insert an even number of collumns in the maze grid (2 - 40): \n"))
            except:
                print("Something went wrong!")
                continue
            if 2 <= cols <= 40 and rows % 2 == 0:
                break
            else:
                print("Invalid value, try again.\n")
        continue
    
    if choose == 3:
        kill = 0
        while True:
            try:
                s = list(input("Enter the start grid coordinates (odd numbers, use comma as delimiter): \n").split(','))
                s = list(map(int, s))
            except:
                print("Something went wrong!\n")
                continue
            try:
                if (0 < s[0] < rows and s[0] % 2 == 1) and (0 < s[1] < cols and s[1] % 2 == 1):
                    break
                else:
                    print("Invalid value, try again.\n")
            except:
                print("Please specify maze size.\n")
                kill = 1
                break
        if kill == 1:
            continue
        while True:
            try:
                f = list(input("Enter the end grid coordinates (odd numbers, use comma as delimiter): \n").split(','))
                f = list(map(int, f))
            except:
                print("Something went wrong!\n")
                continue
            try:
                if (0 < f[0] < rows and f[0] % 2 == 1) and (0 < f[1] < cols and f[1] % 2 == 1):
                    break
                else:
                    print("Invalid value, try again.\n")
            except:
                print("Please specify maze size.\n")
                break
        continue

    if choose == 1:
        while True:
            try:
                maze, info, end = generate(rows,cols,s,f)
                print("Generation successful!\n")
            except:
                print("Some values invalid or missing. \n")
                break

            while True:
                create_world(maze)
                set_speed(nr)
                
                while True:
                    back = 0
                    back1 = 0
                    print("Insert 1 to choose the algorithm.")
                    print("Insert 2 to choose the simulation speed (default 10).")
                    print("Insert 3 to change maze parameters.")
                    print("Insert 4 to generate new maze.")
                    print("Insert 5 to reset the maze.\n")
                    try:
                        choose2 = int(input("--> "))
                    except:
                        print("Something went wrong!")
                        continue

                    if 0 < choose2 < 6:
                        pass
                    else:
                        print("Invalid value, try again.\n")
                        continue

                    if choose2 == 1:
                        while True:
                            print("Insert 1 for random mouse algorithm.")
                            print("Insert 2 for wall following algorithm.")
                            print("Insert 3 for Trémaux's algorithm.")
                            print("Insert 4 for A* algorithm.")
                            print("Insert 5 to go back.\n")
                            try:
                                choose3 = int(input("--> "))
                            except:
                                print("Something went wrong!\n")
                                continue

                            if 0 < choose3 < 6:
                                pass
                            else:
                                print("Invalid value, try again.\n")
                                continue
                            try:
                                if choose3 == 1:
                                    random_mouse()
                                elif choose3 == 2:
                                    wall_follow()
                                elif choose3 == 3:
                                    try:
                                        Tremaux()
                                    except:
                                        print("Something went wrong!\n")
                                elif choose3 == 4:
                                    a_star()
                                else:
                                    break
                                break
                            except:
                                print("Something went wrong!\n")
                                break

                    if choose2 == 2:
                        while True:
                            print("Insert the simulation speed (1 - 10).\n")
                            nr = int(input("--> "))
                            if 0 < nr < 11:
                                set_speed(nr)
                                break
                            else:
                                print("Invalid value, try again.\n")
                                continue
                    if choose2 == 3:
                        back = 1
                        back1 = 1
                        break
                    
                    if choose2 == 4:
                        back1 = 1
                        break

                    if choose2 == 5:
                        break
                bye()
                if back1 == 1:
                    break
            if back == 1:
                break


