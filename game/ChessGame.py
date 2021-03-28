"""
A module for a game of chess
"""

import copy

def isOnBoard(position):
  """
  Check if the position is on the board
  Input:
    position: Tuple of Int
  Return:
    Bool
  """
  if position[0] < 0:
    return False
  if position[1] < 0:
    return False
  if position[0] > 7:
    return False
  if position[1] > 7:
    return False
  return True

class Figure:
  """Superclass for a figure on the board"""
  def __init__(self, board, position, player, value):
    self.board = board
    self.player = player
    self.position = position
    self.value = value
    self.name = '.'
    self.has_moved = False
    self.possible_moves = []
  
  def getID(self):
    """Return an ID for this figure"""
    raise NotImplementedError()

  def isValidMove(self, destination):
    """
    Check if the move is valid
    Input:
      destination: Tuple of Int     - X and Y coordinate of destination
    Return:
      Bool                          - Move is valid => True
    """
    raise NotImplementedError()

  def move(self, destination):
    """
    Move to destination
    Input:
      destination: Tuple of Int     - X and Y coordinate of destination
    Return:
      Bool                          - True: All fine, False: Invalid move
    """
    if not self.isValidMove(destination):
      return False
    self.position = destination
    self.has_moved = True
    return True

  def canMove(self):
    """
    Check if this figure has possible moves it can take
    Input:
    Return:
      Bool
    """
    for possible_move in self.possible_moves:
      destination = [self.position[0] + possible_move[0], self.position[1] + possible_move[1]]
      if self.isValidMove(destination):
        return True
    return False

class Empty(Figure):
  """Class for an empty place on the board (simplifies valid move checking)"""
  def __init__(self, board, position):
    super().__init__(board, position, -1, 0)

  def isValidMove(self, destination):
    if not isOnBoard(destination):
      return False
    return False
  
  def getID(self):
    return 0

  def move(self, destination):
    raise Exception("Cannot move")

class Pawn(Figure):
  """Class for the pawn figure"""
  def __init__(self, board, position, player):
    super().__init__(board, position, player, 1)
    self.name = 'p'
    if player == 0:
      self.possible_moves = [(0, 1), (0, 2), (1, 1), (-1, 1)]
    else:
      self.possible_moves = [(0, -1), (0, -2), (1, -1), (-1, -1)]

  def getID(self):
    return 1 + 7*self.player

  def isValidMove(self, destination):
    if not isOnBoard(destination):
      return False
    dest_figure = self.board.getFigure(destination)
    if dest_figure.player == self.player:
      return False
    if abs(destination[0] - self.position[0]) == 1:
      if(dest_figure is None
          or self.player == 0 and destination[1] != self.position[1]+1
          or self.player == 1 and destination[1] != self.position[1]-1):
        return False
    elif abs(destination[0] - self.position[0]) == 0:
      if abs(self.position[1] - destination[1]) == 2:
        if self.has_moved:
          return False
        elif(self.board.isPathClear(self.position, destination)
            and (self.player == 1 and destination[1] == self.position[1]+2
                or self.player == 2 and destination[1] == self.position[1]-2)):
          return True
      elif(self.player == 0 and destination[1] != self.position[1]+1
          or self.player == 1 and destination[1] != self.position[1]-1):
        return False
    else:
      return False
    if self.board.meansCheck(self, destination):
      return False
    return True

class Knight(Figure):
  """Class for the knight figure"""
  def __init__(self, board, position, player):
    super().__init__(board, position, player, 3)
    self.name = 'n'
    self.possible_moves = [(1,2), (2, 1), (-1, 2), (2, -1), (1, -2), (-2, 1), (-1, -2), (-2, -1)]

  def getID(self):
    return 2 + 7*self.player

  def isValidMove(self, destination):
    if not isOnBoard(destination):
      return False
    dest_figure = self.board.getFigure(destination)
    if dest_figure.player == self.player:
      return False
    if(abs(destination[1] - self.position[1]) == 2 and abs(destination[0] - self.position[0]) == 1
        or abs(destination[1] - self.position[1]) == 1 and abs(destination[0] - self.position[0]) == 2):
      return True
    if self.board.meansCheck(self, destination):
      return False
    return False

