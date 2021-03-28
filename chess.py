from game.ChessGame import ChessGame

game = ChessGame()

while 1:
  game.printBoard()
  fide_str = input("FIDE move: ")
  retval = game.move(fide_str)
  if retval == -1:
    print("Invalid move!")
  elif retval in [1, 2]:
    print("Player", retval, 'in check!')
  elif retval in [3, 4]:
    print("Player", retval-2, 'won!')
    game.printBoard()
    break
