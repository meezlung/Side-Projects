import itertools
import random
from string import ascii_uppercase

flag_coordinates = []
mines_match = 0

def generate_mines():
    return random.sample(list(itertools.product(range(7), repeat=2)), k=8)

# Initializes the game board with hidden cells and stores mine locations
def create_board(size):
    board = [['.'] * size for _ in range(size)] # Board by 7 x 7 
    mine_locations = generate_mines() # Kung saan nakaposition ung mines
    
    for mine in mine_locations:
        board[mine[1]][mine[0]] = "!"    

    return board, mine_locations

# Calculates the number of mines surrounding a cell
def count_mines(board, x, y):
    count = 0
    for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(board) and 0 <= ny < len(board[0]) and board[ny][nx] == '!':
            count += 1
    return count

# Prints the game board
def print_board(board, revealed=False):
    size = len(board)
    
    # Print column labels
    print("   " + " ".join(ascii_uppercase[:size]))

    for i, row in enumerate(board):
        print(str(i + 1).rjust(2) + " ", end='')

        for x in range(size):
            cell = board[i][x]
            if cell == '!':
                if revealed:
                    print('! ', end='')
                else:
                    print('F ', end=' ')  # Display flags for mines
            else:
                print(cell, end=' ')
        print()

def check_coordinates_are_valid(x, y):
    return 0 <= x < 7 and 0 <= y < 7

def flag_cell(board, x, y):
    if board[y][x] != 'F':
        board[y][x] = 'F'
    else:
        board[y][x] = '.'

def run_game(size, mines_match, flag_coordinates):
    board, mine_locations = create_board(size)
    revealed_board = [['.'] * size for _ in range(size)]
    flags_placed = 0

    while True:
        print_board(revealed_board)
        generate_mines()
        print(""" 
Controls
[O] Open a Cell
[F] Flag/Unflag a Cell
[CTRL + C] Exit the Game
        """)
        choice = input("Enter choice: ").upper()
        move = input("Give a coordinate ([A-G][1-7]): ")
        
        translator = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6}
    
        if move[0] == 'Q':
            break

        if choice == 'F' or choice == 'O':
            if choice == 'F' and len(move) == 2:
                
                x, y = translator[move[0]], int(move[1]) - 1
                flag_coordinates.append((x, y))
                print("Chosen coordinate: ", x, y)

                if check_coordinates_are_valid(x, y) and revealed_board[y][x] == '.':
                    flag_cell(revealed_board, x, y)
                    flags_placed += 1
                    if (x, y) in mine_locations:
                        mines_match += 1

                elif check_coordinates_are_valid(x, y) and revealed_board[y][x] == 'F':
                    flag_cell(revealed_board, x, y)
                    
                    flag_index = flag_coordinates.index((x, y))
                    print(flag_index)
                    
                    del flag_coordinates[flag_index]
                    del flag_coordinates[flag_index]

                else:
                    print("Invalid coordinate. ")       
                          
            elif choice == 'O' and len(move) == 2:

                x, y = translator[move[0]], int(move[1]) - 1
                print(x, y)

                if check_coordinates_are_valid(x, y):
                    if board[y][x] == '!':
                        print("Game Over!")
                        break
                    elif revealed_board[y][x] == '.':
                        count = count_mines(board, x, y)
                        if count == 0:
                            flood_fill(revealed_board, x, y, board)
                        else:
                            revealed_board[y][x] = str(count)
                else:
                    print("Invalid coordinate.")
            else:
                print("Invalid coordinate.")
        else:
            print("Invalid choice.")

        # Answers
        # print('Number of Mines: ', len(mine_locations))
        # print('Number of Flags: ', len(flag_coordinates))
        # print('Flag coordinates: ', flag_coordinates)
        # print('Mine locations: ', mine_locations)
        # print('Mines left: ', len(mine_locations) - mines_match)
        
        if len(flag_coordinates) == len(mine_locations) and sorted(flag_coordinates) == sorted(mine_locations):
            print("YOU WIN")
            break

        elif len(flag_coordinates) == len(mine_locations) and sorted(flag_coordinates) == sorted(mine_locations):
            print("YOU LOSE")
            break

    print_board(board, revealed=True)
    
# Recursively flood fills empty spaces
def flood_fill(revealed_board, x, y, board):
    if 0 <= x < len(revealed_board) and 0 <= y < len(revealed_board[0]) and revealed_board[y][x] == '.':
        count = count_mines(board, x, y)
        revealed_board[y][x] = str(count)
        if count == 0:
            for a, b in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]: # Check adjacents of that coordinate
                flood_fill(revealed_board, x + a, y + b, board)

run_game(7, mines_match, flag_coordinates)
generate_mines()
