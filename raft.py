import logic

class RaftGUI:
    '''
    The RaftGUI is the interface between the main GUI and the logic module.
    All properties of the raft, such as the location and velocity of the
    raft is set here. Any key press event is being evaluated here.

    The interface to the GUI module is:
    1. updating of coordinates of the GUI canvas item
    2. getting key press events from the GUI

    The interface to the logic module is:
    1. sending key press events to the logic module
    2. sending grid type to the logic module
    3. getting the resulting action from 1 & 2

    Internal processing of the RaftGUI:
    1. internal update of coordinates
    2. setting a destination
    3. setting of velocity base on destination
    '''
    vel = 1
    game_ended = False
    
    def __init__(self, river):
        '''
        Initialises a new raft, setting it's start coordinate base on the
        where the 'S' grid is located in the map.
        Initialise velocity and destination.
        '''
        self.river = river
        self.grid_coord = river.getStartOrEndCoord('S').getGridID()
        self.XY_coord = list(river.grid(*self.grid_coord).getXYCoord())
        self.starting_grid_coord = self.grid_coord
        self.starting_XY_coord = self.XY_coord[:]
        self.x_vel = 0
        self.y_vel = 0
        self.dest_grid_coord = None
        self.dest_XY_coord = None

    def getGridCoord(self):
        return self.grid_coord

    def getXYCoord(self):
        return self.XY_coord

##    def getCornerCoord(self):
##        '''
##        Get the corner coordinates to define a canvas shape.
##        Useless in case of creating image.
##        '''
##        return (self.XY_coord[0], self.XY_coord[1],
##                self.XY_coord[0] + grid_length,
##                self.XY_coord[1] + grid_length)

    def restartLevel(self):
        ''' Reset all the coordinates '''
        self.grid_coord = self.starting_grid_coord
        self.XY_coord = self.starting_XY_coord[:]
        self.game_ended = False
        self.setNextAction(logic_event=logic.execute(self))

    def move(self):
        ''' Update XY coordinates base on set velocity '''
        self.XY_coord[0] += self.x_vel
        self.XY_coord[1] += self.y_vel
        # sets destination to None when it has reached
        # then resets velocity and finally interfaces with the logic
        # module (to update the logic module with its new location)
        if self.isAtDestination():
            self.grid_coord = self.dest_grid_coord # update grid coordinate
            self.resetDestination()
            self.setVel()
            self.setNextAction(logic_event=logic.execute(self))

    def isAtDestination(self):
        at_dest = False
        # assuming that we are dealing strictly with integer
        # otherwise we will need to compare by epsilon
        dest_coord = list(self.dest_XY_coord) \
                     if self.dest_XY_coord is not None else None
        if self.XY_coord == dest_coord:
            at_dest = True
        return at_dest

    def resetDestination(self):
        self.dest_grid_coord = None
        self.dest_XY_coord = None

    def setDestination(self, grid_coord):
        self.dest_grid_coord = grid_coord
        self.dest_XY_coord = self.river.grid(*grid_coord).getXYCoord()

    def getDestination(self, event):
        curr_grid = self.getGridCoord()
        if event == 'Up':
            return (curr_grid[0] - 1, curr_grid[1])
        elif event == 'Down':
            return (curr_grid[0] + 1, curr_grid[1])
        elif event == 'Left':
            return (curr_grid[0], curr_grid[1] - 1)
        elif event == 'Right':
            return (curr_grid[0], curr_grid[1] + 1)
        else:
            print 'getDestination error/no destination'

    def setVel(self):
        ''' Sets the velocity base on destination. '''
        if self.dest_XY_coord is None:
            self.x_vel = 0
            self.y_vel = 0
        else:
            # assumming that we are dealing strictly with integer
            # otherwise we will need to compare by epsilon
            if self.dest_XY_coord[0] < self.XY_coord[0]:
                self.x_vel = -self.vel
            elif self.dest_XY_coord[0] > self.XY_coord[0]:
                self.x_vel = self.vel
            else:
                self.xvel = 0
                
            if self.dest_XY_coord[1] < self.XY_coord[1]:
                self.y_vel = -self.vel
            elif self.dest_XY_coord[1] > self.XY_coord[1]:
                self.y_vel = self.vel
            else:
                self.y_vel = 0

    def hasEnded(self):
        return self.game_ended

    def isInAutopilotMode(self):
        '''No keystroke is allowed as long as raft is moving.
           When not moving, it could be in the middle of autopilot mode.
           Therefore we need to disable keystroke when in autopilot mode too.
           '''
        return not (self.x_vel == 0 and self.y_vel == 0 and \
                    logic.getNonKeyDownAction(self) is None)

    def keyDown(self, event):
        ''' Interface with GUI to get key press events.
            Checks if keystroke is allowed before setting new action.
            When raft is still moving, any keystroke may cause the
            program to set a new destination. Therefore this must
            be taken into account.'''
        if not self.isInAutopilotMode():
            self.setNextAction(key_event=event)

    def setNextAction(self, key_event=None, logic_event=None):
        ''' Interface with logic module to get next course of action. '''
        print 'key event: {}, logic event: {}'.format(key_event, logic_event)
        if key_event is not None:
            logic_event = logic.execute(self, key_event.keysym)
        if logic_event in ['Up', 'Down', 'Left', 'Right']:
            self.setDestination(self.getDestination(logic_event))
        elif logic_event == 'E' or logic_event == 'R':
            self.game_ended = True
##        elif logic_event == 'R':
##            self.restartLevel()

