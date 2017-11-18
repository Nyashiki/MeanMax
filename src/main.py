import sys
import time
import math
import numpy as np


# Constants
DEBUG = True

INF = 9999999

REAPER = 0
DESTROYER = 1
DOOF = 2
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
        self.target = -1

class Doof:
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
        self.target = -1

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
rage = []
my_reaper = None
op_reaper = []
my_destroyer = None
op_destroyer = []
my_doof = None
op_doof = []
tanker = []
wreck = []

# Function
def game_turn_input():
    global score, rage, my_reaper, op_reaper, my_destroyer, op_destroyer, my_doof, op_doof, tanker, wreck

    score = [None for x in range(PLAYER_NUM)]
    for i in range(PLAYER_NUM):
        score[i] = int(input())
        if DEBUG:
            sys.stderr.write(str(score[i]) + "\n")

    rage = [None for x in range(PLAYER_NUM)]
    for i in range(PLAYER_NUM):
        rage[i] = int(input())
        if DEBUG:
            sys.stderr.write(str(rage[i]) + "\n")
    
    my_reaper = None
    op_reaper = []
    my_destroyer = None
    op_destroyer = []
    my_doof = None
    op_doof = []
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
            if player_id == 0:
                my_reaper = Reaper(unit_id, mass, radius, x, y, vx, vy, extra, extra2)
            else:
                op_reaper.append(Reaper(unit_id, mass, radius, 
                    x, y, vx, vy, extra, extra2))

        elif unit_type == DESTROYER:
            if player_id == 0:
                my_destroyer = Destroyer(unit_id, mass, radius, x, y, vx, vy, extra, extra2)
            else:
                op_destroyer.append(Destroyer(unit_id, mass, radius, 
                    x, y, vx, vy, extra, extra2))

        elif unit_type == DOOF:
            if player_id == 0:
                my_doof = Doof(unit_id, mass, radius, x, y, vx, vy, extra, extra2)
            else:
                op_doof.append(Doof(unit_id, mass, radius, 
                    x, y, vx, vy, extra, extra2))

        elif unit_type == TANKER:
            tanker.append(Tanker(unit_id, mass, radius, x, y, extra, extra2))

        elif unit_type == WRECK:
            wreck.append(Wreck(unit_id, mass, radius, x, y, extra, extra2))

def dist2D(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def sigmoid(x):
    return 1 / (1 + math.exp(-x))
    
def speed(vx, vy):
    return math.sqrt(vx**2 + vy**2)

def think_reaper():
    start_time = time.time()

    dist_min = INF

    nx = -1
    ny = -1

    for w in wreck:
        dist = dist2D(my_reaper.x, my_reaper.y, w.x, w.y)
        if dist < dist_min:
            dist_min = dist
            nx = w.x
            ny = w.y

    if dist_min == INF:
        # wreckがなかったら、Tankerに一番近いDestroyerに近寄っておく。
        nx = my_destroyer.x
        ny = my_destroyer.y
        for t in tanker:
            dist = dist2D(my_destroyer.x, my_destroyer.y, t.x, t.y)
            if dist < dist_min:
                nx = t.x
                ny = t.y
        
        for d in op_destroyer:
            for t in tanker:
                dist = dist2D(d.x, d.y, t.x, t.y)
                if dist < dist_min:
                    dist = dist_min
                    nx = t.x
                    ny = t.y
        
    elapsed = time.time() - start_time
    # スロットルをsigmoid関数によりなめらかに調整。
    # 現在の速度も考慮。
    print(nx, ny, (int)(300 * sigmoid(dist_min - speed(my_destroyer.vx, my_destroyer.vy))), elapsed)

def think_destroyer():
    start_time = time.time()

    # 密集していたらGrenadeを投げる。
    if rage[0] >= 60:
        xs = [e.x for e in op_reaper + op_destroyer + op_doof]
        ys = [e.y for e in op_reaper + op_destroyer + op_doof]
        tx = int(np.mean(xs))
        ty = int(np.mean(ys))
        if dist2D(my_destroyer.x, my_destroyer.y, tx, ty) < 2000:
            print("SKILL", tx, ty)
            return

    dist_min = INF

    nx = -1
    ny = -1

    for t in tanker:
        if t.unit_id == my_destroyer.target:
            nx = t.x
            ny = t.x
            break
    else:
        for t in tanker:
            dist = dist2D(my_destroyer.x, my_destroyer.y, t.x, t.y)
            if dist < dist_min:
                dist_min = dist
                nx = t.x
                ny = t.y
                my_destroyer.target = t.unit_id

    elapsed = time.time() - start_time
    print(nx, ny, 300, elapsed)

def think_doof():
    start_time = time.time()

    # とりあえず最も近い相手のReaperにフルスロットルで近づいてみる。
    # 行きたいところに先回りして、邪魔をする。
    dist_min = INF

    nx = -1
    ny = -1

    for r in op_reaper:
        dist = dist2D(my_doof.x, my_doof.y, r.x, r.y)
        if dist < dist_min:
            dist_min = dist
            nx = r.x
            ny = r.y

    elapsed = time.time() - start_time
    print(nx, ny, 300, elapsed)

if __name__ == "__main__":
    # main loop
    while True:
        game_turn_input()
        think_reaper()
        think_destroyer()
        think_doof()
        