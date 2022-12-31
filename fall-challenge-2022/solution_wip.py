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

        self.is_neutral = scrap_count>0 and owner==-1
        self.is_grass = scrap_count<1
        self.coord = (x, y)

    def get_max_neighbour_enemy_robots(self):
        x, y = self.coord

        mx = 0
        for dx, dy in steps:
            adj_cell = map.get((x+dx, y+dy))
            if not adj_cell: continue

            if not(adj_cell.is_mine or adj_cell.is_grass) and adj_cell.robot_count>mx:
                mx = adj_cell.robot_count

        return mx

    def is_scrap_lower_than_neighbour(self):
        x, y = self.coord
        for dx, dy in steps:
            adj_cell = map.get((x+dx, y+dy))
            if not adj_cell: continue

            if self.scrap_count >= adj_cell.scrap_count:
                pass

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
            
        if not (cell.is_mine or cell.is_grass):
            return True

    return False

def find_destination(coord):
    x, y = coord
    
    visited = {}
    q = [(x, y)]

    while q:
        cx, cy = q.pop(0)

        steps.sort(key=lambda crd: math.hypot((cx+crd[0])-enemy_base.coord[0], (cy+crd[1])-enemy_base.coord[1])*10)
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

initial_turn = True
my_base = None
enemy_base = None


# game loop
while True:
    targets = set()
    my_robot_cells = []
    my_empty_cells = []
    enemy_robot_cells = []
    enemy_empty_cells = []

    
    
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

            else:
                if cell.robot_count>0:
                    enemy_robot_cells.append(cell)
                else:
                    enemy_empty_cells.append(cell)

            if initial_turn:
                if cell.robot_count == 0:
                    if cell.is_mine:
                        my_base = cell
                    elif cell.is_opponent:
                        enemy_base = cell


    actions = []
    if initial_turn:
        actions.append(f"BUILD {my_base.coord[0]} {my_base.coord[1]}")
        my_matter -= 10
    initial_turn = False

    # dbg('my base', my_base.coord, 'enemy base', enemy_base.coord)
    dbg('itering map')
    my_empty_cells.sort(key=lambda c: c.get_max_neighbour_enemy_robots(), reverse=True)

    for cell in my_robot_cells:
        #todo: move numbers of robots need to move else spawn necessary robot
        #todo: update destinatin cell robot count after a move
        spawn_count = 0
        move_count = 0
        while move_count<cell.robot_count and spawn_count==0:
            dest = find_destination(cell.coord)
            if dest:
                dest_cell = map[dest]
                max_ememy_near_dest = dest_cell.get_max_neighbour_enemy_robots()
                necessary = max_ememy_near_dest + dest_cell.robot_count + 1
                need = max(necessary-cell.robot_count, 0)

                if need>0:
                    if my_matter >= 10*need:
                        actions.append(f"SPAWN {need} {cell.coord[0]} {cell.coord[1]}")
                        spawn_count += need
                    else:
                        cell_to_build = my_empty_cells[0]
                        if cell_to_build.can_build:
                            actions.append(f"BUILD {cell_to_build.coord[0]} {cell_to_build.coord[1]}")

                else:
                    to_move = necessary
                    actions.append(f"MOVE {to_move} {cell.coord[0]} {cell.coord[1]} {dest[0]} {dest[1]}")
                    move_count += to_move

        cell.robot_count -= move_count
        cell.robot_count += spawn_count
    
    for cell in my_empty_cells:
        # dbg(cell.coord, 'my cell', cell.is_mine, 'no robot', cell.robot_count<1, 'can spawn', cell.can_spawn)
        # todo build recycler at my lowest scraper empty cell

        nb_mx_robot = cell.get_max_neighbour_enemy_robots()

        if nb_mx_robot>0:
            if nb_mx_robot>2:
                actions.append(f"BUILD {cell.coord[0]} {cell.coord[1]}")

            else:
                actions.append(f"SPAWN {2} {cell.coord[0]} {cell.coord[1]}")



        # if my_matter>=10:
        #     min_scrap_cell = min(my_empty_cells, key=lambda c: c.scrap_count)
        #     actions.append(f"BUILD {min_scrap_cell.coord[0]} {min_scrap_cell.coord[1]}")
        #     my_matter -= 10

        # if cell.can_spawn:
        #     # dbg('should spawn', should_spawn_at(*cell.coord), 'have engough matter', my_matter>=10)
        #     need = cell.get_max_neighbour_enemy_robots()+1


        #     if my_matter>=10*need and (not cell.in_recycler_range):
        #         actions.append(f"SPAWN {need} {cell.coord[0]} {cell.coord[1]}")
        #         # dbg('spawned')
        #         my_matter -= 10*need

        #     elif my_matter<10*need and my_matter>=10 and cell.can_build:
        #         actions.append(f"BUILD {cell.coord[0]} {cell.coord[1]}")
        #         my_matter -= 10

        # if cell.get_max_neighbour_enemy_robots()>0:
        #     if cell.can_build and my_matter>=10 and (not cell.in_recycler_range):
        #         actions.append(f"BUILD {cell.coord[0]} {cell.coord[1]}")
        #         my_matter -= 10

                
    
    print((";".join(actions) or "WAIT")+';'+"MESSAGE Hello world!")
    dbg('action taken')
