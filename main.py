from random import shuffle


class Puzzle:
    def __init__(self, size, lines):
        self.size = size
        self.all_pieces = [Piece(i, lines[i].split()) for i in range(1, len(lines))]

        self.puzzle = None
        self.reset_puzzle()

        self.pieces = None
        self.reset_pieces()

    def reset_puzzle(self):
        self.puzzle = [[0 for _ in range(self.size[1])] for _ in range(self.size[0])]

    def reset_pieces(self):
        self.pieces = self.all_pieces.copy()
        shuffle(self.pieces)

    def check_border_piece(self, row_ind, col_ind, piece):
        for _ in range(4):
            if row_ind == 0:
                if col_ind == 0:
                    if piece.sides['left'] == '0' and piece.sides['top'] == '0': return True
                    else: piece.turn_piece()
                elif col_ind == self.size[1]:
                    if piece.sides['top'] == '0' and piece.sides['right'] == '0': return True
                    else: piece.turn_piece()
                else:
                    if piece.sides['top'] == '0':
                        if self.puzzle[row_ind][col_ind-1] != 0:
                            if self.puzzle[row_ind][col_ind-1].sides['right'] == piece.sides['left']: return True
                    else: piece.turn_piece()
            elif row_ind == self.size[0]:
                if col_ind == 0:
                    if piece.sides['bottom'] == '0' and piece.sides['left'] == '0': return True
                    else: piece.turn_piece()
                elif col_ind == self.size[1]:
                    if piece.sides['right'] == '0' and piece.sides['bottom'] == '0': return True
                    else: piece.turn_piece()
                else:
                    if piece.sides['bottom'] == '0':
                        if self.puzzle[row_ind][col_ind-1] != 0:
                            if self.puzzle[row_ind][col_ind-1].sides['right'] == piece.sides['left']: return True
                    else: piece.turn_piece()
            else:
                if col_ind == 0:
                    if piece.sides['left'] == '0':
                        if self.puzzle[row_ind-1][col_ind] != 0:
                            if self.puzzle[row_ind-1][col_ind].sides['bottom'] == piece.sides['top']: return True
                    else: piece.turn_piece()
                else:
                    if piece.sides['right'] == '0':
                        if self.puzzle[row_ind-1][col_ind] != 0:
                            if self.puzzle[row_ind-1][col_ind].sides['bottom'] == piece.sides['top']: return True
                    else: piece.turn_piece()
        return False

    def check_inner_piece(self, row_ind, col_ind, piece):
        for _ in range(4):
            if self.puzzle[row_ind-1][col_ind] != 0 and self.puzzle[row_ind][col_ind-1] != 0:
                if self.puzzle[row_ind-1][col_ind].sides['bottom'] == piece.sides['top'] and \
                        self.puzzle[row_ind][col_ind-1].sides['right'] == piece.sides['left']: return True
            else: piece.turn_piece()
        return False

    def check_fit(self, row_ind, col_ind, piece):
        fit = list()
        # Comprueba si se trata de un borde, o si lo es, de si encaja o no
        if row_ind == 0 or row_ind == self.size[0] or col_ind == 0 or col_ind == self.size[1]:
            if self.check_border_piece(row_ind, col_ind, piece): fit.append(1)
            else: fit.append(0)

        # Comprueba si la pieza interna encaja con las de su alrededor (izquierda y arriba)
        else:
            if self.check_inner_piece(row_ind, col_ind, piece): fit.append(1)
            else: fit.append(0)

        return all(fit)

    def build_puzzle(self):

        completed = False
        while not completed:

            for row_ind, row in enumerate(self.puzzle):
                for col_ind, col in enumerate(row):
                    for p_ind, p in enumerate(self.pieces):
                        if self.check_fit(row_ind, col_ind, p):
                            self.puzzle[row_ind][col_ind] = self.pieces.pop(p_ind)
                            break

            if all([c for r in self.puzzle for c in r]): completed = True
            self.reset_puzzle()
            self.reset_pieces()
        return self.puzzle



        # for row_ind, row in enumerate(self.puzzle):
        #     for col_ind, col in enumerate(row):
        #         for p_ind, p in enumerate(self.pieces):
        #             if self.check_fit(row_ind, col_ind, p):
        #                 self.puzzle[row_ind][col_ind] = self.pieces.pop(p_ind)
        #                 break
        # if all([c for r in self.puzzle for c in r]):
        #     return self.puzzle
        # else:
        #     self.reset_puzzle()
        #     self.reset_pieces()
        #     return self.build_puzzle()


class Piece:
    def __init__(self, p_num, side_shapes):
        self.piece_num = p_num
        self.sides = {'left': side_shapes[0],
                      'top': side_shapes[1],
                      'right': side_shapes[2],
                      'bottom': side_shapes[3]}

    def turn_piece(self):
        """
        Changes the self.sides attribute values clockwise
        """

        self.sides['left'], self.sides['top'], self.sides['right'], self.sides['bottom'] = \
            self.sides['bottom'], self.sides['left'], self.sides['top'], self.sides['right']


if __name__ == '__main__':

    with open('input.txt') as f:
        all_lines = f.readlines()
    all_lines = [line.replace('\n', '') for line in all_lines]

    puzzle = Puzzle(size=tuple([int(i) for i in all_lines[0].split()]), lines=all_lines)

    puzzle.build_puzzle()

    # solution = get_solution(puzzle_size, list(all_pieces.keys()))
    # final_solution = '\n'.join([' '.join(str(num) for num in row) for row in solution])
    # print(final_solution)

    # p1 = Piece('1', [2, 5, 4, 0])
