import random
class MapGUI:
    '''
    MapGUI has two main functionality:
    1. It can print a n by n map, so that you can simply copy and paste
    the list into your python editor and build a map level from the list.
    This is not important, can ignore.

    2. Given an input map(stored in the maps.py), it will initialise
    the grids of the map. It will set the properties of the grids base on
    what is defined in the input map. The grid properties can be accessed
    as follows:

    river = MapGUI(maps.map_lvl1, grid_length)
    grid_ID = river.grid(row, col).getGridID()
    grid_type = river.grid(row, col).getGridType()
    and so on...
    '''
    def __init__(self, map_lvl, grid_size, col=None, row=None):
        self.col = col
        self.row = row
        self.grid_size = grid_size
        self.createMap(map_lvl)

    def createEmptyMap(self):
        empty_map = [[' ' for i in range(self.row)] for j in range(self.col)]
        return empty_map

    def printEmptyMap(self):
        empty_map = self.createEmptyMap()
        rows = ',\n'.join([str(row) for row in empty_map])
        map_string = '[' + rows + ']'
        print map_string        

    def createMap(self, map_lvl):
        self.grid_ = []
        for row in range(len(map_lvl)):
            self.grid_.append([])
            for col in range(len(map_lvl[0])):
                self.grid_[row].append(Grid(self.grid_size, (row, col), map_lvl[row][col]))

    def grid(self, row, col):
        return self.grid_[row][col]

    def getStartOrEndCoord(self, s):
        for row in range(len(self.grid_)):
            for col in range(len(self.grid_[0])):
                if self.grid(row, col).getGridType() == s:
                    return self.grid(row, col)

class Grid:
    '''
    A grid object has the following attributes:
    1. XYcoord - A tuple
    2. grid_ID - A tuple. (i, j) stands for row number i, column number j
    3. grid_type - defines how the current flows, if any, and whether it is an obstacle,
                    it also defines the starting and ending position by 'S' and 'E'.
    '''
    XYcoord = (0, 0)
    def __init__(self, grid_size, grid_ID, grid_type):
        self.grid_size = grid_size
        self.grid_ID = grid_ID
        self.setGridType(grid_type)
        self.setGridDirection(grid_type)
        self.setXYCoord()

    def getGridID(self):
        return self.grid_ID
        
    def getGridType(self):
        return self.grid_type

    def getGridDirection(self):
        return self.grid_direction

    def setGridType(self, grid_type):
        if grid_type in '^v<>':
            self.grid_type = 'D'
        else:
            self.grid_type = grid_type

    def setGridDirection(self, grid_type):
        if grid_type in '^v<>':
            self.grid_direction = grid_type
        elif grid_type == '?':
            self.grid_direction = random.choice('^v<>')
        else:
            self.grid_direction = None

    def getXYCoord(self):
        return self.XYCoord

    def setXYCoord(self):
        x = self.grid_ID[1] * self.grid_size
        y = self.grid_ID[0] * self.grid_size
        self.XYCoord = (x, y)

