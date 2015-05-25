from Tkinter import *
from mapUtil import *
from raft import *
import maps
import random

grid_length = 40
grid_columns = 8
grid_rows = 8
canvas_width = grid_length * grid_columns
canvas_height = grid_length * grid_rows

class GameGUI:
    '''
    The GameGUI creates the canvas and all its items. The canvas is updated
    at roughly 60 frames per second. At each canvas updates, it will get
    any coordinate updates from the raft object. The raft object in turn
    get it's cue from the logic module.

    Every time an arrow key is pressed, it gets 'sent' to the raft object
    for processing, which then 'asks' the logic module for the next action.
    Hence the raft object act as a interface between the GUI and logic module.
    '''
    instruction_txt = 'Story:\n\nHelp Cui Cui navigate through the '\
                      'strong current in the river and overcome obstacles to '\
                      'reach the destination marked X. \n\nUse the arrow '\
                      'keys to navigate.'
    def __init__(self, root=None):
        if root is not None:
            self.root = root
        self.root.title('Game')
        # sets the main window at the center of the screen
        self.root.geometry(self.getGeometry(canvas_width + 94,
                                            canvas_height + 4))
        
        self.msg_instruction = Message(self.root,
                                       text=self.instruction_txt,
                                       width=80)
        self.msg_instruction.pack(side=LEFT)
        
        self.canvas = Canvas(background='white',
                             width=canvas_width,
                             height=canvas_height)
        self.canvas.pack(side=LEFT)

        self.initialise()

        self.root.bind('<Key>', self.keyDown)

    def initialise(self):
        self.root.withdraw()
        self.game_level = None
        self.game_ended = False
        # create the window for level selection
        self.createLevelSelectorWindow()

    def createLevelSelectorWindow(self):
        '''Creates the window for level selection. After user chooses
           a level, the window will be destroyed, and the main window
           will be brought back. '''
        self.toplevel_menu = Toplevel(self.root, takefocus=True)
        self.toplevel_menu.geometry(self.getGeometry(200, 210))        
        self.toplevel_menu.overrideredirect(1)
        #self.toplevel_menu.lift(self.root)
        self.toplevel_menu.wm_attributes("-topmost", 1)

        self.btn_lvl1 = Button(self.toplevel_menu,
                               text='Level 1',
                               command=lambda:self.levelSelector(1))
        self.btn_lvl2 = Button(self.toplevel_menu,
                               text='Level 2',
                               command=lambda:self.levelSelector(2))
        self.btn_lvl3 = Button(self.toplevel_menu,
                               text='Level 3',
                               command=lambda:self.levelSelector(3))
        self.btn_lvl4 = Button(self.toplevel_menu,
                               text='Map test',
                               command=lambda:self.levelSelector(4))
        self.btn_lvl1.pack(padx=20, pady=13)
        self.btn_lvl2.pack(padx=20, pady=13)
        self.btn_lvl3.pack(padx=20, pady=13)
        self.btn_lvl4.pack(padx=20, pady=13)

    def levelSelector(self, lvl):
        self.game_level = lvl
        self.toplevel_menu.destroy()
        self.createMapAndRaft(lvl)
        # bring the main window back
        self.root.deiconify()
        
    def getGeometry(self, w, h):
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        return '{}x{}+{}+{}'.format(w, h, x, y)

    def createMapAndRaft(self, lvl):
        # create the map
        map_level = random.choice(maps.mapSelection[lvl])
        self.river = MapGUI(map_level, grid_length)
        self.up_current_image = PhotoImage(file = './images/up.gif')
        self.down_current_image = PhotoImage(file = './images/down.gif')
        self.left_current_image = PhotoImage(file = './images/left.gif')
        self.right_current_image = PhotoImage(file = './images/right.gif')
        self.no_current_image = PhotoImage(file = './images/empty.gif')
        self.obstacle_image = PhotoImage(file = './images/obstacle.gif')
        self.end_image = PhotoImage(file = './images/end.gif')

        self.canvas_grid_id = []
        for row in range(grid_rows):
            self.canvas_grid_id.append([])
            for col in range(grid_columns):
                if self.river.grid(row, col).getGridType() in 'D?':
                    if self.river.grid(row, col).getGridDirection() == '^':
                        image_file = self.up_current_image
                    elif self.river.grid(row, col).getGridDirection() == 'v':
                        image_file = self.down_current_image
                    elif self.river.grid(row, col).getGridDirection() == '<':
                        image_file = self.left_current_image
                    elif self.river.grid(row, col).getGridDirection() == '>':
                        image_file = self.right_current_image
                elif self.river.grid(row, col).getGridType() == '@':
                    image_file = self.obstacle_image
                elif self.river.grid(row, col).getGridType() == 'E':
                    image_file = self.end_image
                else:
                    image_file = self.no_current_image
                self.canvas_grid_id[row].append(self.canvas.create_image(*self.river.grid(row, col).getXYCoord(),
                                         image=image_file,
                                         anchor=N+W))

        # create the raft
        self.raft = RaftGUI(self.river)
        self.raft_image = PhotoImage(file = './images/raft.gif')
        self.raft_ID = self.canvas.create_image(*self.raft.getXYCoord(),
                                                image=self.raft_image,
                                                anchor=N+W)
        if self.game_level in [2, 3, 4]:
            self.randomiseGrids()
        self.updateCanvas()

    def updateCanvas(self):
        if not self.game_ended:
            if self.raft.hasEnded():
                self.game_ended = True
                self.endGameEvent()
        self.updateRaft()
        self.update_id = self.canvas.after(17, self.updateCanvas)

    def randomiseGrids(self):
        '''Randomise all '?' grids whenever the raft is in non-autopilot
           mode.'''
        #if logic.autopilot == False:
