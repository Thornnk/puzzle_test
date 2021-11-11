# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


class Piece:
    def __init__(self, side_shapes):
        self.sides = {'left': side_shapes[0],
                      'top': side_shapes[1],
                      'right': side_shapes[2],
                      'bottom': side_shapes[3]
        }

    def check_fit(self):
        pass


p1 = Piece([0, 1, 3, 2])
print(p1.sides)
