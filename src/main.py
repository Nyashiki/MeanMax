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
TAR_POOL = 5
OIL_POOL = 6

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

class TarPool:
    def __init__(self, unit_id,
                       mass, radius, x, y, extra, extra2):
        self.unit_id = unit_id
        self.mass = mass
        self.radius = radius
        self.x = x
        self.y = y
        self.extra = extra
        self.extra2 = extra2

class OilPool:
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
tar_pool = []
oil_pool = []

# Function
def game_turn_input():
    global score, rage
    global my_reaper, op_reaper, my_destroyer, op_destroyer, my_doof, op_doof
    global tanker, wreck, tar_pool, oil_pool

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
    tar_pool = []
    oil_pool = []

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

        elif unit_type == TAR_POOL:
            tar_pool.append(TarPool(unit_id, mass, radius, x, y, extra, extra2))

        elif unit_type == OIL_POOL:
            oil_pool.append(OilPool(unit_id, mass, radius, x, y, extra, extra2))

def dist2D(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def sigmoid(x):
    return 1 / (1 + math.exp(-x))
    
def speed(vx, vy):
    return math.sqrt(vx**2 + vy**2)

def think_reaper():
    global rage
    
    start_time = time.time()

    dist_min = INF

    nx = -1
    ny = -1
    throttle = 100

    for w in wreck:
        dist = dist2D(my_reaper.x, my_reaper.y, w.x, w.y)
        if dist < dist_min:
            dist_min = dist
            nx = w.x
            ny = w.y
            xx = my_reaper.x + my_reaper.vx / 0.2
            yy = my_reaper.y + my_reaper.vy / 0.2
            if dist2D(xx, yy, w.x, w.y) < w.radius:
                throttle = 1
            else:
                dist_2 = dist2D(xx, yy, w.x, w.y)
                throttle = int(300 * sigmoid(dist_2))

    # wreckがなかったら、Tankerに一番近いDestroyerに近寄っておく。
    if dist_min == INF:
        nx = my_destroyer.x
        ny = my_destroyer.y
        xx = my_reaper.x + my_reaper.vx / 0.2
        yy = my_reaper.y + my_reaper.vy / 0.2

        for d in op_destroyer:
            for t in tanker:
                dist = dist2D(d.x, d.y, t.x, t.y)
                if dist < dist_min:
                    dist = dist_min
                    nx = d.x
                    ny = d.y
                if dist2D(xx, yy, d.x, d.y) < d.radius:
                    throttle = 0
                else:
                    dist_2 = dist2D(xx, yy, d.x, d.y)
                    throttle = int(300 * sigmoid(dist_2))

    elapsed = time.time() - start_time

    print(nx, ny, throttle, elapsed)

def think_destroyer():
    global rage

    start_time = time.time()

    # 相手のWreckを取られそうだったら、Grenadeを投げる。
    if rage[0] >= 60:
        for w in wreck:
            dist = dist2D(my_destroyer.x, my_destroyer.y, w.x, w.y)
            if dist < 2000: 
                my_dist = dist2D(my_reaper.x, my_reaper.y, w.x, w.y)            
                # 相手がこのWreckから水を得そうならば、Grenadeを投擲。
                for r in op_reaper:
                    dx = w.x - r.x
                    dy = w.y - r.y
                    dot = dx * r.vx + dy * r.vy
                    if dot > 0:
                        op_dist = dist2D(w.x, w.y, r.x, r.y)
                        if op_dist < my_dist and op_dist < 3000:
                            print("SKILL", w.x, w.y)
                            rage[0] -= 60
                            return
    dist_min = INF

    nx = -1
    ny = -1

    # 前ターンに狙ったものがあれば、それを狙う。
    for t in tanker:
        if t.unit_id == my_destroyer.target:
            nx = t.x
            ny = t.x
            break
    # 一番近いものを壊せばいいわけではない。相手に取られそうな場合には破壊しない。
    else:
        for t in tanker:
            dist = dist2D(my_destroyer.x, my_destroyer.y, t.x, t.y)
            my_dist = dist2D(my_reaper.x, my_reaper.y, t.x, t.y)
            op_dist_min = INF
            for r in op_reaper:
                dist_op = dist2D(r.x, r.y, t.x, t.y)
                if dist_op < op_dist_min:
                    op_dist_min = dist_op

            if dist < dist_min and my_dist < op_dist_min:
                dist_min = dist
                nx = t.x
                ny = t.y
                my_destroyer.target = t.unit_id

    elapsed = time.time() - start_time
    print(nx, ny, 300, elapsed)

def think_doof():
    global rage

    start_time = time.time()

    # とりあえず最も近い相手のReaperにフルスロットルで近づいてみる。
    # 行きたいところに先回りして、邪魔をする。

    # Wreckが取られそうならOil Poolを作成。
    # ToDo: ほかのUnitがrage を使用していたら、rageが足りなくなるかもしれないことに注意。
    if rage[0] >= 30:
        # 今自分のDoofがWreckにいるか
        for w in wreck:
            dist = dist2D(my_doof.x, my_doof.y, w.x, w.y)
            if dist < 2000:
                my_dist = dist2D(my_reaper.x, my_reaper.y, w.x, w.y)            
                # 相手がこのWreckから水を得そうならば、Oil Poolを作成
                # 水を得そうとは、
                #  - ある程度距離が近い (ToDo)
                #  - Wreckに向かっている
                for r in op_reaper:
                    dx = w.x - r.x
                    dy = w.y - r.y
                    dot = dx * r.vx + dy * r.vy
                    if dot > 0:
                        op_dist = dist2D(w.x, w.y, r.x, r.y)
                        if op_dist < my_dist and op_dist < 3000:
                            print("SKILL", w.x, w.y)
                            rage[0] -= 30
                            return

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
        