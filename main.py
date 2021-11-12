from random import shuffle


class Piece:
    def __init__(self, p_num, side_shapes):
        self.p_num = p_num
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


class Puzzle:
    def __init__(self, size, lines):
        self.size = size

        self.all_pieces = self.parse_lines(lines)
        self.corners, self.borders, self.inner_body = list(), list(), list()
        self.separate_pieces()

        self.puzzle = [[0 for _ in range(size[1])] for _ in range(self.size[0])]

    @staticmethod
    def parse_lines(lines):
        pcs = dict()
        for i in range(1, len(lines)):
            pcs[i] = Piece(f'piece_{i}', lines[i].split())
        return pcs

    def separate_pieces(self):
        for key in self.all_pieces:
            piece = list(self.all_pieces[key].sides.values())
            if piece.count('0') == 2: self.corners.append(key)
            elif piece.count('0') == 1: self.borders.append(key)
            elif piece.count('0') == 0: self.inner_body.append(key)
            else: raise Exception(f'The piece {self.all_pieces[key]} is not valid.')
        print(self.corners, self.borders, self.inner_body)

    def build_corners(self):
        piece0, piece1, piece2, piece3 = self.all_pieces[self.corners[0]], self.all_pieces[self.corners[1]],\
                                         self.all_pieces[self.corners[2]], self.all_pieces[self.corners[3]]
        while piece0.sides['left'] != '0' or piece0.sides['top'] != '0': piece0.turn_piece()
        while piece1.sides['top'] != '0' or piece1.sides['right'] != '0': piece1.turn_piece()
        while piece2.sides['right'] != '0' or piece2.sides['bottom'] != '0': piece2.turn_piece()
        while piece3.sides['bottom'] != '0' or piece3.sides['left'] != '0': piece3.turn_piece()

        self.puzzle[0][0], self.puzzle[0][-1] = self.corners[0], self.corners[1]
        self.puzzle[-1][0], self.puzzle[-1][-1] = self.corners[2], self.corners[3]

    def build_borders(self):

        def find_socket(pc_ind):
            pc = self.all_pieces[pc_ind]
            for row_ind, row in enumerate(self.puzzle):
                for col_ind, col in enumerate(row):
                    if col == '0':
                        left_index = self.puzzle[row_ind][col_ind-1] if 0 < col_ind else None
                        right_index = self.puzzle[row_ind][col_ind+1] if col_ind < len(row) else None
                        left_piece = self.all_pieces[left_index]
                        right_piece = self.all_pieces[right_index]
                        for _ in range(4):
                            if row_ind == 0:
                                if pc.sides['top'] == '0' and pc.check_fit(left_piece, ['left', 'right']):
                                    self.puzzle[row_ind][col_ind] = pc_ind
                                    return
                                else: pc.turn_piece()
                            elif row_ind == len(self.puzzle):
                                if pc.sides['bottom'] == '0':
                                    self.puzzle[row_ind][col_ind] = pc_ind
                                    return
                                else: pc.turn_piece()
                            else:
                                if col_ind == 0:
                                    if pc.sides['bottom'] == '0':
                                        self.puzzle[row_ind][col_ind] = pc_ind
                                        return
                                    else: pc.turn_piece()
                        shuffle(self.borders)
                        return 'reset'

        for piece_index in self.borders:
            response = find_socket(piece_index)
            if response == 'reset': return self.build_borders()

    def build_inner_body(self):
        pass

    def build_puzzle(self):
        self.build_corners()
        self.build_borders()
        self.build_inner_body()


if __name__ == '__main__':

    with open('input.txt') as f:
        all_lines = f.readlines()
    all_lines = [line.replace('\n', '') for line in all_lines]

    puzzle = Puzzle(tuple([int(i) for i in all_lines[0].split()]), all_lines)

    puzzle.build_puzzle()

    # solution = get_solution(puzzle_size, list(all_pieces.keys()))
    # final_solution = '\n'.join([' '.join(str(num) for num in row) for row in solution])
    # print(final_solution)

    # p1 = Piece('1', [2, 5, 4, 0])







# def get_solution(size, pieces):
#     """
#     Params:
#     size: 2 element tuple (width and height)
#     pieces: list with the pieces numbers
#
#     Returns:
#     The puzzle solution as a string of the given size if exists else None
#     """
#
#     pcs = pieces
#     result = list()
#     for r in range(1, size[0]+1):
#         if len(result) < size[1]:
#             row = []
#             for piece_num in pcs:
#                 if len(row) < size[0]:
#                     if not result:
#                         if not row: row.append(piece_num)
#                         else:
#                             for _ in range(4):
#                                 if all_pieces[row[-1]].check_fit(all_pieces[piece_num], ['right', 'left']):
#                                     row.append(piece_num)
#                                     break
#                                 else:
#                                     all_pieces[piece_num].turn_piece()
#                     else:
#                         if not row:
#                             if all_pieces[result[-1][0]].check_fit(all_pieces[piece_num], ['bottom', 'top']):
#                                 row.append(piece_num)
#                         else:
#                             for _ in range(4):
#                                 if all_pieces[result[-1][0]].check_fit(all_pieces[piece_num], ['bottom', 'top']) \
#                                         and all_pieces[row[-1]].check_fit(all_pieces[piece_num], ['right', 'left']):
#                                     row.append(piece_num)
#                                     break
#                                 else:
#                                     all_pieces[piece_num].turn_piece()
#                 else: break
#             if len(row) == size[0]:
#                 result.append(row)
#         else: break
#     if len(result) == size[1]:
#         return result
#     else:
#         shuffle(pcs)
#         return get_solution(size, pcs)