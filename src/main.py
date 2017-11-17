import sys
import math
import numpy as np



# Constants
DEBUG = True

INF = 9999999

REAPER = 0
DESTROYER = 1
TANKER = 3
WRECK = 4

PLAYER_NUM = 3
AREA_RADIUS = 6000
REAPER_RADIUS = 400

# Class
class Reaper:
    def __init__(self, unit_id, mass,
                       radius, x, y, vx, vy, extra, extra2):
        self.unit_id = unit_id
        self.mass = mass
        self.radius = radius
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.extra = extra
        self.extra2 = extra2

class Destroyer:
    def __init__(self, unit_id, mass,
                       radius, x, y, vx, vy, extra, extra2):
        self.unit_id = unit_id
        self.mass = mass
        self.radius = radius
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.extra = extra
        self.extra2 = extra2

class Tanker:
    def __init__(self, unit_id,
                       mass, radius, x, y, extra, extra2):
        self.unit_id = unit_id
        self.mass = mass
        self.radius = radius
        self.x = x
        self.y = y
        self.extra = extra
        self.extra2 = extra2

class Wreck:
    def __init__(self, unit_id,
                       mass, radius, x, y, extra, extra2):
        self.unit_id = unit_id
        self.mass = mass
        self.radius = radius
        self.x = x
        self.y = y
        self.extra = extra
        self.extra2 = extra2

# Global
score = []
my_reaper = []
op_reaper = []
my_destroyer = []
op_destroyer = []
tanker = []
wreck = []

# Function
def game_turn_input():
    global score, my_reaper, op_reaper, my_destroyer, op_destroyer, wreck

    score = [None for x in range(PLAYER_NUM)]
    for i in range(PLAYER_NUM):
        score[i] = int(input())
        if DEBUG:
            sys.stderr.write(str(score[i]) + "\n")

    for i in range(PLAYER_NUM):
        x = input()
        if DEBUG:
            sys.stderr.write(x + "\n")
    
    my_reaper = []
    op_reaper = []
    my_destroyer = []
    op_destroyer = []
    tanker = []
    wreck = []

    unit_count = int(input())
    if DEBUG:
        sys.stderr.write(str(unit_count) + "\n")
        
    for i in range(unit_count):
        unit_id, unit_type, player_id, mass, radius, x, y, vx, vy, extra, extra2 = input().split()
        if DEBUG:
            sys.stderr.write(unit_id + " " + unit_type + " " + player_id + " " 
                           + mass + " " + radius + " " + x + " " + y + " "
                           + vx + " " + vy + " " + extra + " " + extra2 + "\n")

        unit_id = int(unit_id)
        unit_type = int(unit_type)
        player_id = int(player_id)
        mass = float(mass)
        radius = int(radius)
        x = int(x)
        y = int(y)
        vx = int(vx)
        vy = int(vy)
        extra = int(extra)
        extra2 = int(extra2)

        if unit_type == REAPER:
            if (player_id == -1):
                op_reaper.append(Reaper(unit_id, mass, radius, 
                    x, y, vx, vy, extra, extra2))
            else:
                my_reaper.append(Reaper(unit_id, mass, radius, 
                    x, y, vx, vy, extra, extra2))
        elif unit_type == DESTROYER:
            if (player_id == -1):
                op_destroyer.append(Destroyer(unit_id, mass, radius, 
                    x, y, vx, vy, extra, extra2))
            else:
                my_destroyer.append(Destroyer(unit_id, mass, radius, 
                    x, y, vx, vy, extra, extra2))

        elif unit_type == TANKER:
            tanker.append(Tanker(unit_id, mass, radius, x, y, extra, extra2))

        elif unit_type == WRECK:
            wreck.append(Wreck(unit_id, mass, radius, x, y, extra, extra2))

def dist2D(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def think_reaper():
    dist_min = INF

    nx = -1
    ny = -1

    for w in wreck:
        dist = dist2D(my_reaper[0].x, my_reaper[0].y, w.x, w.y)
        if dist < dist_min:
            dist_min = dist
            nx = w.x
            ny = w.y

    # wreckがなかったらDestroyerに近寄っておく。
    if nx == -1:
        nx = my_destroyer[0].x
        ny = my_destroyer[0].y

    print(nx, ny, 300)

def think_destroyer():
    dist_min = INF

    nx = -1
    ny = -1

    for t in tanker:
        dist = dist2D(my_destroyer[0].x, my_destroyer[0].y, t.x, t.y)
        if dist < dist_min:
            dist_min = dist
            nx = t.x
            ny = t.y

    print(nx, ny, 300)

if __name__ == "__main__":
    # main loop
    while True:
        game_turn_input()
        think_reaper()
        think_destroyer()

        print("WAIT")