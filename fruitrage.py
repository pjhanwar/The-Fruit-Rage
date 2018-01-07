import sys
import time
import numpy as np
import datetime
import math

global board_size
global no_of_fruits
global initial_time


def getBoard():
    fname = "input.txt"
    output_file = "output.txt"
    global board_size
    global no_of_fruits
    global initial_time
    try:
        input_file = open(fname, 'r')
        lines = input_file.readlines()
        for index, line in enumerate(lines):
            if index == 0:
                board_size = int(lines[index].strip("\n"))
                no_of_fruits = int(lines[index + 1].strip("\n"))
                initial_time = float(lines[index + 2].strip("\n"))
                board = []
                for i in range(3, board_size + 3):
                    board.append(list(lines[index + i].strip("\n")))
        input_file.close()
        return board,initial_time
    except IOError:
        fo = open(output_file, 'w')
        fo.write("FAIL\nFile not found: {}".format(fname))
        fo.close()
        sys.exit()


def calibrate(initial_time, b):
    if initial_time > 0.05:
        estimate_nodes = float(2500.0)
        estimate_nodes *= initial_time
        depth = int(math.log(estimate_nodes, b))
        return depth
    else:
        return 0


def minimax(board, initial_time):
    dmove = {}
    n = board_size
    d = dict()
    d[0] = 'A'
    d[1] = 'B'
    d[2] = 'C'
    d[3] = 'D'
    d[4] = 'E'
    d[5] = 'F'
    d[6] = 'G'
    d[7] = 'H'
    d[8] = 'I'
    d[9] = 'J'
    d[10] = 'K'
    d[11] = 'L'
    d[12] = 'M'
    d[13] = 'N'
    d[14] = 'O'
    d[15] = 'P'
    d[16] = 'Q'
    d[17] = 'R'
    d[18] = 'S'
    d[19] = 'T'
    d[20] = 'U'
    d[21] = 'V'
    d[22] = 'W'
    d[23] = 'X'
    d[24] = 'Y'
    d[25] = 'Z'

    my_moves = finding_all_moves(board)
    b = len(my_moves)
    total_game_moves = int(math.ceil(b/2))
    if total_game_moves == 0:
        total_game_moves = 1
    per_move_time = initial_time/total_game_moves
    if b == 1:
        depth = 0
    else:
        depth = calibrate(per_move_time, b)

    board_count = [[-1 for x in range(n)] for y in range(n)]
    if depth > 0:
        sq = n * n
        mid = sq / 2
        op = 0
        if initial_time >= 300:
            for x in range(n):
                for y in range(n):
                    if board[x][y] == '*':
                        board_count[x][y] = 0
                        op += 1
                    else:
                        board_count[x][y] = -1
        else:
            for x in range(n):
                for y in range(n):
                    if board[x][y] == '*':
                        board_count[x][y] = 0
                    else:
                        board_count[x][y] = -1

        for move in my_moves:
            m=0
            board_copy = [k[:] for k in board]
            board_count_copy = [k[:] for k in board_count]
            row = move[0]
            col = move[1]
            board_count_copy = replace_with_star(board_copy, board_count_copy, row, col)
            count = 0
            for i in range(0, n):
                for j in range(0, n):
                    if board_count_copy[i][j] == 1:
                        board_copy[i][j] = '*'
                        count += 1
            m += count
            board_copy = apply_gravity(board_copy)
            for i in range(n):
                for j in range(n):
                    if board_copy[i][j] == '*':
                        board_count_copy[i][j] = 0
                    else:
                        board_count_copy[i][j] = -1
            value, diff = min_turn(board_copy,board_count_copy,m,op,mid,depth-1)
            if value == 1:
                board_count_new = replace_with_star(board,board_count,move[0],move[1])
                for i in range(0, n):
                    for j in range(0, n):
                        if board_count_new[i][j] == 1:
                            board[i][j] = '*'
                board = apply_gravity(board)
                fo = open("output.txt", 'w')
                row = move[0] + 1
                letter = d[move[1]]
                fo.write(letter + repr(row) + "\n")
                for a in board:
                    fo.write("".join(map(str, a)) + "\n")
                fo.close()
                return 1
            else:
                dmove[move] = diff
                continue
        d_sorted_keys = sorted(dmove, key=dmove.get, reverse=True)
        r = d_sorted_keys[0]
        move = tuple(r)
        board_count_new = replace_with_star(board, board_count, move[0], move[1])
        for i in range(0, n):
            for j in range(0, n):
                if board_count_new[i][j] == 1:
                    board[i][j] = '*'
        board = apply_gravity(board)
        fo = open("output.txt", 'w')
        row = move[0] + 1
        letter = d[move[1]]
        fo.write(letter + repr(row) + "\n")
        for a in board:
            fo.write("".join(map(str, a)) + "\n")
        fo.close()
    else:
        move = tuple(my_moves[0])
        board_count_new = replace_with_star(board, board_count, move[0], move[1])
        for i in range(0, n):
            for j in range(0, n):
                if board_count_new[i][j] == 1:
                    board[i][j] = '*'
        board = apply_gravity(board)
        fo = open("output.txt", 'w')
        row = move[0] + 1
        letter = d[move[1]]
        fo.write(letter + repr(row) + "\n")
        for a in board:
            fo.write("".join(map(str, a)) + "\n")
        fo.close()
        return 1