class Bishop(Figure):
  """Class for the bishop figure"""
  def __init__(self, board, position, player):
    super().__init__(board, position, player, 3)
    self.name = 'b'
    # Should suffice to check these
    self.possible_moves = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

  def getID(self):
    return 3 + 7*self.player

  def isValidMove(self, destination):
    if not isOnBoard(destination):
      return False
    if self.board.getFigure(destination).player == self.player:
      return False
    if abs(destination[0]-self.position[0]) != abs(destination[1] - self.position[1]):
      return False
    if not self.board.isPathClear(self.position, destination):
      return False
    if self.board.meansCheck(self, destination):
      return False
    return True

class Rook(Figure):
  """Class for the rook figure"""
  def __init__(self, board, position, player):
    super().__init__(board, position, player, 5)
    self.name = 'r'
    # Should suffice to check these
    self.possible_moves = [(0, -1), (0, 1), (1, 0), (-1, 0)]

  def getID(self):
    return 4 + 7*self.player

  def isValidMove(self, destination):
    if not isOnBoard(destination):
      return False
    if self.board.getFigure(destination).player == self.player:
      return False
    if abs(destination[0]-self.position[0]) != 0 and abs(destination[1] - self.position[1]) != 0:
      return False
    if not self.board.isPathClear(self.position, destination):
      return False
    if self.board.meansCheck(self, destination):
      return False
    return True

