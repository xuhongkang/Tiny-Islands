import random as rand
from board import Board

# Var/Round      Initializing                           Standard                                  Island
# Output             N/A                ((olocx, olocy) * Choices, otype * Choices)             (unoc_tiles)
# Input        Preset Variables                         (Choice)                                  (pgroup)


# Preset Variables:                    Description                          Default Values                        Restrictions
# x_length                       Length of Board (X-axis)                         9                                 >2, <20
# y_length                       Length of Board (Y-axis)                         9                                 >2, <20
# 
# max_turns:                     Maximum number of Turns              x_length * y_length/2.7(RndUp)      >1, <x_length * y_length
# isl_turns:                   List of Island Drawing Turns        x_length * y_length/max_turns(RndUp)   length >=0, x_length * y_length
#                                                                                                         & every element in turn range
# terrain_num(f)               Number of different terrains                       7                                    >0
# choices/cnum                 Number of choices to choose from                   2                                    >1

# ALL Variables: (Preset) x_length, y_length, max_turns, isl_turns, terrain_num(f), cnum
#                (Listening) input, output, 
#                (Core) turn, board, score

class Game:
    def __init__(self, x_length=9, y_length=9, choices=2, max_turns=30, isl_turns=(10, 20, 30)):

        self.xlength = x_length
        self.ylength = y_length
        self.cnum = choices
        self.max_turns = max_turns
        self.isl_turns = isl_turns

        self.input = []
        self.output = []

        self.turn = 0
        self.board = Board(x_length, y_length)
        self.score = 0

    def start(self):
        self.turn = 1
        self.rnd_mgr()
    
    def wait(self):
        while not self.input:
            pass
        self.output = []
    
    def set_input(self, msg):
        self.input = msg

    def get_output(self):
        return self.output
    
    def rnd_mgr(self):
        if self.turn in self.isl_turns:
            self.isl_rnd()
        else:
            self.std_rnd()
        self.rnd_eval()
        self.rnd_end()
    
    def isl_rnd(self):

        self.output = self.board.unoc()

        self.wait()

        self.board.draw_isl(self.input)
        self.input = []
    
    def std_rnd(self):
        otpt = []
        for i in range(1,self.cnum):
            otpt.append((rand.randint(1,7), rand.choice((
                (0, rand.randint(0,self.board.xmax)),
                (1,rand.randint(0,self.board.ymax))
            ))))
        self.output = otpt

        self.wait()

        self.board.insr(self.input[0],self.input[1])
        self.input = []

    def rnd_eval(self):
        self.board.eval()
        self.score = self.board.pts
    
    def rnd_end(self):
        self.turn += 1
        if self.turn <= 30:
            self.rnd_mgr()

Game()