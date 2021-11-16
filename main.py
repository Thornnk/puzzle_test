from random import shuffle


class Puzzle:
    def __init__(self, size, lines):
        self.size = size
        self.all_pieces = [Piece(i, lines[i]) for i in range(1, len(lines))]

        self.puzzle = None
        self.reset_puzzle()

        self.pieces = None
        self.reset_pieces()

    def reset_puzzle(self):
        self.puzzle = [[0 for _ in range(self.size[1])] for _ in range(self.size[0])]

    def reset_pieces(self):
        self.pieces = self.all_pieces.copy()
        shuffle(self.pieces)

    def build_puzzle(self):
        for p in self.pieces:
            for row_index, row in self.puzzle:
                for col_index, col in row:
                    if row_index == 0:
                        if p['top'] == 0:
                            if p.check_fit()


class Piece:
    def __init__(self, p_num, side_shapes):
        self.piece_num = p_num
        self.sides = {'left': side_shapes[0],
                      'top': side_shapes[1],
                      'right': side_shapes[2],
                      'bottom': side_shapes[3]}

    def check_fit(self, piece2, specific_sides):
        """
        :param piece2: Piece() object
        :param specific_sides: list of length 2 (strings with opposite sides)
        :return: boolean
        """

        return self.sides[specific_sides[0]] == piece2.sides[specific_sides[1]]

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
