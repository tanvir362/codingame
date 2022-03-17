import sys
import math

# Save humans, destroy zombies!

def if_mv_reduce_dist(hums, curx, cury, nxtx, nxty):
    for h in hums:
        if math.hypot(h[0] - nxtx, h[1] - nxty) <= math.hypot(h[0] - curx, h[1] - cury):
            return True
    return False

is_first = True
# game loop
while True:
    mv_x, mv_y = 8000, 4500
    min_dist = 25000
    humans = []
    zombies = []

    x, y = [int(i) for i in input().split()]
    human_count = int(input())
    for i in range(human_count):
        human_id, human_x, human_y = [int(j) for j in input().split()]
        humans.append((human_x, human_y))
    
    zombie_count = int(input())
    for i in range(zombie_count):
        zombie_id, zombie_x, zombie_y, zombie_xnext, zombie_ynext = [int(j) for j in input().split()]
        dist = math.hypot(zombie_x - x, zombie_y - y)
        if dist < min_dist:
            if is_first:
                min_dist = dist
                mv_x, mv_y = zombie_x, zombie_y
                is_first = False
            
            elif if_mv_reduce_dist(humans, x, y, zombie_x, zombie_y):
                min_dist = dist
                mv_x, mv_y = zombie_x, zombie_y

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    # Your destination coordinates
    print(mv_x, mv_y, sep=" ")

