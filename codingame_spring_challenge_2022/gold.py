"""
- refactor code
- entity(s) will move according to a path if nothing is visible to them
- use others magics
"""

import sys
import math


class Entity:
    def __init__(self, entity_id, x, y, type, vx=-1, vy=-1, health=-1, near_base=-1, threat_for=-1):
        self.id = entity_id
        self.position = (x, y)
        self.speed = (vx, vy)
        self.health = health
        self.near_base = near_base
        self.is_my_threat = threat_for == 1
        self.is_opponent_threat = threat_for == 2

        self.is_removed = False
        self.type = type

    def update_properties(self, x, y, vx=-1, vy=-1, health=-1, near_base=-1, threat_for=-1):
        self.position = (x, y)
        self.speed = (vx, vy)
        self.health = health
        self.near_base = near_base
        self.is_my_threat = threat_for == 1
        self.is_opponent_threat = threat_for == 2

        self.is_removed = False

    def get_distance(self, point):
        return math.hypot(self.position[0]-point[0], self.position[1]-point[1])


class Hero(Entity):
    def __init__(self, entity_id, x, y, type, base=None):
        super().__init__(entity_id, x, y, type)
        self.base = base
        self.allocate = None
        # self.rest_position_x = [[3205,14767][base.position[0]!=0], [3506,16409][base.position[0]!=0], [1290,13782][base.position[0]!=0]][entity_id]
        # self.rest_position_y = [[1800,6644][base.position[0]!=0], [391,5180][base.position[0]!=0], [3729,2265][base.position[0]!=0]][entity_id]

        if entity_id == 3:
            self.rest_position = (2500, 2100)
        elif entity_id == 4:
            # self.rest_position = (12500, 7600)
            self.rest_position = (9280, 6657)
        elif entity_id == 5:
            # self.rest_position = (16000, 4300)
            self.rest_position = (12332, 2689)
        elif entity_id == 0:
            self.rest_position = (15700, 6400)
        elif entity_id == 1:
            # self.rest_position = (1500, 4800)
            self.rest_position = (9321, 1431)
        elif entity_id == 2:
            # self.rest_position = (4700, 1600)
            self.rest_position = (4245, 6370)

    def cast_wind(self, x=8788, y=4536):
        print(f"SPELL WIND {game.opponent_base.position[0]} {game.opponent_base.position[1]}")
        self.base.mana -= 10

    def cast_shield(self, id):
        print(f"SPELL SHIELD {id}")
        self.base.mana -= 10

    def cast_controll(self, id):
        pass

    def move(self, x, y):
        print(f"MOVE {x} {y}")

    def search(self):
        self.move(self.rest_position[0], self.rest_position[1])

    def defend(self):
        entity = self.allocate
        if getattr(entity, 'type', None) == 'monster':
            if entity.get_distance(self.base.position) <= 1800:
                if self.get_distance(entity.position) <= 1280 and self.base.mana >=10:
                    self.cast_wind()
                else:
                    self.move(entity.position[0], entity.position[1])
            else:
                self.move(entity.position[0], entity.position[1])

        elif getattr(entity, 'type', None) == 'opponent_hero':
            pass
            
        
        else:
            self.search()

    def attack(self):
        entity = self.allocate
        if getattr(entity, 'type', None) == 'monster':
            if self.get_distance(entity.position) <= 1280 and self.base.mana >=10:
                #near me
                self.cast_wind(game.opponent_base.position[0], game.opponent_base.position[1])
            
            elif self.base.mana>=10 and self.get_distance(game.opponent_base.position)>entity.get_distance(game.opponent_base.position):
                #near opponent base than I do
                if entity.health >= 10 and entity.id not in self.base.shielded:
                    self.cast_shield(entity.id)
                    self.base.shielded.add(entity.id)

                else:
                    self.move(self.rest_position[0], self.rest_position[1])

            else:
                self.move(entity.position[0], entity.position[1])

        elif getattr(entity, 'type', None) == 'opponent_hero':
            pass
            
        
        else:
            self.search()


class Monster(Entity):
    def __init__(self, entity_id, x, y, type, vx, vy, health, near_base, threat_for):
        super().__init__(entity_id, x, y, type, vx, vy, health, near_base, threat_for)

    def get_rank(self):
        if self.near_base==1 and self.is_my_threat:
            return 1000

        elif self.is_my_threat:
            return 500

        elif self.near_base==1 and self.is_opponent_threat:
            return -1000

        else:
            return -500

    def get_nearest_hero_mine(self):
        heros = sorted(game.my_base.heros.values(), key=lambda h: self.get_distance(h.position))

        return heros[0]



class Base:
    def __init__(self, x, y):
        self.position = (x, y)
        self.health = 3
        self.mana = 0
        self.heros = {}

        self.hero_targeting = {}
        self.monster_targeted_by = {}

        self.shielded = set()

    def get_distance(self, point):
        return math.hypot(self.position[0]-point[0], self.position[1]-point[1])


