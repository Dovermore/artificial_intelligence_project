import tkinter

# window size (fixed, but you can adjust here)
H, W = 360, 640

def main():
    root = tkinter.Tk()
    root.title('HexSlider')
    root.wm_resizable(0,0) # prevent resizing
    canv = BoardViewCanvas(root)
    
    # begin!
    root.mainloop()

class Color:
    BG = "#663300"
    FG = "#ffd9b3"
    HL = "#ffe6cc"
    LINES = "#663300"
    STONE = "#fff2e6"
    RED   = "#cc3300"
    GREEN = "#339966"
    BLUE  = "#003399"
    BLACK = "#000000"
    NONE  = ""

# hex shape flat
FH, FW = 0.866, 1
HEX_F = [(-FW/2,0),(-FW/4,-FH/2),(FW/4,-FH/2),(FW/2,0),(FW/4,FH/2),(-FW/4,FH/2)]
# hex shape pointy
PH, PW = 1, 0.866
HEX_P = [(-PW/2,-PH/4),(0,-PH/2),(PW/2,-PH/4),(PW/2,PH/4),(0,PH/2),(-PW/2,PH/4)]

class BoardViewCanvas(tkinter.Canvas):

    def __init__(self, root):
        super().__init__(root, width=W, height=H, background=Color.BG, 
            highlightthickness=0)
        self.root = root

        # set up state
        self.initialise()
        # # bind keypresses
        self.bind("<Button-1>", self.clicked)
        
        # pack into interface
        self.pack()
    
    # called in the beginning
    def initialise(self):
        # build game board
        self.board = Board(self)
        self.button = ExportButton(self, self.board, self.root)

    def clicked(self, event):
        click = self.find_withtag(tkinter.CURRENT)
        if len(click):
            (theid,) = click
            if theid in self.board.hexid:
                thehex = self.board.hexid[theid]
                print(f'clicked hex (q={thehex.q}, r={thehex.r}).')
                self.board.cycle(thehex.q, thehex.r)
                return
            elif theid == self.button.id:
                thebutton = self.button
                print(f'clicked the {thebutton.name} button!')
                thebutton.click()
                return
        print('clicked nothing.')

with open("template.tex") as templatefile:
    TEMPLATE = templatefile.read()

class ExportButton:
    def __init__(self, canvas, board, root):
        self.name = 'Export'
        self.root = root
        self.board = board

        # render the button (a hexagon):
        D = min(H, W)
        coordinates = transform(HEX_F, (0.8*W, 0.8*H), (0.2*D, 0.2*D))
        self.id      = canvas.create_polygon(coordinates, fill=Color.FG)
        self.labelid = canvas.create_text((0.8*W, 0.8*H), text="Export",
                fill=Color.BG, state=tkinter.DISABLED)

    def click(self):
        tikz = self.render_to_tikz(self.board)
        print(tikz)
    def render_to_tikz(self, board):
        block_coord_strs = []
        piece_coord_strs = []
        for hq, hr in board.hexes:
            p = board.pieces[hq, hr]
            if p.col == 'BLOCK':
                block_coord_strs.append(f"{hq}/{hr}")
            elif p.col in {'R', 'G', 'B'}:
                piece_coord_strs.append(f"{hq}/{hr}/{p.col}")
        all_block_coords = ','.join(block_coord_strs)
        all_piece_coords = ','.join(piece_coord_strs)
        template = TEMPLATE.replace("SUBSTITUTE_BLOCKS", all_block_coords)
        template = template.replace("SUBSTITUTE_PIECES", all_piece_coords)
        return template

