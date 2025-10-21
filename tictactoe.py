board =[' '] * 9
def display_board(board):
    print(f'{board[0]} | {board[1]} | {board[2]}')
    print(f'{board[3]} | {board[4]} | {board[5]}')
    print(f'{board[6]} | {board[7]} | {board[8]}')

def win():
    if board[0] == board[1] == board[2] and board[0] != ' ':
        return True
    elif board[3] == board[4] == board[5] and board[3] != ' ':
        return True
    elif board[6] == board[7] == board[8] and board[6] != ' ':
        return True
    elif board[0] == board[3] == board[6] and board[0] != ' ':
        return True
    elif board[1] == board[4] == board[7] and board[1] != ' ':
        return True
    elif board[2] == board[5] == board[8] and board[2] != ' ':
        return True
    elif board[0] == board[4] == board[8] and board[0] != ' ':
        return True
    elif board[2] == board[4] == board[6] and board[2] != ' ':
        return True
    else:
        return False

def draw():
    if board.count(' ')  == 0:
        return True 
    else:
        return False

def is_available(position):
    return True if board[position] == ' 'else False

def insert(letter,position):
    if is_available(position):
        board[position] = letter
        display_board(board)
        if win():
            if letter == 'X':
                print('Player1 X wins')
            else:
                print('Player2 0 wins')
        else: 
            draw()
            print("It's a Draw")
    else:
        print("Position not free! Try again")
        player_move(letter)

def player_move(letter):
    while True:
        try:
            position = int(input('Enter the position to insert:')) - 1
            if position not in range(9):
                print("Invalid position! choose between 1 and 9")
                continue
            insert(letter,position)
            break
        except ValueError:
            print("Please enter a valid number!")

def tic_tac_toe():
    print('Welcome to Tic Tac Toe')
    print('Player 1: X | Player 2: 0')

while not win():
    display_board(board)
    player_move('X')
    player_move('0')
tic_tac_toe()