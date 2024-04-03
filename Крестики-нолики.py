def pattern(cells):
    print("    0  1  2")
    for i in range(3):
        print(str(i) + "  ", end="")
        for j in range(3):
            print(" " + str(cells[i][j]) + " ", end="")
        print()

def win(cells):
    for i in range(3):
        if cells[i][0] == cells[i][1] == cells[i][2] != '-':
            return True
        if cells[0][i] == cells[1][i] == cells[2][i] != '-':
            return True
    if cells[0][0] == cells[1][1] == cells[2][2] != '-':
        return True
    if cells[0][2] == cells[1][1] == cells[2][0] != '-':
        return True

cells = [['-' for _ in range(3)] for _ in range(3)]
current_player = 'X'

while True:
    pattern(cells)
    row = int(input("Выберите строку (0, 1, 2): "))
    col = int(input("Выберите столбец (0, 1, 2): "))

    if cells[row][col] == '-':
        cells[row][col] = current_player

        if win(cells):
            print("Игрок", current_player, "выиграл!")
            break

        if current_player == 'X':
            current_player = 'O'
        else:
            current_player = 'X'
    else:
        print("Выберите другую клетку")