def max_turn(board,board_count,mypoint,opppoint,mid,depth):
    n = board_size
    my_moves = finding_all_moves(board)
    for move in my_moves:
        m = mypoint
        op = opppoint
        board_copy = [k[:] for k in board]
        board_count_copy = [k[:] for k in board_count]
        row = move[0]
        col = move[1]
        board_count_copy = replace_with_star(board_copy, board_count_copy, row, col)
        count = 0
        for i in range(0, n):
            for j in range(0, n):
                if board_count_copy[i][j] == 1:
                    board_copy[i][j] = '*'
                    count += 1
        m += count
        board_copy = apply_gravity(board_copy)
        for i in range(n):
            for j in range(n):
                if board_copy[i][j] == '*':
                    board_count_copy[i][j] = 0
                else:
                    board_count_copy[i][j] = -1
        if m < mid and depth >= 0 and not gameover(board):
            value,diff = min_turn(board_copy,board_count_copy,m,op,mid,depth-1)
            if value == 0:
                return 0,diff
            else:
                return 1,diff
        else:
            diff = m - op
            if diff > 0:
                return 1,diff
            elif diff == 0:
                return 1,diff
            else:
                return 0,diff


def min_turn(board,board_count,mypoint,opppoint,mid,depth):
    n = board_size
    global dmove
    opp_moves = finding_all_moves(board)
    for move in opp_moves:
        m = mypoint
        op = opppoint
        board_copy = [k[:] for k in board]
        board_count_copy = [k[:] for k in board_count]
        row = move[0]
        col = move[1]
        board_count_copy = replace_with_star(board_copy,board_count_copy, row, col)
        count = 0
        for i in range(0, n):
            for j in range(0, n):
                if board_count_copy[i][j] == 1:
                    board_copy[i][j] = '*'
                    count +=1
        op += count
        board_copy = apply_gravity(board_copy)
        for i in range(n):
            for j in range(n):
                if board_copy[i][j] == '*':
                    board_count_copy[i][j] = 0
                else:
                    board_count_copy[i][j] = -1
        if mid > op and depth >= 0 and not gameover(board_copy):
            value, diff = max_turn(board_copy,board_count_copy,m,op,mid,depth-1)
            if value == 0:
                return 0,diff
            else:
                continue
        else:
            diff = m - op
            if diff > 0:
                continue
            elif diff == 0:
                continue
            else:
                return 0,diff
    return 1,0


def replace_with_star(board, board_count, row, col):
    n = board_size

    if board_count[row][col] == -1:
        board_count[row][col] = 1

    if col < n - 1 and board[row][col] == board[row][col + 1] and board_count[row][col + 1] == -1:
        board_count[row][col + 1] = 1
        board_count = replace_with_star(board, board_count, row, col+1)

    if row < n - 1 and board[row][col] == board[row + 1][col] and board_count[row+1][col] == -1:
        board_count[row + 1][col] = 1
        board_count = replace_with_star(board, board_count, row+1, col)

    if row > 0 and board[row][col] == board[row - 1][col] and board_count[row - 1][col] == -1:
        board_count[row - 1][col] = 1
        board_count = replace_with_star(board, board_count, row-1, col)

    if col > 0 and board[row][col] == board[row][col - 1] and board_count[row][col - 1] == -1:
        board_count[row][col - 1] = 1
        board_count = replace_with_star(board, board_count, row, col-1)

    return board_count


def finding_all_moves(board):
    n = board_size
    board_count = [[-1 for x in range(n)] for y in range(n)]
    d = {}
    for i in range(0, n):
        for j in range(0, n):
            if board_count[i][j] == -1 and board[i][j] != '*':
                board_count[i][j] = 1
                max_count, board_count = find_adjacent(board, board_count, i, j, 1)
                a = list()
                a.append(i)
                a.append(j)
                d[tuple(a)] = max_count
    d_sorted_keys = sorted(d, key=d.get, reverse=True)
    return d_sorted_keys


def find_adjacent(board, board_count, row, col, count):
    n = board_size
    if col < n - 1 and board[row][col] == board[row][col + 1] and board_count[row][col+1] == -1:
        count += 1
        board_count[row][col + 1] = 1
        count, board_count = find_adjacent(board, board_count, row, col + 1, count)

    if row < n - 1 and board[row][col] == board[row + 1][col] and board_count[row + 1][col] == -1:
        count += 1
        board_count[row + 1][col] = 1
        count, board_count = find_adjacent(board, board_count, row + 1, col, count)

    if row > 0 and board[row][col] == board[row - 1][col] and board_count[row - 1][col] == -1:
        board_count[row - 1][col] = 1
        count += 1
        count, board_count = find_adjacent(board, board_count, row - 1, col, count)

    if col > 0 and board[row][col] == board[row][col - 1] and board_count[row][col-1] == -1:
        board_count[row][col-1] = 1
        count += 1
        count, board_count = find_adjacent(board, board_count, row, col - 1, count)

    return count, board_count


def apply_gravity(board):
    n = board_size
    for j in range(0, n):
        count = 0
        a = []
        for i in range(0, n):
            if board[i][j] == '*':
                count += 1
            else:
                a.append(board[i][j])
                continue
        for i in range(0, count):
            board[i][j] = '*'
        itr = 0
        for i in range(count, n):
            board[i][j] = a[itr]
            itr += 1
    return board


def gameover(board):
    val = np.array(board)
    if (val == '*').all():
        return True
    return False


def main():
    board, initial_time = getBoard()
    minimax(board,initial_time)


if __name__ == '__main__':
    main()
