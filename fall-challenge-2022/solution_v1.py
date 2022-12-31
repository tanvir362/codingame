import sys
import math
import random

def dbg(*arg, **kwarg):
    print(*arg, **kwarg, file=sys.stderr, flush=True)

class Cell:
    def __init__(self, scrap_count, owner, units, recycler, can_build, can_spawn, in_recycler_range, x, y):
        self.scrap_count = scrap_count
        self.is_mine = owner==1
        self.is_opponent = owner==0
        self.robot_count = units
        self.is_recycler = recycler==1
        self.can_build = can_build==1
        self.can_spawn = can_spawn==1
        self.in_recycler_range = in_recycler_range==1

        self.is_grass = scrap_count<1
        self.coord = (x, y)

map = {}
steps = [(1, 0), (0, -1), (-1, 0), (0, 1)]


def is_validate_coord(x, y):
    if x<0 or x>=width or y<0 or y>=height:
        return False

    return True

#x, y should be in control
def should_spawn_at(x, y):
    if (map[(x, y)] in targets): return False

    for dx, dy in steps:
        cell = map.get((x+dx, y+dy))
        if not cell:
            continue
            
        if not (cell.is_mine or cell.in_recycler_range or cell.is_grass):
            return True

    return False

def find_destination(coord):
    x, y = coord
    
    visited = {}
    q = [(x, y)]

    while q:
        cx, cy = q.pop(0)

        # random.shuffle(steps)
        for dx, dy in steps:
            cell = map.get((cx+dx, cy+dy))
            if not cell:
                continue

            if not (visited.get((cx+dx, cy+dy), False) or cell.is_grass):
                if not (cell.is_mine or cell.in_recycler_range) and (cell not in targets):
                    targets.add(cell)
                    return cell.coord

                q.append((cx+dx, cy+dy))
                visited[(cx+dx, cy+dy)] = True

def calculate_robot_sum(cell):
    sm = cell.robot_count * [-1, 1][cell.is_mine]

    x, y = cell.coord
    for dx, dy in steps:
        adj_cell = map.get((x+dx, y+dy))
        if not adj_cell: continue

        sm += adj_cell.robot_count * [-1, 1][adj_cell.is_mine]

    return sm




width, height = [int(i) for i in input().split()]

# game loop
while True:
    targets = set()
    my_robot_cells = []
    my_empty_cells = []
    
    my_matter, opp_matter = [int(i) for i in input().split()]
    for i in range(height):
        for j in range(width):
            # owner: 1 = me, 0 = foe, -1 = neutral
            scrap_amount, owner, units, recycler, can_build, can_spawn, in_range_of_recycler = [int(k) for k in input().split()]
            cell = Cell(scrap_amount, owner, units, recycler, can_build, can_spawn, in_range_of_recycler, j, i)
            map[(j, i)] = cell
            if cell.is_mine:
                if cell.robot_count>0:
                    my_robot_cells.append(cell)
                else:
                    my_empty_cells.append(cell)

    actions = []
    dbg('itering map')
    for cell in my_robot_cells:
        #todo: move numbers of robots need to move else spawn necessary robot
        dest = find_destination(cell.coord)
        if dest:
            actions.append(f"MOVE {cell.robot_count} {cell.coord[0]} {cell.coord[1]} {dest[0]} {dest[1]}")

    for cell in my_empty_cells:
        # dbg(cell.coord, 'my cell', cell.is_mine, 'no robot', cell.robot_count<1, 'can spawn', cell.can_spawn)
        if cell.can_spawn:
            # dbg('should spawn', should_spawn_at(*cell.coord), 'have engough matter', my_matter>=10)
            sm = calculate_robot_sum(cell)
            need = 1
            if sm<0:
                need = -sm
                need += 1


            if should_spawn_at(*cell.coord) and my_matter>=10*need:
                actions.append(f"SPAWN 1 {cell.coord[0]} {cell.coord[1]}")
                # dbg('spawned')
                my_matter -= 10*need

            elif my_matter<10*need and my_matter>=10 and cell.can_build:
                actions.append(f"BUILD {cell.coord[0]} {cell.coord[1]}")
                
    
    print((";".join(actions) or "WAIT")+';'+"MESSAGE Hello world!")
    dbg('action taken')
