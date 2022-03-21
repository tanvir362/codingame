import random
import sys
import math


class Entity:
    def __init__(self, entity_id, x, y, vx, vy):
        self.id = entity_id
        self.position = (x, y)
        self.speed = (vx, vy)

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

    def snaffles_in_my_area(self):
        snafflles = [
            snfl 
            for snfl in game_snaffles.values() 
            if (snfl.is_removed == False
                and 
                [abs(my_team.goal[0]-snfl.position[0])<=8000, abs(my_team.goal[0]-snfl.position[0])>8000][self.id])
            
        ]

        return snafflles

    def get_behind_snaffle(self):
        behind_snaffles = sorted((snfl for snfl in game_snaffles.values() if not snfl.is_removed and snfl.get_distance(my_team.goal)<self.get_distance(my_team.goal)), key=lambda s:s.get_distance(my_team.goal), reverse=True)

        if behind_snaffles:
            return behind_snaffles[0]

        return None

    def get_nearest_snaffle(self):
        # possible_targets = self.snaffles_in_my_area()

        snaffles = sorted((
            snaffle 
            for snaffle in game_snaffles.values()
            # for snaffle in [game_snaffles.values(), possible_targets][len(possible_targets)>0]
            if (not snaffle.is_removed and snaffle.targetted_by==None)
        ), key=lambda s: self.get_distance(s.position))
        # print([(snf.id, round(self.get_distance(snf.position), 2)) for snf in snaffles], file=sys.stderr, flush=True)

        for snaffle in snaffles:
            snaffle_n_wizard = snaffle.get_nearest_wizard()

            if snaffle_n_wizard != self:
                continue

            return snaffle
        
        # if snaffles:
            
        #     return snaffles[0]
        
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
            #     self.move(130, self.get_nearest_snaffle() or [snfl for snfl in game_snaffles.values() if not snfl.is_removed][0])
            
            if self.target:
                self.target.targetted_by = None
                self.target = None
            
            
            
            self.move(130, self.get_nearest_snaffle() or [snfl for snfl in game_snaffles.values() if not snfl.is_removed][0])



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
    def get_nearest_wizard(self):
        # print(f'finding nearest wizard for {self.id}', file=sys.stderr, flush=True)

        wizards = sorted((wizard for wizard in my_team.wizards.values() if wizard.target==None), key=lambda w: self.get_distance(w.position))
        # print("my wizards not holding", [(wz.id, round(self.get_distance(wz.position),2)) for wz in wizards], file=sys.stderr, flush=True)
        if wizards:
            return wizards[0]

        return None


class Bludger(Entity):
    def __init__(self, entity_id, x, y, vx, vy, state):
        super().__init__(entity_id, x, y, vx, vy)


class Team:
    def __init__(self, team_id, score=None, magic=None):
        self.id = team_id
        self.goal = [(0, 3750), (16000, 3750)][team_id]
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

game_snaffles = {}
def end_turn():
    for snf in game_snaffles.values():
        snf.is_removed = True


# Grab snaffles and try to throw them through the opponent's goal!
# Move towards a Snaffle and use your team id to determine where you need to throw it.

my_team_id = int(input())  # if 0 you need to score on the right of the map, if 1 you need to score on the left
my_team = Team(my_team_id)
opponent_team = Team([1, 0][my_team_id])

# game loop
while True:
    my_score, my_magic = [int(i) for i in input().split()]
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
            snaffle = game_snaffles.get(entity_id, Snaffle(entity_id, x, y, vx, vy, state))
            game_snaffles[entity_id] = snaffle
            snaffle.update_properties(x, y, vx, vy, state)
            snaffle.is_removed = False


    
    for wizard in my_team.wizards.values():

        # Write an action using print
        # To debug: print("Debug messages...", file=sys.stderr, flush=True)


        # Edit this line to indicate the action for each wizard (0 ≤ thrust ≤ 150, 0 ≤ power ≤ 500)
        # i.e.: "MOVE x y thrust" or "THROW x y power"
        wizard.act()

    end_turn()
