import sys
import math
import random

class Entity:
    def __init__(self, id, x, y):
        self.id = id
        self.position = (x, y)
        self.is_visible = True

    def update_property(self, x, y):
        self.position = (x, y)
        self.is_visible = True

    def calc_dist(self, point):
        return math.hypot(self.position[0]-point[0], self.position[1]-point[1])


class Buster(Entity):
    def __init__(self, id, x, y, entity_type, state, value):
        super().__init__(id, x, y)
        self.team_id = entity_type
        self.is_mine = entity_type == game.my_team_id
        self.is_carrying = state == 1
        self.carrying_ghost_id = value # -1 if not carrying

        self.going_toward = game.my_base

    def update_property(self, x, y, state, value):
        super().update_property(x, y)
        self.is_carrying = state == 1
        self.carrying_ghost_id = value



    def move(self, point):
        print(f"MOVE {point[0]} {point[1]}")

    def bust(self, ghost_id):
        print(f"BUST {ghost_id}")

    def release(self):
        print("RELEASE")

    def find_nearest_ghost(self):
        try:
            ghosts = sorted([ght for ght in game.ghosts.values() if not ght.is_in_my_base], key=lambda ghost: ghost.calc_dist(self.position))

            return ghosts[0]

        except Exception as e:
            print(str(e), file=sys.stderr, flush=True)
            return None

    
    def act(self):
        if self.is_carrying:
            #move to base or release
            carrying_ghost = game.ghosts.get(self.carrying_ghost_id)

            if self.calc_dist(game.my_base) < 1600:
                game.ghosts[self.carrying_ghost_id].is_in_my_base = True
                self.release()
                print(f'{self.id} released {self.carrying_ghost_id} ghost', file=sys.stderr, flush=True)

            else:
                self.move(game.my_base)
                print(f'{self.id} moved toward base', file=sys.stderr, flush=True)

        else:
            n_ghost = self.find_nearest_ghost()

            if n_ghost:
                #bust or move toward ghost

                print(f"{n_ghost.id} is in my base: {n_ghost.is_in_my_base}", file=sys.stderr, flush=True)

                if self.calc_dist(n_ghost.position) <= 1760 and self.calc_dist(n_ghost.position) >= 900:
                    self.bust(n_ghost.id)
                    print(f'{self.id} busted {n_ghost.id} ghost', file=sys.stderr, flush=True)

                else:
                    self.move(n_ghost.position)
                    print(f'{self.id} moved toward {n_ghost.id} ghost', file=sys.stderr, flush=True)

            else:
                options = [(4000, 2250), (12000, 2250), (4000, 6750), (12000, 6750)]
                pick = self.going_toward
                if self.calc_dist(self.going_toward) <= 50:
                    pick = random.choice(options)

                self.going_toward = pick
                self.move(pick)
                print(f'{self.id} moved random', file=sys.stderr, flush=True)
                
            
    def __str__(self):
        return f"id: {self.id} position: {self.position} {'MINE' if self.is_mine else 'RIVAL'} {f'carrying: {self.carrying_ghost_id}' if self.is_carrying else ''}"


class Ghost(Entity):
    def __init__(self, id, x, y, state, value):
        super().__init__(id, x, y)
        self.state = state
        self.attempting_by = value
        self.is_in_my_base = False

    def update_property(self, x, y, state, value):
        super().update_property(x, y)
        self.state = state
        self.attempting_by = value

    def __str__(self):
        return f"id: {self.id} position: {self.position} attempting by: {self.attempting_by}"


class Game:
    def __init__(self, bpp, ghost_count, my_team_id):
        self.busters_per_player = bpp
        self.ghost_count = ghost_count
        self.my_team_id = my_team_id
        self.my_base = (0, 0) if my_team_id == 0 else (16000, 9000)

        self.busters = {}
        self.ghosts = {}

    def end_round(self):
        for ghost in self.ghosts.values():
            ghost.is_visible = False

        for buster in self.busters.values():
            buster.is_visible = False



# Send your busters out into the fog to trap ghosts and bring them home!

busters_per_player = int(input())  # the amount of busters you control
ghost_count = int(input())  # the amount of ghosts on the map
my_team_id = int(input())  # if this is 0, your base is on the top left of the map, if it is one, on the bottom right

game = Game(busters_per_player, ghost_count, my_team_id)
# game loop
while True:
    entities = int(input())  # the number of busters and ghosts visible to you
    for i in range(entities):
        # entity_id: buster id or ghost id
        # y: position of this buster / ghost
        # entity_type: the team id if it is a buster, -1 if it is a ghost.
        # state: For busters: 0=idle, 1=carrying a ghost.
        # value: For busters: Ghost id being carried. For ghosts: number of busters attempting to trap this ghost.
        entity_id, x, y, entity_type, state, value = [int(j) for j in input().split()]
        if entity_type == -1:
            ghost = game.ghosts.get(entity_id, Ghost(entity_id, x, y, state, value))
            game.ghosts[entity_id] = ghost
            ghost.update_property(x, y, state, value)
            # print(ghost, file=sys.stderr, flush=True)
        else:
            buster = game.busters.get(entity_id, Buster(entity_id, x, y, entity_type, state, value))
            game.busters[entity_id] = buster
            buster.update_property(x, y, state, value)
            # print(buster, file=sys.stderr, flush=True)


    # for i in range(busters_per_player):

    #     # Write an action using print
    #     # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    #     # MOVE x y | BUST id | RELEASE
    #     print("MOVE 8000 4500")

    for buster_id in game.busters:
        buster = game.busters[buster_id]
        if buster.is_mine:
            buster.act()

    game.end_round()

