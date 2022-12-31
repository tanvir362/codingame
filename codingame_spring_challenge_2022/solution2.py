"""
- Three defender as well attacker
- Controll enemy's heros
- refactor code
"""

import sys
import math


class Entity:
    def __init__(self, entity_id, x, y, shield_life, is_controlled, type, vx=-1, vy=-1, health=-1, near_base=-1, threat_for=-1):
        self.id = entity_id
        self.position = (x, y)
        self.shield_life = shield_life
        self.is_controlled = is_controlled == 1
        self.speed = (vx, vy)
        self.health = health
        self.near_base = near_base
        self.is_my_threat = threat_for == 1
        self.is_opponent_threat = threat_for == 2

        self.is_removed = False
        self.type = type


    def update_properties(self, x, y, shield_life, is_controlled, vx=-1, vy=-1, health=-1, near_base=-1, threat_for=-1):
        self.position = (x, y)
        self.shield_life = shield_life
        self.is_controlled = is_controlled
        self.speed = (vx, vy)
        self.health = health
        self.near_base = near_base
        self.is_my_threat = threat_for == 1
        self.is_opponent_threat = threat_for == 2

        self.is_removed = False

    def get_distance(self, point):
        return math.hypot(self.position[0]-point[0], self.position[1]-point[1])


class Hero(Entity):
    def __init__(self, entity_id, x, y, shield_life, is_controlled, type, base=None):
        super().__init__(entity_id, x, y, shield_life, is_controlled, type)
        self.base = base
        self.allocate = None
        # self.rest_position_x = [[3205,14767][base.position[0]!=0], [3506,16409][base.position[0]!=0], [1290,13782][base.position[0]!=0]][entity_id]
        # self.rest_position_y = [[1800,6644][base.position[0]!=0], [391,5180][base.position[0]!=0], [3729,2265][base.position[0]!=0]][entity_id]

        # if entity_id == 3:
        #     self.rest_position = (9321, 6397)
        # elif entity_id == 4:
        #     self.rest_position = (4505, 6616)
        # elif entity_id == 5:
        #     self.rest_position = (12208, 2457)
        # elif entity_id == 0:
        #     self.rest_position = (8131, 2511)
        # elif entity_id == 1:
        #     self.rest_position = (13152, 2210)
        # elif entity_id == 2:
        #     self.rest_position = (5449, 6534)

        if entity_id == 3:
            self.rest_position = (9321, 6397)
        elif entity_id == 4:
            self.rest_position = (4505, 6616)
        elif entity_id == 5:
            self.rest_position = (12208, 2457)
        elif entity_id == 0:
            # self.rest_position = (12756, 4277)
            self.rest_position = (15700, 6400)
        elif entity_id == 1:
            self.rest_position = (5750, 2744)
        elif entity_id == 2:
            self.rest_position = (2015, 6137)

    def __str__(self):

        return f"{self.type} - {self.id}"

    def cast_wind(self, x=8788, y=4536):
        print(f"SPELL WIND {x} {y}")
        self.base.mana -= 10

    def cast_shield(self, id):
        print(f"SPELL SHIELD {id}")
        self.base.mana -= 10

    def cast_control(self, entity):
        if self.get_distance(self.base.position) <= 6000 and self.shield_life==0:
            self.cast_shield(self.id)
            self.base.mana -= 10
            return    

        if entity.get_distance(self.base.position) < entity.get_distance(entity.base.position):
            x, y = entity.base.position

        else:
            x, y = self.base.position

        print(f"SPELL CONTROL {entity.id} {x} {y}")
        self.base.mana -= 10
        entity.is_controlled = True

    def move(self, x, y):
        if math.hypot(self.base.position[0]-x, self.base.position[1]-y)<=7500 and not (self.id==0 or self.id == 3):
            print(f"MOVE {x} {y}")
        else:
            print(f"MOVE {self.rest_position[0]} {self.rest_position[1]}")

    def search(self):
        self.move(self.rest_position[0], self.rest_position[1])

    def defend(self, entity):
        if entity.get_distance(self.base.position) <= 2000:
            if self.get_distance(entity.position) < 1280 and self.base.mana >=10 and entity.shield_life==0:
                self.cast_wind()
            else:
                self.move(entity.position[0], entity.position[1])
        else:
            self.move(entity.position[0], entity.position[1])

    def attack(self, entity):
        if self.base.mana >=10:
            if self.get_distance(entity.position) < 1280 and entity.shield_life==0:
                self.cast_wind(game.opponent_base.position[0], game.opponent_base.position[1])

            elif self.get_distance(game.opponent_base.position)>entity.get_distance(game.opponent_base.position) and self.get_distance(entity.position) < 2200:
                if entity.health >= 10 and entity.shield_life == 0:
                    #near opponent base than I do
                    self.cast_shield(entity.id)

                else:
                    self.search()

            else:
                self.search()
        
        else:
            if self.get_distance(entity.position)>805:
                self.move(entity.position[0], entity.position[1])

            else:
                self.search()


    def act(self):
        entity = self.allocate
        # print(f"{str(self)} acting", file=sys.stderr, flush=True)
        if getattr(entity, 'type', None) == 'monster':
            if entity.is_opponent_threat:
                self.attack(entity)

            else:
                self.defend(entity)

        elif getattr(entity, 'type', None) == 'opponent_hero':
            if self.base.mana >= 10 and entity.shield_life==0:
                if self.get_distance(entity.position) < 1280:
                    self.cast_wind(entity.base.position[0], entity.base.position[1])
                else:
                    self.cast_control(entity)
            else:
                self.move(entity.position[0], entity.position[1])

        else:
            self.search()

    def get_opponent_hero_to_controll(self, gm):
        opponent_heros = [oh for oh in gm.get_heros_opponent() if self.get_distance(oh.position)<2200 and (not oh.is_controlled) and oh.shield_life==0 and (oh.get_distance(self.base.position) <= 7500 or oh.get_distance(oh.base.position)<=5000)]

        if opponent_heros and gm.get_monsters_inside_my_base():
            return opponent_heros[0]

        return None



