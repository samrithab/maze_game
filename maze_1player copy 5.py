import random
from stack import Stack

class MazeGame:
    '''
    A game where a player moves through a grid to reach some treasure.
    '''

    def __init__(self, width, height, player, monster1, monster2):
        '''
        (MazeGame, Player) -> None
        Construct a new MazeGame with the given width and height,
        and a player. MazeGame should also place a "gold" at
        a randomly chosen coordinate on the far edge of the grid.
        '''
        
        self.width = width
        self.height = height
        self.player = player
        self.monster1 = monster1
        self.monster2 = monster2
        # place the gold at a random spot on the far edge of the grid
        self.gold_coord = (width-1, random.randint(1, height-1)) 

        self.grid = []
        self.make_grid()
        self.direc = ''
        self.flee_direc = ''
        
    def make_grid(self):
        '''
        (MazeGame) -> None
        Given width, height and positions of player and gold,
        append things to this maze's grid.
        '''
        
        for i in range(self.height):
            self.grid.append([])
            for j in range(self.width):
                self.grid[i].append('(_)')

        self.grid[self.monster1.y][self.monster1.x] = "(_)"
        self.grid[self.monster2.y][self.monster2.x] = "(_)"
        
        self.grid[self.player.y][self.player.x] = '(x)'
        self.grid[self.gold_coord[1]][self.gold_coord[0]] = '(*)'
    
    def play_game(self):
        '''
        (MazeGame) -> None
        Play the game, with each player taking turns making a move, until
        one player reaches the gold. Players each keep track of their wins and losses.
        '''
        b = False
        # print out the starting state of the maze
        print(self)
        print('------------')
        
        while ((self.player.x, self.player.y) != \
               (self.gold_coord[0], self.gold_coord[1]) and self.battle_mode != False):
            # if no one has reached the gold yet, play one turn of the game (one player makes one move)
            if self.play_one_turn() == False:
                b = False
                break
            b = True

        if b == True:
            print('Yay, you won, {}!'.format(self.player.name))
        else:
            print('You lost')


    def get_new_position(self, d):
        '''
        (MazeGame, str) -> tuple of two ints or None        
        Given a direction represented as a string "N", "S", "E", or "W" (for moving North,
        South, East or West respectively), return the new position. If the new position is
        not valid (i.e. falls outside of the grid), return None.
        '''
        
        direction_dict = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}
        dx, dy = direction_dict[d]
        new_x = self.player.x + dx
        new_y = self.player.y + dy

        if (0 <= new_x < self.width) and (0 <= new_y < self.height):
            return new_x, new_y
        else:
            return None

    def update_grid(self, new_position):
        '''
        (MazeGame, tuple of two ints) -> None
        Move player to the given new position in grid.
        '''
        # update grid to reflect updated coordinates for current_player
        # keep track of the Player's current position before they move
        old_x, old_y = self.player.x, self.player.y 
        self.player.move(new_position)
        self.grid[self.player.y][self.player.x] = self.grid[old_y][old_x]
        self.grid[old_y][old_x] = '(_)'
        
    def play_one_turn(self):
        '''
        (MazeGame) -> None
        Play one turn of the game. Turn could involve moving one place,
        attempting to move one place, or undoing the most recent move.
        '''
        
        # get the direction the Player wants to move
        direction = self.player.get_direction()
        self.direc = direction
        e = False
        
        if (direction == 'U'):
            self.undo_last_move()
        else:
            # this returns None if move is not valid
            new_position = self.get_new_position(direction)

            if (new_position) == (self.monster1.x, self.monster1.y) or (new_position) == (self.monster2.x, self.monster2.y):
                q = str(input('Do you wish to attack (a) or flee (f)? '))
                if q == 'a':
                    x = self.battle_mode()
                    if x == True:
                        if new_position:
                            self.update_grid(new_position)
                            print("Player {} moved {}.".format(self.player.name, direction))
                        else:
                            print("Player {} attempted to move {}. Way is blocked.".format(self.player.name, direction))

                    else:
                        return False
                else:
                    self.flee_mode()
                    new_position = self.get_new_position(self.flee_direc)

                    if new_position == (self.monster1.x, self.monster1.y) or new_position == (self.monster2.x, self.monster2.y) or new_position == None:
                        print("Flee Denied")
                        self.prompt_again()
                        
                    elif new_position:
                        self.update_grid(new_position)
                        print("Player {} moved {}.".format(self.player.name, self.flee_direc))
                    #else:
                        #print("Player {} attempted to move {}. Way is blocked.".format(self.player.name, self.flee_direc))

                           
                print(self)
                print('------------')
            
            elif new_position:
                self.update_grid(new_position)
                print("Player {} moved {}.".format(self.player.name, direction))
            else:
                print("Player {} attempted to move {}. Way is blocked.".format(self.player.name, direction))

                           
        print(self)
        print('------------')



    def prompt_again(self):

        new_position = self.get_new_position(self.direc)
        q = str(input('Do you wish to attack (a) or flee (f)? '))
        if q == 'a':
            x = self.battle_mode()
            if x == True:
                if new_position:
                    self.update_grid(new_position)
                    print("Player {} moved {}.".format(self.player.name, self.direc))
                else:
                    print("Player {} attempted to move {}. Way is blocked.".format(self.player.name, self.direc))

            else:
                return False
        else:
            print("Flee denied, you are forced to attack now")
            print("You are forced to attack now")
            x = self.battle_mode()
            if x == True:
                if new_position:
                    self.update_grid(new_position)
                    print("Player {} moved {}.".format(self.player.name, self.direc))
                else:
                    print("Player {} attempted to move {}. Way is blocked.".format(self.player.name, self.direc))

            else:
                return False


    def undo_last_move(self):
        '''
        (MazeGame) -> None
        Update the grid to the state it was in before the previous move was made.
        If no moves were previously made, print out the message "Can't undo".
        '''
        
        # TODO: IMPLEMENT THIS AS DESCRIBED IN INSTRUCTIONS

        if self.player.moves.isEmpty():
            print("Cant't undo")

        else:
            direc = self.player.moves.pop()
            if direc == "N":
                new_position = self.get_new_position("S")
                if new_position:
                    self.update_grid(new_position)

            elif direc == "S":
                new_position = self.get_new_position("N")
                if new_position:
                    self.update_grid(new_position)

            elif direc == "E":
                new_position = self.get_new_position("W")
                if new_position:
                    self.update_grid(new_position)

            elif direc == "W":
                new_position = self.get_new_position("E")
                if new_position:
                    self.update_grid(new_position)


                    
                    
    def battle_mode(self):
        print("You have entered a monster occupied zone")
        print("You have " + str(self.player.hp) + "life points")
        if self.player.x == 0:
            print("Monster's life points " + str(self.monster1.hp))
            while self.player.hp > 0 and self.monster1.hp > 0:
                    j = input("Press 's' to shoot ")
                    if j == 's':
                        self.player.attack(self.monster1)
                        if self.monster1.hp > 0:
                            self.monster1.attack(self.player)
                            print("The monster attacked you")
            if self.monster1.hp == 0:
                self.monster1.move((-2, -2))
                print("You defeated the monster")
                return True
                   
            else:
                print("The monster defeated you")
                return False

        else:
            print("Monster's life points " + str(self.monster2.hp))
            while self.player.hp > 0 and self.monster2.hp > 0:
                    j = input("Press 's' to shoot ")
                    if j == 's':
                        self.player.attack(self.monster2)
                        if self.monster2.hp > 0:
                            self.monster2.attack(self.player)
                            print("The monster attacked you")
            if self.monster2.hp == 0:
                self.monster2.move((-2, -2))
                print("You defeated the monster")
                return True
                   
            else:
                print("The monster defeated you")
                return False
            

    def flee_mode(self):

        if self.direc == "N":
            q = ["S", "E", "W"]
            w = random.randint(0, 2)
            self.flee_direc = q[w]
        elif self.direc == "S":
            q = ["N", "E", "W"]
            w = random.randint(0, 2)
            self.flee_direc = q[w]
        elif self.direc == "E":
            q = ["N", "S", "W"]
            w = random.randint(0, 2)
            self.flee_direc = q[w]
        elif self.direc == "W":
            q = ["N", "S", "E"]
            w = random.randint(0, 2)
            self.flee_direc = q[w]
                
            
            
            
    def __str__(self):
        '''
        (MazeGame) -> str
        Return string representation of the game's grid.
        '''
        s = ''
        for row in self.grid:
            s += ''.join(row) + "\n"
        return s.strip()


