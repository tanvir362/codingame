import sys
import math

# Save humans, destroy zombies!

initial_x, initial_y = 0, 0
is_initial = True

reached1 = False
reached2 = False

# game loop
while True:
    x, y = [int(i) for i in input().split()]
    if is_initial:
        initial_x, initial_y = x, y
        is_initial = False
        point1 = (4000, 4500) if x<=8000 else (12000, 4500)
        point2 = (4000, 4500) if x>8000 else (12000, 4500)

        p3x = 16000 if x<=8000 else 0
        p3y = 9000 if y<=4500 else 0
        point3 = (p3x, p3y)
        

    
    human_count = int(input())
    for i in range(human_count):
        human_id, human_x, human_y = [int(j) for j in input().split()]
    zombie_count = int(input())
    for i in range(zombie_count):
        zombie_id, zombie_x, zombie_y, zombie_xnext, zombie_ynext = [int(j) for j in input().split()]

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    # Your destination coordinates
    if initial_x <= 8000:
        if x >= point1[0]:
            reached1 = True
        if x >= point2[0]:
            reached2 = True
    else:
        if x <= point1[0]:
            reached1 = True
        if x <= point2[0]:
            reached2 = True
    
    if not reached1:
        print(point1[0], point1[1], sep=" ")
    elif reached1 and not reached2:
        print(point2[0], point2[1], sep=" ")
    else:
        print(point3[0], point3[1], sep=" ")

