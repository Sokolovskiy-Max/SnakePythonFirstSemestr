from Rd_Pt_Text import *


class HighScores:
    def __init__(self, table):
        self.hs_table = table

    def update(self, name, scores):
        self.hs_table[name] = scores

    def print(self, x, y):
        step_x = 250
        step_y = 30

        for name, scores in self.hs_table.items():
            print_text(name, x, y)
            x += step_x
            print_text(str(scores), x, y)
            x -= step_x
            y += step_y
