import numpy as np



# Constants
DEBUG = True

REAPER = 0
WRECK = 4
PLAYER_NUM = 3
AREA_RADIUS = 6000
REAPER_RADIUS = 400

# Class
class Reaper:
    def __init__(self, unit_id, player_id, mass,
                       radius, x, y, vx, vy, extra, extra2):
        self.unit_id = unit_id
        self.player_id = player_id
        self.mass = mass
        self.radius = radius
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
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
reaper = []
wreck = []

# Function
def game_turn_input():
    global score, reaper, wreck

    score = [None for x in range(PLAYER_NUM)]
    for i in range(PLAYER_NUM):
        score[i] = int(input())

    for i in range(PLAYER_NUM):
        input()
    
    reaper = []
    wreck = []
    unit_count = int(input())
    for i in range(unit_count):
        unit_id, unit_type, player_id, mass, radius, x, y, vx, vy, extra, extra2 = input().split()
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
            reaper.append(Reaper(unit_id, player_id, mass, radius, 
                x, y, vx, vy, extra, extra2))
        elif unit_type == WRECK:
            wreck.append(Wreck(unit_id, mass, radius, x, y, extra, extra2))
    

if __name__ == "__main__":
    # main loop
    while True:
        game_turn_input()
        print("WAIT")
        print("WAIT")
        print("WAIT")