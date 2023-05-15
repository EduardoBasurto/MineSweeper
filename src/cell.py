
class Cell():
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.clicked = False
        self.bombed = False
        self.flagged = False
        self.content = 0
        self.color = {
            0 : (255, 255, 255),
            1 : (0, 0, 255),       # BLUE
            2 : (0, 255, 0),      # GREEN
            3 : (250, 253, 15),  # YELLOW
            4 : (255, 0, 0)         # RED
        }

    def __repr__(self) -> str:
        return str(self.clicked)

    def get_color(self):
        return self.color.get(self.content, (0, 0, 0))

    def add_one(self):
        self.content += 1

    def bombed_cell(self):
        self.bombed = True
        self.content = 'X'

    def set_neighbors(self, neighbors):
        self.neighbors = neighbors

    def clicked_cell(self):
        self.clicked = True

    def unclicked_cell(self):
        self.clicked = False

    def saved_cell(self):
        self.clicked = True
        self.flagged = True
    
    def unsaved_cell(self):
        self.clicked = False
        self.flagged = False