class Game:
    def __init__(self, base_x, base_y, heroes_per_player):
        self.my_base = Base(base_x, base_y)
        self.heroes_per_player = heroes_per_player
        self.monsters = {}

        self.opponent_base = Base(0 if base_x!=0 else 17630, 0 if base_y!=0 else 9000)


    def get_monsters(self):
        return [monster for monster in self.monsters.values() if not monster.is_removed and (monster.is_my_threat or not monster.is_opponent_threat)]

    def get_monsters_opponent(self):
        return [monster for monster in self.monsters.values() if not monster.is_removed and monster.is_opponent_threat]

    def initiate_turn(self):
        key_values = [*self.my_base.hero_targeting.items()]
        for h, m in key_values:
            if m.is_removed:
                self.my_base.hero_targeting.pop(h)

        key_values = [*self.my_base.monster_targeted_by.items()]
        for m, h in key_values:
            monster = self.monsters.get(m)
            if monster.is_removed:
                self.my_base.monster_targeted_by.pop(m)

        for h in self.my_base.heros.values():
            h.allocate = None

    def turn(self):
        #for hero near my base
        monsters = sorted(self.get_monsters(), key=lambda m: (-m.get_rank(), m.get_distance(self.my_base.position)))
        if monsters:
            for m in monsters[:2]:
                hero = m.get_nearest_hero_mine()
                if not hero.allocate:
                    hero.allocate = m
                else:
                    #nearest my hero already allocated for a monster, assigning the monster to other hero
                    if hero.id == 1:
                        self.my_base.heros.get(2).allocate = m
                    elif hero.id == 2:
                        self.my_base.heros.get(1).allocate = m

        #for hero near opponent base
        monsters = sorted(self.get_monsters_opponent(), key=lambda m: -m.get_distance(self.opponent_base.position))
        # opponent_heros = sorted(self.get_heros_opponent(), key=lambda h: -h.get_distance(self.opponent_base.position))
        if monsters:
            for e in [*monsters][:1]:
                hero = e.get_nearest_hero_mine()
                if not hero.allocate:
                    hero.allocate = e


        for h in self.my_base.heros.values():
            if h.id == 0 or h.id==3:
                h.attack()
            else:
                h.defend()
    
    def end_turn(self):
        for monster in self.monsters.values():
            monster.is_removed = True

        # for h in self.opponent_base.heros.values():
        #     h.is_removed = True

    
    # def get_heros_opponent(self):

    #     return [h for h in self.opponent_base.heros.values() if not h.is_removed]




# base_x: The corner of the map representing your base
base_x, base_y = [int(i) for i in input().split()]
heroes_per_player = int(input())  # Always 3

game = Game(base_x, base_y, heroes_per_player)

# game loop
while True:
    for i in range(2):
        # health: Your base health
        # mana: Ignore in the first league; Spend ten mana to cast a spell
        health, mana = [int(j) for j in input().split()]
        if i == 0:
            game.my_base.health = health
            game.my_base.mana = mana


    entity_count = int(input())  # Amount of heros and monsters you can see
    for i in range(entity_count):
        # _id: Unique identifier
        # _type: 0=monster, 1=your hero, 2=opponent hero
        # x: Position of this entity
        # shield_life: Ignore for this league; Count down until shield spell fades
        # is_controlled: Ignore for this league; Equals 1 when this entity is under a control spell
        # health: Remaining health of this monster
        # vx: Trajectory of this monster
        # near_base: 0=monster with no target yet, 1=monster targeting a base
        # threat_for: Given this monster's trajectory, is it a threat to 1=your base, 2=your opponent's base, 0=neither
        _id, _type, x, y, shield_life, is_controlled, health, vx, vy, near_base, threat_for = [int(j) for j in input().split()]

        if _type == 1:
            hero = game.my_base.heros.get(_id, Hero(_id, x, y, 'my_hero', game.my_base))
            game.my_base.heros[_id] = hero
            hero.update_properties(x, y)

        elif _type == 0:
            monster = game.monsters.get(_id, Monster(_id, x, y, 'monster', vx, vy, health, near_base, threat_for))
            game.monsters[_id] = monster
            monster.update_properties(x, y, vx, vy, health, near_base, threat_for)

        # elif _type == 2:
        #     hero = game.opponent_base.heros.get(_id, Hero(_id, x, y, 'opponent_hero', game.opponent_base))
        #     game.opponent_base.heros[_id] = hero
        #     hero.update_properties(x, y)
            
    game.initiate_turn()

    # monsters = sorted(game.get_monsters(), key=lambda m: (-m.get_rank(), m.get_distance(game.my_base.position)))
    # for i in range(heroes_per_player):
    #     if monsters:
    #         print(f"MOVE {monsters[i%len(monsters)].position[0]} {monsters[i%len(monsters)].position[1]}")
        
        
    #     else:
    #         print("WAIT")

    game.turn()

    game.end_turn()

    print(game.my_base.position, file=sys.stderr, flush=True)
