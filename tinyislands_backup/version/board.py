# type:                 loc:                st:
# 0: Unoccupied         -1: Shore           0: Inactive
# 1: Boasts             0: Ocean            1: Active
# 2: Waves              1: Island 1
# 3: Beach              2: Island 2
# 4: Houses             3: Island 3
# 5: Churches
# 6: Forest
# 7: Mountains

class Tile:
    def __init__(self, type, loc, st):
        self.type = type
        self.loc = loc
        self.st = st

class Board:
    def __init__(self):
        # Initialize Points
        self.pts = 0
        # Initialize Tiles List
        self.tiles = []
        # Initialize Tiles Values
        for y in range(0,9):
            row = []
            for x in range(0,9):
                row.append(Tile(0,0,0))
            self.tiles.append(row)
    
    # Set Floor of 0 for Total Points
    def scrflr(self):
        if self.pts < 0:
            self.pts = 0
    
    # Return List of Tuple XY for Unoccupied Tiles
    def unoc(self):
        # Initialize List
        unoc = []
        # Search For Unoccupied Tiles
        rownum = 0
        for row in self.tiles:
            colnum = 0
            for tile in row:
                if tile.type == 0:
                    unoc.append((colnum, rownum))
                colnum += 1
            rownum += 1
        return unoc
    
    # Insert New Tile
    def insr(self, pos, type):
        # Locate Tile Position
        tile = self.tiles[pos[1]][pos[0]]
        # Update Tile Type
        tile.type = type
        # Activate Terrain Status, Await Evaluation
        tile.st = 1
    
    def draw_isl(self, pgroup, wave):
        for pos in pgroup:
            tile = self.tiles[pos[1]][pos[0]]
            tile.loc = wave
        for pos in pgroup:
            near = []
            for i in (1, -1):
                nx = pos[0] + i
                if 0 <= nx <= 8:
                    near.append(nx, pos[1])
                ny = pos[1] + i
                if 0 <= ny <= 8:
                    near.append(pos[0], ny)
            for n in near:
                targ = self.tiles[n[1]][n[0]]
                if targ.loc == 0:
                    targ.loc = -1

    # Evaluate board
    def eval(self):
        for row in self.tiles:
            for tile in row:
                if tile.st == 1:
                    self.pen(tile)
        self.bonus()
    
    # Evaluate Penalty
    def pen(self, t):
        if t.type in range(1,4):
            if t.loc in range(1,4):
                t.st = 0
                self.pts -= 5
        elif t.type in range(4,8):
            if t.loc not in range(1,4):
                t.st = 0
                self.pts -= 5
        self.scrflr()
    
    def bonus(self):
        shps = []
        isls = []
        wvs = []
        hses = []
        chrhs = []
        grps = []
        frst = []
        mtns = []

        rownum = 0
        for row in self.tiles:
            colnum = 0
            for tile in row:
                if tile.type == 1 and tile.st == 1:
                    shps.append((colnum,rownum))
                if tile.loc in [1,2,3]:
                    isls.append((colnum,rownum))
                if tile.type == 2 and tile.st == 1 and tile.loc == 0:
                    wvs.append((colnum,rownum))
                if tile.type == 3 and tile.st == 1 and tile.loc == -1:
                    self.pts += 1
                if tile.type == 4 and tile.st == 1:
                    hses.append((colnum,rownum))
                if tile.type == 5 and tile.st == 1:
                    chrhs.append((colnum,rownum))
                if tile.type == 6 and tile.st == 1:
                    frst.append((colnum,rownum))
                if tile.type == 7 and tile.st == 1:
                    mtns.append(tile)
                colnum += 1
            rownum += 1
        
        for s in shps:
            targs = shps + isls
            targs.remove(s)
            if targs:
                dlist = []
                for tar in targs:
                    dist = abs(tar[0] - s[0]) + abs(tar[1] - s[1])
                    dlist.append(dist)
                self.pts += min(dlist)
        
        for w in wvs:
            targs = wvs
            targs.remove(w)
            bonus = 2
            for tar in targs:
                if w[0] == tar[0] or w[1] == tar[1]:
                    bonus = 0
                    break
            self.pts += bonus
        
        for h in hses:
            unique = []
            for ytry in range(-1,2):
                for xtry in range(-1,2):
                    if xtry != 0 and ytry != 0:
                        xnear = h[0] + xtry
                        ynear = h[1] + ytry
                        if xnear <= 8 and ynear <= 8:
                            targ = self.tiles[ynear][xnear]
                            if targ.type not in (0,4) and targ.type not in unique:
                                unique.append(targ.type)
            self.pts += len(unique)

        for c in chrhs:
            crusade = False
            inf = chrhs
            inf.remove(c)
            # Check for Crusade
            for i in inf:
                if c.loc == i.loc:
                    crusade = True
            if not crusade:
                nrow = 0
                for row in self.tiles:
                    ncol = 0
                    for targ in row:
                        if targ.type == 4 and c.loc == targ.loc:
                            self.pts += 1
                            for ytry in range(-1,2):
                                for xtry in range(-1,2):
                                    if xtry != 0 and ytry != 0:
                                        xnear = c[0] + xtry
                                        ynear = c[1] + ytry
                                        if targ[0] == xnear and targ[1] == ynear:
                                            self.pts += 1
                        ncol += 1
                    nrow += 1
        
        for f in frst:
            for i in (-1, 1):
                for grp in grps:
                    for targ in grp:
                        if (f[0] + i == targ[0] or f[0]== targ[0]) and (f[1] == targ[1] or f[1] + i == targ[1]):
                            grp.append(f)
                            registered = True
                            break
                if registered == True:
                    break
            if not registered:
                newgrp = []
                newgrp.append(f)
                grps.append(newgrp)
        for grp in grps:
            self.pts += len(grp) * 2 - 2

        for m in mtns:
            for ytry in range(-1,2):
                for xtry in range(-1,2):
                    if xtry != 0 and ytry != 0:
                        xnear = m[0] + xtry
                        ynear = m[1] + ytry
                        if 0 <= xnear <= 8 and 0 <= ynear <= 8:
                            targ = self.tiles[ynear][xnear]
                            if targ[0] == m[0] + xtry and targ[1] == m[1] + ytry:
                                if targ.type == 5:
                                    self.pts += 2
