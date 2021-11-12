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


def get_solution(size, pieces):
    """
    Params:
    size: 2 element tuple (width and height)
    pieces: list with the pieces numbers

    Returns:
    The puzzle solution as a string of the given size if exists else None
    """

    pcs = pieces
    result = list()
    for r in range(1, size[0]+1):
        if len(result) < size[1]:
            row = []
            for piece_num in pcs:
                if len(row) < size[0]:
                    if not result:
                        if not row: row.append(piece_num)
                        else:
                            for _ in range(4):
                                if all_pieces[row[-1]].check_fit(all_pieces[piece_num], ['right', 'left']):
                                    row.append(piece_num)
                                    break
                                else:
                                    all_pieces[piece_num].turn_piece()
                    else:
                        if not row:
                            if all_pieces[result[-1][0]].check_fit(all_pieces[piece_num], ['bottom', 'top']):
                                row.append(piece_num)
                        else:
                            for _ in range(4):
                                if all_pieces[result[-1][0]].check_fit(all_pieces[piece_num], ['bottom', 'top']) \
                                        and all_pieces[row[-1]].check_fit(all_pieces[piece_num], ['right', 'left']):
                                    row.append(piece_num)
                                    break
                                else:
                                    all_pieces[piece_num].turn_piece()
                else: break
            if len(row) == size[0]:
                result.append(row)
        else: break
    if len(result) == size[1]:
        return result
    else:
        shuffle(pcs)
        return get_solution(size, pcs)


if __name__ == '__main__':

    with open('input.txt') as f:
        lines = f.readlines()
    lines = [l.replace('\n', '') for l in lines]
    puzzle_size = tuple([int(i) for i in lines[0].split()])

    all_pieces = dict()
    for i in range(1, len(lines)):
        all_pieces[i] = Piece(f'piece_{i}', lines[i].split())

    solution = get_solution(puzzle_size, list(all_pieces.keys()))
    final_solution = '\n'.join([' '.join(str(num) for num in row) for row in solution])
    print(final_solution)

    # p1 = Piece('1', [2, 5, 4, 0])
