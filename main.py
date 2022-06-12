import turtle as T
import random

T.tracer(0)
T.hideturtle()

OCEAN_COLOR = "#2da1fa"
SHIP_COLOR = "#fff45b"
HIT_COLOR = "red"
MISS_COLOR = "white"

RED_TEXT = "\u001b[31m"
GREEN_TEXT = "\u001b[32;1m"
RESET = "\u001b[0m"

NUM_ROWS = 10
MARKER_SIZE = 7
SQUARE_SIZE = 30
LETTERS = "ABCDEFGHIJ"
DIRS = ("left", "right", "up", "down")


# position to draw board in center
START_X = -(33 * NUM_ROWS) - 30
START_Y = (33 * NUM_ROWS) / 2

# ship name and ship length
game_ships = {
  "carrier": 5,
  "battleship": 4,
  "cruiser": 3,
  "submarine": 3,
  "destroyer": 2
}


class Player:
  def __init__(self, name):
    self.name = name
    self.main_board = [["ocean" for j in range(NUM_ROWS)] for i in range(NUM_ROWS)]
    self.shot_board = [["ocean" for j in range(NUM_ROWS)] for i in range(NUM_ROWS)]
    self.ship_health = {name:health for name, health in game_ships.items()}
    self.ships_sunk = 0

  
  def draw_board(self, board, x, y):
    for row in range(NUM_ROWS): # label rows and cols
      draw_text(x-15, y-28-(SQUARE_SIZE+3)*row, LETTERS[row])
      draw_text(x+15+(SQUARE_SIZE+3)*row, y+3, row)
   
      for col in range(NUM_ROWS): # draw ocean/ship
        if "ocean" in board[row][col]:
          T.color(OCEAN_COLOR)
        else:
          T.color(SHIP_COLOR)
        draw_square(x+(SQUARE_SIZE+3)*col, y-(SQUARE_SIZE+3)*row)

        if "H" in board[row][col]: # draw marker
          T.color(HIT_COLOR)
          draw_marker(x+(SQUARE_SIZE+3)*col+15, y -(SQUARE_SIZE+3)*row-22)
        elif "M" in board[row][col]:
          T.color(MISS_COLOR)
          draw_marker(x+(SQUARE_SIZE+3)*col+15, y-(SQUARE_SIZE+3)*row-22)
          
    T.update()



  def draw_stats(self):
    draw_text(-0.575*START_X, START_Y - 380, 
      "SHIPS SUNK: " + str(self.ships_sunk))

  
  def place_ship(self, row, col, direction, ship_name, n):
    if not (0 <= row < NUM_ROWS) or not (0 <= col < NUM_ROWS): # 1 - out of range
      return False
      
    if self.main_board[row][col] != "ocean":  # 2 - space isn't empty
      return False
  
    if n == 1:  # 3 - successfully found enough ocean spaces
      self.main_board[row][col] = ship_name # place tail
      return True
  
    # recursive calls
    if direction == "right":
      valid = self.place_ship(row, col+1, "right", ship_name, n-1)
    elif direction == "left":
      valid = self.place_ship(row, col-1, "left", ship_name, n-1)
    elif direction == "down":
      valid = self.place_ship(row+1, col, "down", ship_name, n-1)
    else:
      valid = self.place_ship(row-1, col, "up", ship_name, n-1)
  
    if valid:  # place rest of body
      self.main_board[row][col] = ship_name
      return True


  def setup(self, auto=False):
    for ship_name, ship_length in game_ships.items():
      while True:
        if auto:
          row = random.randint(0,9)
          col = random.randint(0,9)
          direction = random.choice(DIRS)
        else:
          self.draw_board(self.main_board, START_X/2, START_Y)
          choice = input(f"To place your {ship_name.upper()} (length {ship_length}), type the location for the front of the ship and the direction the body should extend in.\nExample: H2 right: ")
    
          try:  # validate input
            row = LETTERS.index(choice[0:1].upper())
            col = int(choice[1:2])
            direction = choice[3:]
          except:
            print(f"\n{RED_TEXT}INVALID INPUT, TRY AGAIN.{RESET}")
            continue

        # place ship
        if direction in DIRS and \
        self.place_ship(row, col, direction, ship_name, ship_length):
          if not auto:
            print(f"\n{GREEN_TEXT}PLACEMENT SUCCESSFUL!{RESET}")
          break      
        else:
          if not auto:
            print(f"\n{RED_TEXT}INVALID POSITION, TRY AGAIN.{RESET}")
            
  
  def attack(self, opponent, auto=False):
    while True:
      if auto:  # attack random position
        row = random.randint(0, NUM_ROWS-1)
        col = random.randint(0, NUM_ROWS-1)
      else:
        choice = input("\nENTER A LOCATION TO ATTACK: "); print()
        try:
          row = LETTERS.index(choice[0].upper())
          col = int(choice[1])
        except:
          print(f"{RED_TEXT}INVALID INPUT, TRY AGAIN.{RESET}")
          continue
      
      target = opponent.main_board[row][col]
      
      # can't attack the same position more than once
      if "H" in target or "M" in target:
        if not auto:
          print(f"{RED_TEXT}INVALID POSITION, TRY AGAIN.{RESET}")
        
      elif opponent.main_board[row][col] == "ocean":  # missed shot
        opponent.main_board[row][col] += "M"
        self.shot_board[row][col] += "M"
        print(f"{self.name} MISSED!")
        return
        
      else:  # hit shot
        opponent.ship_health[target] -= 1
        opponent.main_board[row][col] += "H"
        self.shot_board[row][col] += "H"
        print(f"{RED_TEXT}{self.name} HIT {opponent.name}'s {target.upper()}!{RESET}")
  
        if opponent.ship_health[target] == 0:  # sunken ship
          print(f"{RED_TEXT}{self.name} SANK {opponent.name}'s {target.upper()}!{RESET}")
          self.ships_sunk += 1
  
        return


def draw_square(x, y):
  T.penup(); T.goto(x,y)
  T.setheading(0)
  T.pendown()
  T.begin_fill()
  for i in range(4):
    T.fd(30)
    T.rt(90)
  T.end_fill()


def draw_text(x, y, text):
  T.penup(); T.goto(x, y)
  T.color(OCEAN_COLOR)
  T.write(text, align="center", font=("Arial", 18, "normal"))


def draw_marker(x, y):
  T.penup(); T.goto(x,y)
  T.setheading(0)
  T.pendown()
  T.begin_fill()
  T.circle(MARKER_SIZE)
  T.end_fill()


def main():
  print(f"{GREEN_TEXT} ** WELCOME TO BATTLESHIP **{RESET}\n")
  player1 = Player(input("ENTER YOUR NAME: "))
  player2 = Player("bot")
  player1.setup()
  player2.setup(True)
 
  
  def game_over():
    if player1.ships_sunk == len(game_ships):
      print(f"\n{GREEN_TEXT}{player1.name} WINS!{RESET}")
      return True
    elif player2.ships_sunk == len(game_ships):
      print(f"\n{GREEN_TEXT}{player2.name} WINS!{RESET}")
    return False


  T.clear()
  player1.draw_board(player1.main_board, START_X, START_Y)
  player1.draw_board(player1.shot_board, -0.1*START_X, START_Y)
  player1.draw_stats()
  

  while not game_over():  # main loop
    player1.attack(player2)
    player2.attack(player1, True)
    T.clear()
    player1.draw_board(player1.main_board, START_X, START_Y)
    player1.draw_board(player1.shot_board, -0.1*START_X, START_Y)
    player1.draw_stats()



main()
