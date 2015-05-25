# grid size:8x8, so far 1 level only
# starting point fixed at 1,1
# ending point fixed at 6,6
# 1 definite correct route. with 5 turning points (empty space)
# type in 'up', 'down', 'left', 'right', or 'end' to control
# 'end' ends the game

# touching an obstacle restarts the game (go back to starting point)
# infinite loops restart game too

# arrow signs:
#   "U" = UP
#   "D" = DOWN
#   "L" = LEFT
#   "R" = RIGHT

# stepping on an arrow makes u automatically go in that direction until u: 
# 1. hit the wall (u wont die)
# 2. hit an empty space (the starting point is consdiered an empty space too)
# 3. hit an obstacle (die)
# 4. hit the end point
# ^ for the first 3 scenarios stated above, you will after which be prompted for your next move

# after each move, the map is reprinted so u can figure out where u are
# your position isn't shown, but the coordinates are printed below the map
# coordinates are printed as y,x (row number,column number)

# only 3 grid types: empty,arrow,obstacle

autopilot = False
previous_area = []

def setAutoPilot(raft, grid_type, key_event):
    if (grid_type in 'D?' and not autopilot) or \
       raft.x_vel != 0 or raft.y_vel != 0:
        return True
    elif grid_type not in 'D?' or key_event is not None:
        del previous_area[:]
        return False
    else:
        return autopilot

def isStuckInLoop(raft):
    grid_coord = raft.getGridCoord()
    if autopilot:
        if grid_coord in previous_area:
            if previous_area[-1] != grid_coord:
                return True
        else:
            previous_area.append(grid_coord)
    return False

def getKeyDownAction(raft, key_event):
    grid_row, grid_col = raft.getGridCoord()
    if key_event=="Up":
        if grid_row>0:
            return key_event
        else:
            print "at corner"
    elif key_event=="Down":
        if grid_row<7:
            return key_event
        else:
            print "at corner"
    elif key_event=="Left":
        if grid_col>0:
            return key_event
        else:
            print "at corner"
    elif key_event=="Right":
        if grid_col<7:
            return key_event
        else:
            print "at corner"
    elif key_event is not None:
        print "invalid input. type up, down, left, right, or end only." 

def getNonKeyDownAction(raft):
    grid_row, grid_col = raft.getGridCoord()
    grid_type = raft.river.grid(*raft.getGridCoord()).getGridType()
    grid_dir = raft.river.grid(*raft.getGridCoord()).getGridDirection()
    if grid_type=="E":
        print "Reached end."
        return 'E'
    elif grid_type=="@":
        print "You're hit an obstacle. Restarted"
        return 'R'
    elif grid_dir=="^":
        if grid_row>0:
            return "Up"
    elif grid_dir=="v":
        if grid_row<7:
            return "Down"
    elif grid_dir=="<":
        if grid_col>0:
            return "Left"
    elif grid_dir==">":
        if grid_col<7:
            return "Right"

def execute(raft, key_event=None):
    global autopilot
    
    grid_row, grid_col = raft.getGridCoord()
    grid_type = raft.river.grid(*raft.getGridCoord()).getGridType()
    autopilot = setAutoPilot(raft, grid_type, key_event)
    print 'in autopilot mode:', autopilot
    print 'grid coordinates:', (grid_row, grid_col)
    print 'grid type:', grid_type
    print

    if key_event is not None:
        return getKeyDownAction(raft, key_event)

    if grid_type!=" ":
        if isStuckInLoop(raft):
            print "You went into an infinite loop. Restarted."
            return 'R'
        return getNonKeyDownAction(raft)

    