# TODO: IMPLEMENT PLAYER CLASS AS DESCRIBED IN INSTRUCTIONS
class Player:
    """Creates a new Player
    """
    def __init__(self, name, x, y, hp):
        self.name = name
        self.x = x
        self.y = y
        self.moves = Stack()
        self.hp = hp

    def move(self, tuple):
        self.x = tuple[0]
        self.y = tuple[1]

    def get_direction(self):
        a = str(input('Enter Direction: '))
        if a!= 'U':
            self.moves.push(a)
        return a
    
    def attack(self, monster):
        monster.hp -= 1
        
class Monster:
    """ Creates a Monster
    """
    def __init__(self, x, y, hp):
        self.x = x
        self.y = y
        self.hp = hp

    def move(self, tuple):
        self.x = tuple[0]
        self.y = tuple[1]

    def attack(self, player):
        player.hp -= 1

class HardMonster:
    """ Creates a Monster
    """
    def __init__(self, x, y, hp):
        self.x = x
        self.y = y
        self.hp = hp

    def move(self, tuple):
        self.x = tuple[0]
        self.y = tuple[1]

    def attack(self, player):
        player.hp -= 2




def main():
    """Prompt the user to configure and play the game."""

    width = int(input("Width: "))
    height = int(input("Height: "))

    name = input("What is your name? ")
    p1hp = random.randint(1, 5)
    m1hp = random.randint(1, 5)
    m2hp = random.randint(1, 5)
    p1 = Player(name, 0, 0, p1hp) # make a player at position (0,0)
    monster1 = Monster(0, random.randint(1, height - 1), m1hp)
    monster2 = HardMonster(width-1, random.randint(0, 1), m2hp)
    
    
    play_again = True
    while play_again:
        g = MazeGame(width, height, p1, monster1, monster2)
        g.play_game()
        # reset player locations at end of round
        p1.move((0,0))
        p1.hp = random.randint(1, 5)
        monster1.hp = random.randint(1, 5)
        monster2.hp = random.randint(1, 5)
        monster1.move((0, random.randint(1, height - 1)))
        monster2.move((width-1, random.randint(0, 1)))
        play_again = input('Again? (y/n) ') == 'y'           


if __name__ == '__main__':
    main()