class Board:
    def __init__(self, canvas):
        # create board outline:
        D = min(H, W)
        board_coordinates = transform(HEX_F, (W/2, H/2), (0.9*D, 0.9*D))
        self.id = canvas.create_polygon(board_coordinates, fill=Color.FG)

        # create hexagons and piece shadows on board:
        self.hexes = {}
        self.hexid = {}
        self.pieces = {}
        size = 0.12 * D
        for q in range(-3, 4):
            for r in range(-3, 4):
                s = -q-r
                if s in range(-3, 4):
                    new_hex = Hex(q, r, size, canvas)
                    self.hexes[q,r] = new_hex
                    self.hexid[new_hex.id] = new_hex

                    new_piece = Piece(q, r, size, canvas)
                    self.pieces[q,r] = new_piece

    def cycle(self, q, r):
        view_piece = self.pieces[q,r]
        view_piece.cycle()



def transform(coordinates, translate_xy=(0,0), dilate_xy=(1,1)):
    a, b = translate_xy
    A, B = dilate_xy
    return [(a + x*A, b + y*B) for (x, y) in coordinates]

class Hex:
    def __init__(self, q, r, d, canvas):
        # set me up:
        self.q = q
        self.r = r
        self.s = -q-r

        # and draw me on the canvas:
        # place in the center of the board
        coords = transform(HEX_P, (W/2, H/2), (d, d))
        # offset into position based on coordinates
        coords = transform(coords, (r*PW/2*d + q*PW*d, r*3*PH/4*d))
        # create a hexagon there!
        self.id = canvas.create_polygon(coords, tag="hex",
            outline=Color.BG, fill=Color.NONE, activefill=Color.HL)

        # remember my coordinates too!?
        self.coords = (W/2 + r*PW/2*d + q*PW*d, H/2 + r*3*PH/4*d)


class Piece:
    def __init__(self, q, r, d, canvas):
        self.canvas = canvas

        self.col = None

        # create generic stone, invisible, in position
        x, y = (W/2 + r*PW/2*d + q*PW*d, H/2 + r*3*PH/4*d)
        rad1 = 0.35*d # outer circle (stone)
        rad2 = 0.25*d # inner circle (paint)
        self.stone_id = canvas.create_oval(x-rad1, y-rad1, x+rad1, y+rad1,
            tag="stone", outline=Color.BLACK, fill=Color.STONE,
            state=tkinter.HIDDEN)
        self.paint_id = canvas.create_oval(x-rad2, y-rad2, x+rad2, y+rad2,
            tag="paint", outline=Color.NONE, fill=Color.BLACK,
            state=tkinter.HIDDEN)
        self.letter_id = canvas.create_text(x, y,
            tag="letter", text="?", fill=Color.STONE,
            state=tkinter.HIDDEN)

    def paint(self, col=None):
        self.col = col
        if col is None:
            self.canvas.itemconfig(self.letter_id, text="?")
            self.canvas.itemconfig(self.paint_id,  fill=Color.BLACK)
            self.hide()
        else:
            if col == 'R':
                colour = Color.RED
                letter = 'R'
            elif col == 'G':
                colour = Color.GREEN
                letter = 'G'
            elif col == 'B':
                colour = Color.BLUE
                letter = 'B'
            elif col == 'BLOCK':
                colour = Color.BLACK
                letter = ''
            self.canvas.itemconfig(self.letter_id, text=letter)
            self.canvas.itemconfig(self.paint_id, fill=colour)
            self.show()
    def cycle(self):
        if self.col == 'R':
            self.paint('G')
        elif self.col == 'G':
            self.paint('B')
        elif self.col == 'B':
            self.paint('BLOCK')
        elif self.col == 'BLOCK':
            self.paint(None)
        elif self.col == None:
            self.paint('R')

    def hide(self):
        self.canvas.itemconfig(self.letter_id, state=tkinter.HIDDEN)
        self.canvas.itemconfig(self.paint_id, state=tkinter.HIDDEN)
        self.canvas.itemconfig(self.stone_id, state=tkinter.HIDDEN)
    def show(self):
        self.canvas.itemconfig(self.letter_id, state=tkinter.DISABLED)
        self.canvas.itemconfig(self.paint_id, state=tkinter.DISABLED)
        self.canvas.itemconfig(self.stone_id, state=tkinter.DISABLED)



if __name__ == '__main__':
    main()