class Monster(Entity):
    def __init__(self, entity_id, x, y, shield_life, is_controlled, type, vx, vy, health, near_base, threat_for):
        super().__init__(entity_id, x, y, shield_life, is_controlled, type, vx, vy, health, near_base, threat_for)
    
    def __str__(self):

        return f"{self.type} - {self.id}"
        
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

    def get_distance(self, point):
        return math.hypot(self.position[0]-point[0], self.position[1]-point[1])


class Game:
    def __init__(self, base_x, base_y, heroes_per_player):
        self.my_base = Base(base_x, base_y)
        self.heroes_per_player = heroes_per_player
        self.monsters = {}

        self.opponent_base = Base(0 if base_x!=0 else 17630, 0 if base_y!=0 else 9000)


    def get_monsters(self):
        return [monster for monster in self.monsters.values() if not monster.is_removed]

    def get_monsters_inside_my_base(self):
        return sorted([monster for monster in self.monsters.values() if not monster.is_removed and monster.get_distance(self.my_base.position)<=5000], key=lambda m:m.get_distance(self.my_base.position))

    def get_monsters_outside_my_base(self):
        return [monster for monster in self.monsters.values() if not monster.is_removed and monster.get_distance(self.my_base.position)>5000]
    
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
        monsters_inside_my_base = self.get_monsters_inside_my_base()
        print('sorted monsters inside my base', *map(lambda e: e.__str__(), monsters_inside_my_base), file=sys.stderr, flush=True)
        for monster in monsters_inside_my_base[:2]:
            heros_near_monster = sorted(self.my_base.heros.values(), key=lambda h: monster.get_distance(h.position))
            for hero in [h for h in heros_near_monster if h.id != 0 and h.id != 3]:
                if not hero.allocate:
                    opponent_hero_to_controll = hero.get_opponent_hero_to_controll(self)

                    if opponent_hero_to_controll:
                        hero.allocate = opponent_hero_to_controll

                    else:

                        hero.allocate = monster
                    break
        
        # monsters_outside_my_base = self.get_monsters_outside_my_base()
        print('all monsters visible to me\n', *map(str, (m for m in self.monsters.values() if not m.is_removed)), file=sys.stderr, flush=True)
        for hero in self.my_base.heros.values():
            opponent_hero_to_controll = hero.get_opponent_hero_to_controll(self)
            if opponent_hero_to_controll:
                hero.allocate = opponent_hero_to_controll

            print(f"{str(hero)} allocates {str(hero.allocate)}", file=sys.stderr, flush=True)
            if not hero.allocate:
                nearest_monster = None
                
                nearest_monsters = sorted((m for m in self.monsters.values() if not m.is_removed), key=lambda mn:mn.get_distance(hero.position))
                print('nearest monsters\n', *map(str, nearest_monsters), file=sys.stderr, flush=True)
                if nearest_monsters:
                    nearest_monster = nearest_monsters[0]

                print(f"nearest {str(nearest_monster)}", file=sys.stderr, flush=True)
                if nearest_monster:
                    hero.allocate = nearest_monster


        for h in self.my_base.heros.values():
            h.act()
    
    def end_turn(self):
        for monster in self.monsters.values():
            monster.is_removed = True

        for h in self.opponent_base.heros.values():
            h.is_removed = True

    
    def get_heros_opponent(self):

        return [h for h in self.opponent_base.heros.values() if not h.is_removed]




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
        if i==1:
            game.opponent_base.health = health
            game.opponent_base.mana = mana


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
            hero = game.my_base.heros.get(_id, Hero(_id, x, y, shield_life, is_controlled, 'my_hero', game.my_base))
            game.my_base.heros[_id] = hero
            hero.update_properties(x, y, shield_life, is_controlled)

        elif _type == 0:
            monster = game.monsters.get(_id, Monster(_id, x, y, shield_life, is_controlled, 'monster', vx, vy, health, near_base, threat_for))
            game.monsters[_id] = monster
            monster.update_properties(x, y, shield_life, is_controlled, vx, vy, health, near_base, threat_for)

        elif _type == 2:
            hero = game.opponent_base.heros.get(_id, Hero(_id, x, y, shield_life, is_controlled, 'opponent_hero', game.opponent_base))
            game.opponent_base.heros[_id] = hero
            hero.update_properties(x, y, shield_life, is_controlled)
            
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
