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
# terrain_num                  Number of different terrains                       7                                    >0

# ALL Variables: (Preset) x_length, y_length, max_turns, isl_turns, terrain_num
#                (Listening) input, output, 
#                (Core) turn, board, score




class Game:
    def __init__(self):

        self.x_length = 9
        self.y_length = 9
        self.max_turns = 30
        self.isl_turns = (10, 20, 30)
        self.terrain_num = 7

        self.input = []
        self.output = []

        self.turn = 1
        self.board = Board()
        self.score = 0

        self.rnd_mgr()
    
    def set_input(self, msg):
        self.input = msg

    def get_output(self, msg):
        self.output = msg
    
    def rnd_mgr(self):
        if self.turn in (10,20,30):
            self.isl_rnd()
        else:
            self.std_rnd()
        self.rnd_eval()
        self.rnd_end()
    
    def isl_rnd(self):
        otype = rand.randint(1,7)
        oloc = (rand.randint(1,2),rand.randint(0,8))
        self.output = (otype,oloc)

        while not self.input:
            pass
        self.board.draw_isl(self.input)
        self.input = []
        self.output = []
    
    def std_rnd(self):
        self.output = self.board.unoc()

        while not self.input:
            pass
        self.board.insr(self.input[0],self.input[1])
        self.input = []
        self.output = []

    def rnd_eval(self):
        self.board.eval()
        self.score = self.board.pts
    
    def rnd_end(self):
        self.turn += 1
        if self.turn <= 30:
            self.rnd_mgr()



