import random


def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False

    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False

    return True


def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True


def print_board(board):
    for row in board:
        print(" ".join(str(num) if num != 0 else '.' for num in row))


def generate_sudoku():
    board = [[0] * 9 for _ in range(9)]
    for i in range(0, 9, 3):
        fill_diagonal_box(board, i, i)
    solve_sudoku(board)
    remove_numbers(board, 40)
    return board


def fill_diagonal_box(board, row, col):
    numbers = list(range(1, 10))
    random.shuffle(numbers)
    for i in range(3):
        for j in range(3):
            board[row + i][col + j] = numbers.pop()


def remove_numbers(board, num_remove):
    attempts = num_remove
    while attempts > 0:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        while board[row][col] == 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
        backup = board[row][col]
        board[row][col] = 0

        copy_board = [r[:] for r in board]
        if not solve_sudoku(copy_board):
            board[row][col] = backup
        else:
            attempts -= 1


def user_input(board):
    while True:
        print("\nEnter your move in the format 'row col number' (e.g., 1 3 5).")
        print("Type 'remove row col' to remove a number (e.g., 'remove 1 3').")
        print("Type 'solve' to see the solution or 'quit' to exit.")
        user_input = input("Your move: ").strip()

        if user_input.lower() == 'solve':
            return True
        elif user_input.lower() == 'quit':
            print("Exiting the game. Goodbye!")
            return False
        elif user_input.lower().startswith('remove'):
            try:
                _, row, col = user_input.split()
                row, col = int(row) - 1, int(col) - 1  # Adjust for 0-indexed board
                if 0 <= row < 9 and 0 <= col < 9 and board[row][col] != 0:
                    board[row][col] = 0
                    print_board(board)
                else:
                    print("Invalid removal. Please choose a cell that contains a number.")
            except ValueError:
                print("Invalid input for removal. Please use the format 'remove row col'.")
        else:
            try:
                row, col, num = map(int, user_input.split())
                if 1 <= row <= 9 and 1 <= col <= 9 and 1 <= num <= 9:
                    row -= 1  # Adjust for 0-indexed board
                    col -= 1
                    if board[row][col] == 0 and is_valid(board, row, col, num):
                        board[row][col] = num
                        print_board(board)
                    else:
                        print("Invalid move. Try again.")
                else:
                    print("Please enter numbers between 1 and 9.")
            except ValueError:
                print("Invalid input. Make sure to enter row, column, and number separated by spaces.")


def main():
    board = generate_sudoku()
    print("Generated Sudoku Puzzle:")
    print_board(board)

    if user_input(board):
        print("\nSolving the Sudoku automatically...")
        if solve_sudoku(board):
            print("\nSolved Sudoku:")
            print_board(board)
        else:
            print("No solution exists for the provided board.")


if __name__ == "__main__":
    main()
