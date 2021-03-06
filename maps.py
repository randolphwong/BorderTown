'''
symbol legends:
'^': upward current
'v': downward current
'<': left current
'>': right current
'@': obstacle
'S': starting location
'E': ending location
' ': no current

Simply edit the symbols to create a new map. You can also edit Benjamin's code
a little to create a map with randomised paths. The map levels corresponds to
the map level the user chooses at the start of the game.

The game will pick a random map in that map level. So if you want to do testing,
edit the map inside the test_map.

   [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
'''
map_lvl1 = []
map_lvl2 = []
map_lvl3 = []
test_map = []

map_lvl1.append(   [[' ', '@', ' ', ' ', 'v', ' ', '@', ' '],
                    [' ', ' ', '>', '>', '^', '>', '>', 'v'],
                    [' ', 'v', 'S', '^', '@', ' ', '@', 'v'],
                    ['@', 'v', 'v', '^', '>', '>', '^', '<'],
                    ['v', '<', 'v', '^', '>', 'v', 'v', ' '],
                    ['v', '<', ' ', '<', '^', 'E', '^', '@'],
                    ['>', '>', 'v', '^', '^', '<', 'v', '@'],
                    [' ', ' ', '>', '>', ' ', '^', '<', ' ']])

map_lvl2.append(   [['v', ' ', '?', '<', '<', '<', '<', '@'],
                    [' ', 'v', '<', '^', 'v', '?', ' ', ' '],
                    ['v', '?', '@', '@', 'v', '@', '?', '^'],
                    ['v', ' ', 'v', '>', 'E', '<', '^', '^'],
                    ['v', '^', '?', ' ', '^', '>', '?', '^'],
                    ['>', ' ', '>', '@', '^', '^', '>', ' '],
                    ['?', '>', ' ', 'v', '^', '^', 'S', 'v'],
                    [' ', '@', '^', '?', ' ', '<', '?', '@']])

#from anand
map_lvl2.append(   [['>', '^', '>', '<', '<', '?', '@', '<'],
                    ['?', '<', ' ', '<', '<', ' ', ' ', '^'],
                    ['v', '>', '>', '>', 'v', '>', '^', '^'],
                    [' ', '@', '<', '^', '<', ' ', '^', '^'],
                    ['v', '>', '<', ' ', '@', ' ', '>', '^'],
                    ['E', '^', '>', '^', ' ', '^', '^', ' '],
                    ['@', '^', '@', '?', '>', ' ', '>', '@'],
                    ['S', ' ', ' ', '^', '^', '>', '^', ' ']])
#ben's orginal
##map_lvl3.append(   [['@', '?', ' ', 'v', 'E', 'v', 'S', 'v'],
##                    ['@', '^', ' ', '@', '^', 'v', '>', 'v'],
##                    ['>', '?', 'v', '^', '^', '>', 'v', ' '],
##                    ['?', '<', '>', '?', '^', '@', '>', 'v'],
##                    ['?', '^', '<', '<', '?', ' ', '@', '?'],
##                    ['?', '>', ' ', '<', '?', '@', 'v', ' '],
##                    ['v', ' ', '^', '@', '?', '<', '>', '?'],
##                    ['>', '?', '>', '@', '<', '^', '<', '<']])
#modified ben
map_lvl3.append(   [['@', '>', ' ', '>', 'E', 'v', 'S', 'v'],
                    ['@', '?', ' ', '@', '?', 'v', '>', 'v'],
                    ['>', ' ', '?', '^', '?', '>', 'v', ' '],
                    ['?', '^', '?', '?', '^', '@', '>', 'v'],
                    ['?', '^', '>', '^', '?', ' ', '@', '?'],
                    ['?', '>', ' ', '<', '?', '@', 'v', ' '],
                    ['v', ' ', '^', '@', '^', '<', '>', 'v'],
                    ['>', '?', '>', '@', '<', '^', '<', '<']])

##map_lvl3.append(   [['>', 'v', '?', '5', '<', 'v', '<', '<'],
##                    ['?', '>', 'v', 'v', '?', '<', 'v', '^'],
##                    ['1', 'v', 'v', '>', 'v', '@', '^', '4'],
##                    ['^', 'v', '>', 'v', 'v', 'E', '<', '^'],
##                    ['^', '>', 'v', 'v', '6', '?', '>', '?'],
##                    ['?', '?', 'v', 'v', '?', '@', '3', '<'],
##                    ['^', 'S', 'v', '2', '>', '?', ' ', '^'],
##                    ['^', '<', '<', '>', '>', '?', '>', '^']])
map_lvl3.append(   [['>', 'v', '?', ' ', '<', 'v', '<', '<'],
                    ['?', '>', 'v', 'v', '?', '<', 'v', '^'],
                    [' ', 'v', 'v', '>', 'v', '@', '^', ' '],
                    ['^', 'v', '>', 'v', 'v', 'E', '<', '^'],
                    ['^', '>', 'v', 'v', ' ', '?', '>', '?'],
                    ['?', '?', 'v', 'v', '?', '@', ' ', '<'],
                    ['^', 'S', 'v', ' ', '>', '?', ' ', '^'],
                    ['^', '<', '<', '>', '>', '?', '>', '^']])

##map_lvl3.append(   [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
##                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
##                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
##                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
##                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
##                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
##                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
##                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]

test_map.append(   [['v', '<', '<', '<', '<', '<', '<', '^'],
                    ['v', 'v', '<', '<', '<', '<', '<', '^'],
                    ['v', 'v', ' ', ' ', ' ', ' ', '^', '^'],
                    ['v', ' ', '?', '?', '?', ' ', '^', '^'],
                    ['v', ' ', ' ', '?', 'E', ' ', '^', '^'],
                    ['>', 'v', '>', ' ', ' ', ' ', '^', '^'],
                    ['<', '>', '>', '>', '>', '>', '^', '^'],
                    ['S', '>', '>', '>', '>', '>', '>', '^']])


mapSelection = {1: map_lvl1, 2: map_lvl2, 3: map_lvl3, 4: test_map}
