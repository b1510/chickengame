import math

def is_present_on_line(k, grille, i):
    for e in grille[i]:
        if e == k:
            return False
    return True


def is_present_on_col(k, grille, j):
    for i, e in enumerate(grille):
        if grille[i][j] == k:
            return False
    return True


def is_present_on_block(k, grille, i, j):
    _i = i-(i % 3)
    _j = j-(j % 3)  # ou encore : _i = 3*(i/3), _j = 3*(j/3);

    for i in range(_i, _i + 3):
        for j in range(_j, _j +3):
            if grille[i][j] == k:
                return False
    return True

def is_valide(grille, position):

    if position == len(grille) * len(grille):
        return True

    i = int(position /len(grille))
    j = position % len(grille)

    if grille[i][j] != 0:
        is_valide(grille, position + 1)

    for k, e in enumerate(grille):

        if is_present_on_line(k, grille, i) and is_present_on_col(k, grille, j) and is_present_on_block(k, grille, i, j):
            grille[i][j] = k

            if is_valide(grille, position + 1):
                return True

    grille[i][j] = 0
    return False


def main():
    grille = [
        [9, 0, 0, 1, 0, 0, 0, 0, 5],
        [0, 0, 5, 0, 9, 0, 2, 0, 1],
        [8, 0, 0, 0, 4, 0, 0, 0, 0],
        [0, 0, 0, 0, 8, 0, 0, 0, 0],
        [0, 0, 0, 7, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 2, 6, 0, 0, 9],
        [2, 0, 0, 3, 0, 0, 0, 0, 6],
        [0, 0, 0, 2, 0, 0, 9, 0, 0],
        [0, 0, 1, 9, 0, 4, 5, 7, 0]
    ]
    for line in grille:
        print(line)

    print(is_valide(grille, 0))

    for line in grille:
        print(line)
    # print(grille[2][4])

    print(is_present_on_block(6, grille, 7, 7))

if __name__ == '__main__':
    main()