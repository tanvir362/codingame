import random
import sys
import math


def sign(p1, p2, p3):
    return (p1[0]-p3[0]) * (p2[1]-p3[1]) - (p2[0]-p3[0]) * (p1[1]-p3[1])

def point_in_triangle(v1, v2, v3, pt):
    d1 = sign(pt, v1, v2)
    d2 = sign(pt, v2, v3)
    d3 = sign(pt, v3, v1)

    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

    return not(has_neg and has_pos)


class Entity:
    def __init__(self, entity_id, x, y, vx, vy):
        self.id = entity_id
        self.position = (x, y)
        self.speed = (vx, vy)
    
    @property
    def speed_value(self):
        return math.hypot(self.speed[0], self.speed[1])

    def update_properties(self, x, y, vx, vy):
        self.position = (x, y)
        self.speed = (vx, vy)

    def get_distance(self, point):
        return math.hypot(self.position[0]-point[0], self.position[1]-point[1])


class Wizard(Entity):
    def __init__(self, entity_id, x, y, vx, vy, state):
        super().__init__(entity_id, x, y, vx, vy)

        self.is_holding = state==1
        self.target = None
        self.going_toward = None

    def update_properties(self, x, y, vx, vy, state):
        super().update_properties(x, y, vx, vy)
        self.is_holding = state==1

    def move(self,power, snaffle=None):
        #range of power 0 - 150

        # if snaffle:
        #     point = snaffle.position

        #     if self.target:
        #         self.target.targetted_by = None
        #     snaffle.targetted_by = self

        # else:
        #     point = (random.randint(1, 15999), random.randint(1, 3549))

        self.target = snaffle
        snaffle.targetted_by = self
        point = snaffle.position


        print(f"MOVE {point[0]} {point[1]} {power}")

    def throw(self, snaffle, point, power):
        #range of power 0 - 500

        # self.target.targetted_by = None
        # self.target = None
        print(f"THROW {point[0]} {point[1]} {power}")

    #not using
    def snaffles_in_my_area(self):
        snafflles = [
            snfl 
            for snfl in game.snaffles.values() 
            if (snfl.is_removed == False
                and 
                [abs(my_team.goal[0]-snfl.position[0])<=8000, abs(my_team.goal[0]-snfl.position[0])>8000][self.id])
            
        ]

        return snafflles

    #not using
    def get_behind_snaffle(self):
        behind_snaffles = sorted((snfl for snfl in game.snaffles.values() if not snfl.is_removed and snfl.get_distance(my_team.goal)<self.get_distance(my_team.goal)), key=lambda s:s.get_distance(my_team.goal), reverse=True)

        if behind_snaffles:
            return behind_snaffles[0]

        return None

    def snaffle_to_near_goal(self):
        for snaffle in [snfl for snfl in game.snaffles.values() if not snfl.is_removed]:
            if snaffle.get_distance(my_team.goal) <= 2000:
                return snaffle

        return None

    def get_nearest_snaffle(self):
        # possible_targets = self.snaffles_in_my_area()

        snaffles = sorted((
            snaffle 
            for snaffle in game.snaffles.values()
            # for snaffle in [game.snaffles.values(), possible_targets][len(possible_targets)>0]
            if (not snaffle.is_removed and snaffle.targetted_by==None)
        ), key=lambda s: self.get_distance(s.position))
        # print([(snf.id, round(self.get_distance(snf.position), 2)) for snf in snaffles], file=sys.stderr, flush=True)

        for snaffle in snaffles:
            snaffle_n_wizard = snaffle.get_nearest_my_wizard()

            if snaffle_n_wizard != self:
                continue

            return snaffle
        
        # if snaffles:
            
        #     return snaffles[0]
        
        return None

    def can_cast_flipendo(self):
        #need add budgers next
        for entity in opponent_team.wizards.values():
            if point_in_triangle(self.position, opponent_team.goal_bar1, opponent_team.goal_bar2, entity.position):
                return None

        print('wizerd or buldger in triangle', file=sys.stderr, flush=True)

        for snfl in [s for s in game.snaffles.values() if not s.is_removed]:
            if point_in_triangle(self.position, opponent_team.goal_bar1, opponent_team.goal_bar2, snfl.position):
                return snfl

            print(snfl.id, 'not in tringle', file=sys.stderr, flush=True)

        return None

    def act(self):
        print(f"acting {self.id}:", file=sys.stderr, flush=True)
        if self.is_holding:
            self.throw(self.target, opponent_team.goal, 500)
            print(f"{self.id} threw toward {opponent_team.goal}", file=sys.stderr, flush=True)
        
        else:

            #move target if have a targer or nearest
            # if self.target and self.target.is_removed==False:
            #     self.move(130, self.target)
            #     print(f"{self.id} moved toward {self.target.id}", file=sys.stderr, flush=True)

            # else:
            #     self.move(130, self.get_nearest_snaffle() or [snfl for snfl in game.snaffles.values() if not snfl.is_removed][0])
            
            if self.target:
                self.target.targetted_by = None
                self.target = None
            
            snafflle_near_goal = self.snaffle_to_near_goal()
            if snafflle_near_goal and my_team.magic >=20:
                if self.id == 0:
                    print(f'ACCIO {snafflle_near_goal.id}')
                else:
                    print(f"PETRIFICUS {snafflle_near_goal.get_nearest_enemy_wizard().id}")

            else:
                snaffle = self.get_nearest_snaffle() or [snfl for snfl in game.snaffles.values() if not snfl.is_removed][0]

                my_dist_f_mgoal = self.get_distance(my_team.goal)
                snfl_dist_f_mgoal = snaffle.get_distance(my_team.goal)

                snfl_to_flipendo = self.can_cast_flipendo()

                if my_team.magic >=20 and snfl_to_flipendo:

                    print(f"FLIPENDO {snfl_to_flipendo.id}")
                elif my_team.magic>=20 and my_dist_f_mgoal>snfl_dist_f_mgoal  and (abs(my_dist_f_mgoal-snfl_dist_f_mgoal)>=3500 and abs(my_dist_f_mgoal-snfl_dist_f_mgoal)<5500):
                    # self.target = snaffle
                    # snaffle.targetted_by = self

                    print(f'ACCIO {snaffle.id}')
                else:
                    self.move(130, snaffle)