##        if (self.raft.x_vel == 0 and self.raft.y_vel == 0) or \
##           self.raft.river.grid(*self.raft.getGridCoord()).getGridType() not in 'D?':
        if logic.autopilot == False and \
           (self.raft.x_vel == 0 and self.raft.y_vel == 0):
            for row in range(grid_rows):
                for col in range(grid_columns):
                    if self.river.grid(row, col).getGridType() == '?':
                        random_dir = random.choice('^v<>')
                        self.river.grid(row, col).setGridDirection(random_dir)
                        self.updateArrowImage(row, col, random_dir)
            self.randomise_id = self.canvas.after(2500, self.randomiseGrids)
        else:
            self.randomise_id = self.canvas.after(17, self.randomiseGrids)

    def updateArrowImage(self, row, col, new_dir):
        if new_dir == '^':
            image_file = self.up_current_image
        elif new_dir == 'v':
            image_file = self.down_current_image
        elif new_dir == '<':
            image_file = self.left_current_image
        elif new_dir == '>':
            image_file = self.right_current_image
        
        self.canvas.itemconfig(self.canvas_grid_id[row][col],
                               image=image_file)

    def updateRaft(self):
        # The velocity is always updated base on the current destination.
        # Zero velocity is set when there is no destination.
        # The raft is constantly 'moving' base on the set velocity
        self.raft.setVel()
        self.raft.move()

        # raft.move() only updates the coordinate of the object. Here we need
        # to get the coordinate from the raft object and update the actual canvas
        # item.
        self.canvas.coords(self.raft_ID, *self.raft.getXYCoord())
        
    def keyDown(self, event):
        self.raft.keyDown(event)
        if self.game_level in [2, 3, 4] and self.raft.isInAutopilotMode():
            self.canvas.after_cancel(self.randomise_id)
            self.randomise_id = self.canvas.after(2500, self.randomiseGrids)
            
    def test(self):
        pass

    def endGameEvent(self):
        print 'game ended'
        self.root.withdraw()
        self.raft.restartLevel()
        self.createEndGameWindow()
        self.game_ended = False

    def createEndGameWindow(self):
        self.toplevel_end = Toplevel(self.root, takefocus=True)
        self.toplevel_end.geometry(self.getGeometry(200, 200))        
        self.toplevel_end.overrideredirect(1)
        #self.toplevel_end.lift(self.root)
        self.toplevel_end.wm_attributes("-topmost", 1)

        self.btn_lvl1 = Button(self.toplevel_end,
                               text='Restart level',
                               command=self.restartLevel)
        self.btn_lvl2 = Button(self.toplevel_end,
                               text='Choose new level',
                               command=self.newLevel)
        self.btn_lvl3 = Button(self.toplevel_end,
                               text='Exit',
                               command=self.exitGame)
        self.btn_lvl1.pack(padx=20, pady=20)
        self.btn_lvl2.pack(padx=20, pady=20)
        self.btn_lvl3.pack(padx=20, pady=20)

    def restartLevel(self):
        self.toplevel_end.destroy()
        self.root.deiconify()

    def newLevel(self):
        self.toplevel_end.destroy()
        self.canvas.after_cancel(self.update_id)
        if self.game_level in [2, 3, 4]:
            self.canvas.after_cancel(self.randomise_id)
        self.initialise()

    def exitGame(self):
        self.root.destroy()        

root = Tk()
game = GameGUI(root)
root.mainloop()
