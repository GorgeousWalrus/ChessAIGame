from game.ChessGame import ChessGame

game = ChessGame()

def getMove():
  str_start_pos = input("Position of figure to move")
  while len(str_start_pos) > 2:
    print("Try again")
    str_start_pos = input("Position of figure to move")
  str_end_pos = input("Destination")
  while len(str_end_pos) > 2:
    print("Try again")
    str_end_pos = input("Destination")
  start_pos = (ord(str_start_pos[0])-97, int(str_start_pos[1])-1)
  end_pos = (ord(str_end_pos[0])-97, int(str_end_pos[1])-1)
  return start_pos, end_pos

while 1:
  game.printBoard()
  move = getMove()
  retval = game.move(move)
  if retval == -1:
    print("Invalid move!")
  elif retval in [1, 2]:
    print("Player", retval, 'in check!')
  elif retval in [3, 4]:
    print("Player", retval-2, 'won!')
    game.printBoard()
    break