class Snaffle(Entity):
    def __init__(self, entity_id, x, y, vx, vy, state):
        super().__init__(entity_id, x, y, vx, vy)

        self.is_grabbed = state==1
        self.targetted_by = None #only my wizards for now
        self.is_removed = False

    def update_properties(self, x, y, vx, vy, state):
        super().update_properties(x, y, vx, vy)
        self.is_grabbed = state==1

    #nearest wizard among my wizards
    def get_nearest_my_wizard(self):
        # print(f'finding nearest wizard for {self.id}', file=sys.stderr, flush=True)

        wizards = sorted((wizard for wizard in my_team.wizards.values() if wizard.target==None), key=lambda w: self.get_distance(w.position))
        # print("my wizards not holding", [(wz.id, round(self.get_distance(wz.position),2)) for wz in wizards], file=sys.stderr, flush=True)
        if wizards:
            return wizards[0]

        return None

    def get_nearest_enemy_wizard(self):
        enemy_n_wizards = sorted(
            opponent_team.wizards.values(),
            key=lambda w: self.get_distance(w.position)
        )

        return enemy_n_wizards[0]


class Bludger(Entity):
    def __init__(self, entity_id, x, y, vx, vy, state):
        super().__init__(entity_id, x, y, vx, vy)

        self.last_target = state #-1 otherwise

    def update_properties(self, x, y, vx, vy):
        super().update_properties(x, y, vx, vy)

        self.last_target = state


class Team:
    def __init__(self, team_id, score=None, magic=None):
        goal_pos = [(0, 3750), (16000, 3750)][team_id]
        self.id = team_id
        self.goal = goal_pos
        self.goal_bar1 = (goal_pos[0], goal_pos[1]-500)
        self.goal_bar2 = (goal_pos[0], goal_pos[1]+500)
        self.score = score
        self.magic = magic
        self.wizards = {}


class Game:
    def __init__(self):
        self.snaffles = {}
        self.bludgers = {}

    def get_snaffles(self):

        return [
            snaffle
            for snaffle in self.snaffles.values()
            if not snaffle.is_removed
        ]

    def get_bludgers(self):

        return [
            bludger
            for bludger in self.bludgers.values()
        ]

    def end_turn(self):
        for snf in self.snaffles.values():
            # print(snf.id,'speed', math.hypot(snf.speed[0], snf.speed[1]), file=sys.stderr, flush=True)
            snf.is_removed = True


game = Game()

# Grab snaffles and try to throw them through the opponent's goal!
# Move towards a Snaffle and use your team id to determine where you need to throw it.

my_team_id = int(input())  # if 0 you need to score on the right of the map, if 1 you need to score on the left
my_team = Team(my_team_id)
opponent_team = Team([1, 0][my_team_id])

# game loop
while True:
    my_score, my_magic = [int(i) for i in input().split()]
    my_team.magic = my_magic
    opponent_score, opponent_magic = [int(i) for i in input().split()]
    entities = int(input())  # number of entities still in game
    for i in range(entities):
        inputs = input().split()
        entity_id = int(inputs[0])  # entity identifier
        entity_type = inputs[1]  # "WIZARD", "OPPONENT_WIZARD" or "SNAFFLE" (or "BLUDGER" after first league)
        x = int(inputs[2])  # position
        y = int(inputs[3])  # position
        vx = int(inputs[4])  # velocity
        vy = int(inputs[5])  # velocity
        state = int(inputs[6])  # 1 if the wizard is holding a Snaffle, 0 otherwise

        if entity_type == 'WIZARD':
            wizard = my_team.wizards.get(entity_id, Wizard(entity_id, x, y, vx, vy, state))
            my_team.wizards[entity_id] = wizard
            wizard.update_properties(x, y, vx, vy, state)

        elif entity_type == 'OPPONENT_WIZARD':
            wizard = opponent_team.wizards.get(entity_id, Wizard(entity_id, x, y, vx, vy, state))
            opponent_team.wizards[entity_id] = wizard
            wizard.update_properties(x, y, vx, vy, state)

        elif entity_type == 'SNAFFLE':
            snaffle = game.snaffles.get(entity_id, Snaffle(entity_id, x, y, vx, vy, state))
            game.snaffles[entity_id] = snaffle
            snaffle.update_properties(x, y, vx, vy, state)
            snaffle.is_removed = False

        elif entity_type == 'BLUDGER':
            bludger = Bludger(entity_id, x, y, vx, vy, state)


    
    for wizard in my_team.wizards.values():

        # Write an action using print
        # To debug: print("Debug messages...", file=sys.stderr, flush=True)


        # Edit this line to indicate the action for each wizard (0 ≤ thrust ≤ 150, 0 ≤ power ≤ 500)
        # i.e.: "MOVE x y thrust" or "THROW x y power"
        wizard.act()

    game.end_turn()
