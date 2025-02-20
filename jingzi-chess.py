#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    :   jingzi-chess.py
@Time    :   2023/06/06 13:37:59
@Author  :   Levi Liu
@Version :   1.0
@Site    :   https://www.lvbibir.cn
@Desc    :   None
"""

import os


def print_matrix(matrix: list):
    """根据给定的矩阵列表打印棋盘"""
    os.system("clear")
    for index_row, row in enumerate(matrix):
        for index_col, col in enumerate(row):
            if index_col != len(row) - 1:
                print(col, end="|")
            else:
                print(col)
        if index_row != len(matrix) - 1:
            print("-+" * (len(row) - 1) + "-")


def who_win(matrix: list, row_index: int, col_index: int):
    """传入九宫格矩阵和修改的位置, 判断是否满足获胜条件"""
    # 判断横向
    if len(set(matrix[row_index])) == 1:
        return True
    # 判断纵向
    elif len(set([lst[col_index] for lst in matrix])) == 1:
        return True
    # 判断斜向
    elif matrix[1][1] != " ":
        if matrix[0][0] == matrix[1][1] == matrix[2][2]:
            return True
        elif matrix[0][2] == matrix[1][1] == matrix[2][0]:
            return True
    return False


def play_game():
    init_matrix = [[" "] * 3 for _ in range(3)]
    begin = True
    while begin:
        curr_matrix = init_matrix.copy()
        begin = False
        turn = "x"
        counter = 0
        print_matrix(curr_matrix)
        while counter < 9:
            counter += 1
            # 检查用户输入
            while True:
                user_input = input(
                    f"this is {turn}'s round, please input location (1-9): "
                )
                # 判断是否为 1-9 之间的正整数
                if (
                    not user_input.isdigit()
                    or int(user_input) < 1
                    or int(user_input) > 9
                ):
                    print("please input a number in 1-9 !")
                else:
                    move_number = int(user_input) - 1
                    row_index, col_index = (move_number // 3), (move_number % 3)
                    # 判断是否为已占用的格子
                    if curr_matrix[row_index][col_index] == " ":
                        break
            curr_matrix[row_index][col_index] = turn
            print_matrix(curr_matrix)
            if who_win(matrix=curr_matrix, row_index=row_index, col_index=col_index):
                print(f"{turn} win!")
                break
            if turn == "x":
                turn = "o"
            else:
                turn = "x"


def main():
    play_game()
    while True:
        want_continue = input("Do you want play time game again? (yes | no): ")
        if want_continue == "yes":
            play_game()
        elif want_continue == "no":
            break


if __name__ == "__main__":
    main()
