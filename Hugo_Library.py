# Hugo's Library
# import modules
import sys, random, pygame
from pygame.locals import *

# functions that return randomized values
def random_colour():
    return (random.randint(0,255), random.randint(0,255), random.randint(0,255))

def random_health_drop():
    return random.randint(25,65)

def random_location():
    return (random.randint(100,600), random.randint(100,600))

# calculates the velocity based on direction
def calc_velocity(direction, vel=1.0):
    velocity = Point(0, 0)
    if direction == 0:  # north
        velocity.y = -vel
    elif direction == 2:  # east
        velocity.x = vel
    elif direction == 4:  # south
        velocity.y = vel
    elif direction == 6:  # west
        velocity.x = -vel
    return velocity

# prints text using the supplied font
def print_text(font, x, y, text, color=(255,255,255)):
    imgText = font.render(text, True, color)
    # create a surface for text rendering
    screen = pygame.display.get_surface()
    # render
    screen.blit(imgText, (x,y))

# MySprite is a customized class that inherits pygame.sprite.Sprite
class MySprite(pygame.sprite.Sprite):

    def __init__(self):
        # extend the base Sprite class
        pygame.sprite.Sprite.__init__(self)
        self.master_image = None
        self.frame = 0
        self.old_frame = -1
        self.frame_width = 1
        self.frame_height = 1
        self.first_frame = 0
        self.last_frame = 0
        self.columns = 1
        self.last_time = 0
        self.direction = 0
        self.velocity = Point(0.0,0.0) 

    #X property
    def _getx(self): return self.rect.x
    def _setx(self,value): self.rect.x = value
    X = property(_getx,_setx)

    #Y property
    def _gety(self): return self.rect.y
    def _sety(self,value): self.rect.y = value
    Y = property(_gety,_sety)

    #position property
    def _getpos(self): return self.rect.topleft
    def _setpos(self,pos): self.rect.topleft = pos
    position = property(_getpos,_setpos)
        

    def load(self, filename, width, height, columns):
        self.master_image = pygame.image.load(filename).convert_alpha()
        self.frame_width = width
        self.frame_height = height
        self.rect = Rect(0,0,width,height)
        self.columns = columns
        #try to auto-calculate total frames
        rect = self.master_image.get_rect()
        self.last_frame = (rect.width // width) * (rect.height // height) - 1

    def update(self, current_time, rate=30):
        #update animation frame number
        if current_time > self.last_time + rate:
            self.frame += 1
            if self.frame > self.last_frame:
                self.frame = self.first_frame
            self.last_time = current_time

        #build current frame only if it changed
        if self.frame != self.old_frame:
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self.frame_height
            rect = Rect(frame_x, frame_y, self.frame_width, self.frame_height)
            self.image = self.master_image.subsurface(rect)
            self.old_frame = self.frame

    def __str__(self):
        return str(self.frame) + "," + str(self.first_frame) + \
               "," + str(self.last_frame) + "," + str(self.frame_width) + \
               "," + str(self.frame_height) + "," + str(self.columns) + \
               "," + str(self.rect)

# Point class is for locating
class Point(object):
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    #X property
    def getx(self): return self.__x
    def setx(self, x): self.__x = x
    x = property(getx, setx)

    #Y property
    def gety(self): return self.__y
    def sety(self, y): self.__y = y
    y = property(gety, sety)

    # for testing
    def __str__(self):
        return "{X:" + "{:.0f}".format(self.__x) + \
            ",Y:" + "{:.0f}".format(self.__y) + "}"

# a class for the bullets
class bullet:
    # load properties of the bullet
    def __init__(self, x, y, owner, direction, velocity = 10, colour = (0,0,0), collision_boundary = 5):
        self.velocity, self.colour, self.collision_boundary = velocity, colour, collision_boundary
        self.direction, self.x, self.y, self.owner = direction, x, y, owner

    # updates the current location and return
    def position_update(self):
        self.refresh()
        return (self.x, self.y)

    # check for collision with a certain player
    def collision_check(self, player):
        # check if the bullet overlaps with the player in x and y direction
        Y_hit, X_hit = False, False
        if self.y in range(player.Y-self.collision_boundary, player.Y+61+self.collision_boundary):
            Y_hit = True
        if self.x in range(player.X+30-self.collision_boundary, player.X+61+self.collision_boundary):
            X_hit = True
        if X_hit and Y_hit and player != self.owner:
            return True
        else:
            return False

    # refresh the position each frame
    def refresh(self):
        if self.direction == 0:
            self.y -= self.velocity
        elif self.direction == 2:
            self.x += self.velocity
        elif self.direction == 4:
            self.y += self.velocity
        elif self.direction == 6:
            self.x -= self.velocity
        # exit when there's an error
        else: sys.exit()

# the class for the gomoku game
class five:
    def __init__(self,res=(750,750)):
        # initialize, set resolution and set title
        pygame.init()
        self.screen = pygame.display.set_mode(res)
        pygame.display.set_caption(u"Gomoku | 五子棋")
        # initializes the board
        self.board_init()
        self.P1_win, self.P2_win = False, False
        # defines some colours in the form of tuples
        self.white = (255,255,255)
        self.black = (0,0,0)
        self.bg = (50,50,100)
        self.red = (255,100,100)
        self.blue = (100,100,255)
        # defines the font needed
        self.font0 = pygame.font.Font(None, 30)
        self.font1 = pygame.font.Font(None, 300)
        # this one is for the colour change of players
        self.increase = True
        # initialize counters and players' start location
        self.frame_count = 0
        self.P1_move_counter = 0
        self.P2_move_counter = 0
        self.player_location = [0,[4, 6],[10, 6]]
        # this renders the indicators of rows and columns
        row_index = "ABCDEFGHIJKLMNO"
        self.row = []
        self.column = []
        for i in range(15):
            self.row.append(self.font0.render(row_index[i], True, self.white))
            self.column.append(self.font0.render(row_index[i], True, self.white))

    # this initializes the board list and the coordinates of each grid on the board
    def board_init(self):
        # board list holds the status of each grid on the board
        # None = empty; 1 = occupied by player1; 2 = occupied by player2
        self.board = []
        for i in range(15):
            temp = []
            for j in range(15):
                temp.append(None)
            self.board.append(temp)
        # this list holds the coordinates of each grid on the board
        self.board_coordinates = []
        for x in range(39,712,48):
            temp = []
            for y in range(54,727,48):
                temp.append((x,y))
            self.board_coordinates.append(temp)

    # this function defines what will happen in each frame
    def each_frame(self):
        # draw the background
        self.screen.fill(self.bg)
        # increment counters by one each frame
        self.frame_count += 1
        self.P1_move_counter += 1
        self.P2_move_counter += 1
        # change the colour of player every ten frame
        if not (self.frame_count % 10):
            self.flashing_colour()
        # check if anyone has won
        self.winner_check()
        # get players' location and draw them
        P1_x, P1_y = self.player_location[1][0], self.player_location[1][1]
        P2_x, P2_y = self.player_location[2][0], self.player_location[2][1]
        pygame.draw.circle(self.screen, self.blue, self.board_coordinates[P1_x][P1_y], 30)
        pygame.draw.circle(self.screen, self.red, self.board_coordinates[P2_x][P2_y], 30)
        # draw pawns on the board
        for x in range(15):
            for y in range(15):
                if self.board[x][y]:
                    # identify which player's pawn this one is and assign colour
                    if self.board[x][y] == 2:
                        colour = (255,100,100)
                    else: colour = (100,100,255)
                    pygame.draw.circle(self.screen, colour, self.board_coordinates[x][y], 20)

        # get current event and keys pressed
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
        keys = pygame.key.get_pressed()
        # controls player1
        if not(self.P1_win or self.P2_win):
            if keys[K_w]:
                self.P_move(1, 0)
            elif keys[K_d]:
                self.P_move(1, 2)
            elif keys[K_s]:
                self.P_move(1, 4)
            elif keys[K_a]:
                self.P_move(1, 6)
            if keys[K_1]:
                self.P_move(1, 8)
            # controls player2
            if keys[K_UP]:
                self.P_move(2, 0)
            elif keys[K_RIGHT]:
                self.P_move(2, 2)
            elif keys[K_DOWN]:
                self.P_move(2, 4)
            elif keys[K_LEFT]:
                self.P_move(2, 6)
            if keys[K_2]:
                self.P_move(2, 8)
        elif self.P1_win:
            self.board = [[1]*15]*15
            print_text(self.font1, 30, 30, "Blue", self.white)
            print_text(self.font1, 40, 200, "Wins", self.white)
        elif self.P2_win:
            self.board = [[2]*15]*15
            print_text(self.font1, 30, 30, "Red", self.white)
            print_text(self.font1, 40, 200, "Wins", self.white)
        self.draw_board()
        pygame.display.update()

    # this function draws the board
    def draw_board(self):
        # draw columns
        x1, y1 = 15, 30
        x2, y2 = 15, 750
        for i in range(16):
            pygame.draw.line(self.screen, self.white, (x1,y1), (x2,y2), 3)
            # write column indicator
            if i != 15:
                self.screen.blit(self.column[i], (x1+17,10))
            x1 += 48
            x2 += 48
        # draw rows
        x1, y1 = 15, 30
        x2, y2 = 735, 30
        for i in range(16):
            pygame.draw.line(self.screen, self.white, (x1, y1), (x2, y2), 3)
            # write row indicator
            if i != 15:
                self.screen.blit(self.row[i], (0,y1+17))
            y1 += 48
            y2 += 48

    # functions used to check if there's a winner
    def in_row(self,x,y):
        for i in range(5):
            if not(self.board[x][y] == self.board[x+i][y]):
                return False
        return True
    def in_column(self,x,y):
        for i in range(5):
            if not(self.board[x][y] == self.board[x][y+i]):
                return False
        return True
    def in_cross1(self,x,y):
        for i in range(5):
            if not(self.board[x][y] == self.board[x+i][y+i]):
                return False
        return True
    def in_cross2(self,x,y):
        for i in range(5):
            if not(self.board[x][y] == self.board[x-i][y+i]):
                return False
        return True

    # check if anyone wins and end the game if true
    def winner_check(self):
        for x1 in range(11):
            for y1 in range(11):
                if self.in_cross1(x1,y1):
                    exec(f"self.P{self.board[x1][y1]}_win = True")
            for y2 in range(15):
                if self.in_row(x1,y2):
                    exec(f"self.P{self.board[x1][y2]}_win = True")
        for x2 in range(15):
            for y1 in range(11):
                if self.in_column(x2,y1):
                    exec(f"self.P{self.board[x2][y1]}_win = True")
        for x3 in range(4,15):
            for y1 in range(11):
                if self.in_cross2(x3,y1):
                    exec(f"self.P{self.board[x3][y1]}_win = True")


    # this function allows the players to change colour
    def flashing_colour(self):
        red = self.red[0]
        blue = self.blue[2]
        # RGB value's R and B increase to 255 and drop to 120 repeatedly
        if (red == 255) or (red == 120):
            self.increase = not self.increase
        if self.increase:
            self.red = (red+1, 100, 100)
            self.blue = (100, 100, blue+1)
        else:
            self.red = (red-1, 100, 100)
            self.blue = (100, 100, blue-1)
        return 0

    # this function moves the player and places pawns
    def P_move(self,player,direction):
        # set local variables with shorter names
        row, column = self.player_location[player]
        # move the player and place the pawn with a cool down of 60 frames
        if (self.P1_move_counter>60 and player == 1) or (self.P2_move_counter>60 and player == 2):
            # move player in a direction
            if direction == 0 and column != 0:
                exec(f"self.P{player}_move_counter = 0")
                self.player_location[player][1] -= 1
            elif direction == 2 and row != 14:
                exec(f"self.P{player}_move_counter = 0")
                self.player_location[player][0] += 1
            elif direction == 4 and column != 14:
                exec(f"self.P{player}_move_counter = 0")
                self.player_location[player][1] += 1
            elif direction == 6 and row != 0:
                exec(f"self.P{player}_move_counter = 0")
                self.player_location[player][0] -= 1
            # place pawn at current location
            if direction == 8 and (not self.board[row][column]):
                self.board[row][column] = player