class Queen(Figure):
  """Class for the queen figure"""
  def __init__(self, board, position, player):
    super().__init__(board, position, player, 9)
    self.name = 'q'
    # Should suffice to check these
    self.possible_moves = [(0, -1), (0, 1), (1, 0), (-1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]

  def getID(self):
    return 5 + 7*self.player

  def isValidMove(self, destination):
    if not isOnBoard(destination):
      return False
    if self.board.getFigure(destination).player == self.player:
      return False
    if(abs(destination[0]-self.position[0]) != 0 and abs(destination[1] - self.position[1]) != 0
        and abs(destination[0]-self.position[0]) != abs(destination[1] - self.position[1])):
      return False
    if not self.board.isPathClear(self.position, destination):
      return False
    if self.board.meansCheck(self, destination):
      return False
    return True

class King(Figure):
  """Class for the king figure"""
  def __init__(self, board, position, player):
    super().__init__(board, position, player, 100)
    self.name = 'k'
    self.possible_moves = [(0, -1), (0, 1), (1, 0), (-1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]

  def getID(self):
    return 6 + 7*self.player

  def isValidMove(self, destination):
    if not isOnBoard(destination):
      return False
    if self.board.getFigure(destination).player == self.player:
      return False
    if(abs(self.position[0] - destination[0]) > 1
      or abs(self.position[1] - destination[1]) > 1):
      return False
    if self.board.meansCheck(self, destination):
      return False
    return True

class Board:
  """Class for the chess board"""
  def __init__(self):
    self.board = [[Empty(self, (x, y)) for x in range(8)] for y in range(8)]
    for i in range(8):
      self.board[i][1] = Pawn(self, [i, 1], 0)
      self.board[i][6] = Pawn(self, [i, 6], 1)
    self.board[0][0] = Rook(self, [0, 0], 0)
    self.board[7][0] = Rook(self, [7, 0], 0)
    self.board[0][7] = Rook(self, [0, 7], 1)
    self.board[7][7] = Rook(self, [7, 7], 1)
    self.board[1][0] = Knight(self, [1, 0], 0)
    self.board[6][0] = Knight(self, [6, 0], 0)
    self.board[1][7] = Knight(self, [1, 7], 1)
    self.board[6][7] = Knight(self, [6, 7], 1)
    self.board[2][0] = Bishop(self, [2, 0], 0)
    self.board[5][0] = Bishop(self, [5, 0], 0)
    self.board[2][7] = Bishop(self, [2, 7], 1)
    self.board[5][7] = Bishop(self, [5, 7], 1)
    self.board[3][0] = Queen(self, [3, 0], 0)
    self.board[3][7] = Queen(self, [3, 7], 1)
    self.kings = [King(self, [4, 0], 0), King(self, [4, 7], 1)]
    self.board[4][0] = self.kings[0]
    self.board[4][7] = self.kings[1]
    self.player_figures = [[], []]
    for i in range(8):
      self.player_figures[0].append(self.board[i][0])
      self.player_figures[0].append(self.board[i][1])
      self.player_figures[1].append(self.board[i][6])
      self.player_figures[1].append(self.board[i][7])

  def isPathClear(self, start_pos, end_pos):
    """
    Check if the path between the two positions is clear
    Input:
      start_pos: Tuple of Int
      end_pos:   Tuple of Int
    Return:
      Bool
    """
    if end_pos[0] >= start_pos[0]:
      x_factor = 1
    else:
      x_factor = -1
    if end_pos[1] >= start_pos[1]:
      y_factor = 1
    else:
      y_factor = -1
    # Check if there are figures in between
    if end_pos[0] == start_pos[0]:
      for j in range(1, abs(end_pos[1]-start_pos[1])):
        inter_y = start_pos[1] + y_factor * j
        if not isinstance(self.getFigure((start_pos[0], inter_y)), Empty):
          return False
    elif end_pos[1] == start_pos[1]:
      for j in range(1, abs(end_pos[0]-start_pos[0])):
        inter_x = start_pos[0] + x_factor * j
        if not isinstance(self.getFigure((inter_x, start_pos[1])), Empty):
          return False
    else:
      for i in range(1, abs(end_pos[0]-start_pos[0])):
        inter_x = start_pos[0] + x_factor * i
        inter_y = start_pos[1] + y_factor * i
        if not isinstance(self.getFigure((inter_x, inter_y)), Empty):
          return False
    return True

  def isCheck(self, player):
    """
    Determine if the player stands in check
    Input:
      player: Int
    Return:
      Bool
    """
    attacking_figures = []
    king = self.kings[player]
    # Check X direction:
    for i in range(1, king.position[0]-1):
      figure = self.getFigure([king.position[0]-i, king.position[1]])
      if figure.player == player:
        break
      if isinstance(figure, (Rook, Queen)):
        attacking_figures.append(figure)
        break
      if not isinstance(figure, Empty):
        break
    for i in range(king.position[0]+1, 8):
      figure = self.getFigure([i, king.position[1]])
      if figure.player == player:
        break
      if isinstance(figure, (Rook, Queen)):
        attacking_figures.append(figure)
        break
      if not isinstance(figure, Empty):
        break
    # Check Y direction:
    for i in range(1, king.position[1]-1):
      figure = self.getFigure([king.position[0], king.position[1]-i])
      if figure.player == player:
        break
      if isinstance(figure, (Rook, Queen)):
        attacking_figures.append(figure)
        break
      if not isinstance(figure, Empty):
        break
    for i in range(king.position[1]+1, 8):
      figure = self.getFigure([king.position[0], i])
      if figure.player == player:
        break
      if isinstance(figure, (Rook, Queen)):
        attacking_figures.append(figure)
        break
      if not isinstance(figure, Empty):
        break
    # Check Diagonals
    for i in range(1, min(king.position[0]-1, king.position[1]-1)):
      figure = self.getFigure([king.position[0]-i, king.position[1]-i])
      if figure.player == player:
        break
      if figure.isValidMove(king.position):
        attacking_figures.append(figure)
        break
      if not isinstance(figure, Empty):
        break
    for i in range(1, min(8-king.position[0], 8-king.position[1])):
      figure = self.getFigure([king.position[0]+i, king.position[1]+i])
      if figure.player == player:
        break
      if figure.isValidMove(king.position):
        attacking_figures.append(figure)
        break
      if not isinstance(figure, Empty):
        break
    for i in range(1, min(king.position[0]-1, 8-king.position[1])):
      figure = self.getFigure([king.position[0]-i, king.position[1]+i])
      if figure.player == player:
        break
      if figure.isValidMove(king.position):
        attacking_figures.append(figure)
        break
      if not isinstance(figure, Empty):
        break
    for i in range(1, min(8-king.position[0], king.position[1]-1)):
      figure = self.getFigure([king.position[0]+i, king.position[1]-i])
      if figure.player == player:
        break
      if figure.isValidMove(king.position):
        attacking_figures.append(figure)
        break
      if not isinstance(figure, Empty):
        break
    # Check for Knights
    possible_attack_positions = [(1,2), (2, 1), (-1, 2), (2, -1), (1, -2), (-2, 1), (-1, -2), (-2, -1)]
    for position in possible_attack_positions:
      figure = self.getFigure([king.position[0] + position[0], king.position[1] + position[1]])
      if figure.player == player:
        continue
      if isinstance(figure, Knight):
        attacking_figures.append(figure)
        break
    if len(attacking_figures) > 0:
      return True, attacking_figures
    return False, []

  def meansCheck(self, figure, destination):
    """
    Determine if the move would result in check for the moving player
    Input:
      figure: Object of class Figure
      destination: Tuple of Int
    Return:
      Bool
    """
    board = Board()
    board.board = copy.deepcopy(self.board)
    board.player_figures = [[], []]
    for i in range(8):
      for j in range(8):
        copy_figure = board.getFigure([i, j])
        if not isinstance(copy_figure, Empty):
          board.player_figures[copy_figure.player].append(copy_figure)
        if isinstance(copy_figure, King):
          board.kings[copy_figure.player] = copy_figure
    copy_figure = board.getFigure(figure.position)
    board.update(copy_figure, destination)
    copy_figure.position = destination
    is_check, _ = board.isCheck(figure.player)
    return is_check

  def getFigure(self, position):
    """
    Get the figure at position
    Input:
      position: Tuple of Int
    Return:
      Object of class Figure
    """
    if not isOnBoard(position):
      return Empty(self, position)
    return self.board[position[0]][position[1]]

  def update(self, figure, destination):
    """
    Update the board after a move
    Input:
      figure:       Object of class Figure
      destination:  Tuple of Int
    Return:
      None
    """
    old_position = [figure.position[0], figure.position[1]]
    old_figure = self.getFigure(destination)
    if not isinstance(old_figure, Empty):
      try:
        self.player_figures[old_figure.player].remove(old_figure)
      except ValueError:
        # Happens when called for the copy generated from meansCheck(), irrelevant case
        pass
    self.board[destination[0]][destination[1]] = figure
    self.board[old_position[0]][old_position[1]] = Empty(self, old_position)
    return old_figure

  def move(self, player, start_pos, end_pos):
    """
    Move figure to position
    Input:
      player:    Int
      start_pos: Tuple of Int
      end_pos:   Tuple of Int
    Return:
      Bool (success or invalid move)
    """
    if start_pos == end_pos:
      return False, None
    figure = self.getFigure(start_pos)
    if figure.player != player:
      return False, None
    if not figure.move(end_pos):
      return False, None
    return True, self.update(figure, end_pos)

  def isCheckmateSingle(self, player, attacking_figure):
    """
    Determine whether the attacking figure poses a checkmate situation
    Input:
      player: Int
      attacking_figure: object of class Figure
    Return:
      Bool
    """
    king = self.kings[player]
    possible_defense_positions = []
    # Get all defense positions
    if isinstance(attacking_figure, Knight):
      possible_defense_positions = [attacking_figure.position]
    else:
      x_diff = king.position[0] - attacking_figure.position[0]
      y_diff = king.position[1] - attacking_figure.position[1]
      x_factor = 1
      y_factor = 1
      if y_diff > 0:
        y_factor = -1
      if x_diff > 0:
        x_factor = -1
      if x_diff == 0:
        for y_iter in range(1, abs(king.position[1]-attacking_figure.position[1])+1):
          y_pos = king.position[1] + y_factor * y_iter
          possible_defense_positions.append([king.position[0], y_pos])
      elif y_diff == 0:
        for x_iter in range(1, abs(king.position[0]-attacking_figure.position[0])+1):
          x_pos = king.position[0] + x_factor * x_iter
          possible_defense_positions.append([x_pos, king.position[1]])
      else:
        for i in range(1, abs(king.position[0]-attacking_figure.position[0])+1):
          x_pos = king.position[0] + x_factor * i
          y_pos = king.position[1] + y_factor * i
          possible_defense_positions.append([x_pos, y_pos])
    # Check if any defense position is possible
    for position in possible_defense_positions:
      for figure in self.player_figures[player]:
        if figure.isValidMove(position):
          return False
    for move in king.possible_moves:
      destination = [king.position[0] + move[0], king.position[1] + move[1]]
      if king.isValidMove(destination):
        return False
    return True

  def isCheckmate(self, player, attacking_figures):
    """
    Check if the attacking figures create a checkmate situation
    Input:
      player: Int
      attacking_figures: List of Objects of class Figure
    """
    for figure in attacking_figures:
      if self.isCheckmateSingle(player, figure):
        return True
    return False

  def isStaleMate(self, player):
    """
    Check if current position is a stalemate
    Input:
      player: Int
    Return:
      Bool
    """
    for figure in self.player_figures[player]:
      if figure.canMove():
        return False
    return True

  def printBoard(self):
    """
    Print the board
    Input:
    Return:
    """
    for j in range(7, -1, -1):
      line = str(j+1) + '   '
      for i in range(8):
        figure = self.getFigure([i, j])
        if figure.player == 0:
          line += figure.name.upper() + ' '
        else:
          line += figure.name + ' '
      print(line)
    print('')
    print('    a b c d e f g h')

class ChessGame:
  """Class for the Chess Game"""
  def __init__(self):
    self.board = Board()
    self.current_player = 0
    self.history = []

  def printBoard(self):
    """Print the current board setup"""
    self.board.printBoard()

  def getScores(self):
    """
    Get the scores of the two players (sum of figure values)
    Input:
    Return:
      Tuple of Int
    """
    player_0_score = 0
    player_1_score = 0
    for figure in self.board.player_figures[0]:
      player_0_score += figure.value
    for figure in self.board.player_figures[1]:
      player_1_score += figure.value
    return player_0_score, player_1_score

  def isDraw(self):
    """
    Check if the current situation is a draw
    Input:
    Return:
      Bool
    """
    last_move = self.history[-1]
    if last_move == self.history[-3] and last_move == self.history[-5]:
      return True
    if self.board.isStaleMate(self.current_player):
      return True
    return False

  def undo(self):
    """
    Undo the last move
    Input:
    Return:
    """
    last_move = self.history.pop()
    moved_figure = self.board.getFigure(last_move[0][0])
    taken_figure = last_move[1]
    self.board.update(taken_figure, last_move[0][0])
    self.board.update(moved_figure, last_move[0][1])

  def getBoard(self):
    """Get a representation of the board for computer-evaluation"""
    board = [[0 for _ in range(8)] for _ in range(8)]
    for i in range(8):
      for j in range(8):
        board[i][j] = self.board.getFigure((i,j)).getID()
    return board

  def move(self, move):
    """
    Move figure to position
    Input:
      move: Tuple of Tuple of Int
    Return:
      Int
        0 : Success
        -1: Invalid Move
        1 : Player 1 in Check
        2 : Player 2 in Check
        3 : Checkmate, player 1 won
        4 : Checkmate, player 2 won
        5 : Draw
    """
    retval, taken_figure = self.board.move(self.current_player, move[0], move[1])
    if not retval:
      return -1
    self.history.append((move, taken_figure))
    if self.current_player == 1:
      self.current_player = 0
    else:
      self.current_player = 1
    is_check, attacking_figures = self.board.isCheck(self.current_player)
    if is_check:
      if self.board.isCheckmate(self.current_player, attacking_figures):
        if self.current_player == 1:
          return 3
        return 4
      if self.current_player == 1:
        return 1
      return 2
    if self.isDraw():
      return 5
    return 0
