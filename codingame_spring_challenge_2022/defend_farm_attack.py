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
        self.dir = 1
        self.prev = 1

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


class Hero(Entity):
    def __init__(self, entity_id, x, y, shield_life, is_controlled, type, base=None):
        super().__init__(entity_id, x, y, shield_life, is_controlled, type)
        self.base = base
        self.allocate = None

    def __str__(self):

        return f"{self.type} - {self.id}"

    def cast_wind(self, x=8788, y=4536):
        print(f"SPELL WIND {x} {y}")
        self.base.mana -= 10

    def cast_shield(self, entity):
        print(f"SPELL SHIELD {entity.id}")
        self.base.mana -= 10
        entity.shield_life = 12

    def cast_control(self, entity):
        if entity.type == 'monster':
            x, y = game.opponent_base.position
        else:
            if entity.get_distance(self.base.position) < entity.get_distance(entity.base.position):
                x, y = entity.base.position

            else:
                x, y = self.base.position

        print(f"SPELL CONTROL {entity.id} {x} {y}")
        self.base.mana -= 10
        entity.is_controlled = True

    def move(self, x, y):

        print(f"MOVE {x} {y}")

    def sta(self):
        # p1 = (11729, 7506)
        p1 = (11018, 8956) if self.base.position[0] == 0 else (5960, 62)
        p2 = (13536, 4646) if self.base.position[0] == 0 else (4464, 4222)
        # p3 = (15916, 3127)
        p3 = (17846, 2689) if self.base.position[0] == 0 else (4, 6055)

        if self.dir == 1:
            self.move(p1[0], p1[1])
            if self.get_distance(p1) < 2200:
                self.dir = 2
                self.prev = 1

        elif self.dir == 2:
            self.move(p2[0], p2[1])
            if self.get_distance(p2) <= 805:
                if self.prev == 1:
                    self.dir = 3
                else: self.dir = 1

        elif self.dir == 3:
            self.move(p3[0], p3[1])
            if self.get_distance(p3) < 2200:
                self.dir = 2
                self.prev = 3

    def std(self):
        p1 = (1131, 1131) if self.base.position[0] == 0 else (16499, 7869)
        p2 = (4751, 1499) if self.base.position[0] == 0 else (16012, 4112)
        p3 = (1303, 4783) if self.base.position[0] == 0 else (12892, 7273)

        if self.dir == 1:
            if self.get_distance(p1)<=805:
                self.move(p2[0], p2[1])
                self.dir = 2
            else:
                self.move(p1[0], p1[1])
        
        elif self.dir == 2:
            if self.get_distance(p2)<=805:
                self.move(p3[0], p3[1])
                self.dir = 3
            else:
                self.move(p2[0], p2[1])

        else:
            if self.get_distance(p3)<=805:
                self.move(p1[0], p1[1])
                self.dir = 1
            else:
                self.move(p3[0], p3[1])


    def stf(self):
        p1 = (8774, 4523)

        self.move(p1[0], p1[1])



class Base:
    def __init__(self, x, y):
        self.position = (x, y)
        self.health = 3
        self.mana = 0
        self.heros = {}

    def get_distance(self, point):
        return math.hypot(self.position[0]-point[0], self.position[1]-point[1])


class Game:
    def __init__(self, base_x, base_y, heroes_per_player):
        self.my_base = Base(base_x, base_y)
        self.heroes_per_player = heroes_per_player
        self.monsters = {}

        self.opponent_base = Base(0 if base_x!=0 else 17630, 0 if base_y!=0 else 9000)

    def get_monsters_near_my_base(self):
        return sorted((m for m in self.monsters.values() if not m.is_removed), key=lambda x: x.get_distance(self.my_base.position))

    def get_monsters_near_me(self, hero):
        return sorted((m for m in self.monsters.values() if not m.is_removed), key=lambda x: x.get_distance(hero.position))
    
    def get_monsters(self):
        return [monster for monster in self.monsters.values() if not monster.is_removed and (monster.is_my_threat or not monster.is_opponent_threat)]
    
    def get_opponent_hero_near_my_base(self):
        opponent_heros = [oh for oh in self.opponent_base.heros.values() if oh.get_distance(self.my_base.position)<=6500]
        if opponent_heros:
            return opponent_heros[0]

        return None

    def get_monsters_opponent(self, hero):
        return sorted([monster for monster in self.monsters.values() if not monster.is_removed and not monster.is_my_threat], key=lambda x: x.get_distance(hero.position))

    def defend(self, hero):

        monsters = self.get_monsters_near_my_base()
        if monsters:
            monster = monsters[0]
            if self.my_base.get_distance(monster.position) <= 1500:
                if self.my_base.mana >= 10 and monster.shield_life==0:
                    if hero.get_distance(monster.position)<1280:
                        hero.cast_wind(self.opponent_base.position[0], self.opponent_base.position[1])
                    elif hero.get_distance(monster.position)<=2200 and not monster.is_controlled:
                        hero.cast_control(monster)

                    else:
                        hero.move(monster.position[0]+monster.speed[0], monster.position[1]+monster.speed[1])

                else:
                    hero.move(monster.position[0]+monster.speed[0], monster.position[1]+monster.speed[1])
            elif self.my_base.get_distance(monster.position) <= 6000:
                hero.move(monster.position[0]+monster.speed[0], monster.position[1]+monster.speed[1])

            else:
                hero.std()

            # elif monster.get_distance(self.my_base.position) < monster.get_distance(self.opponent_base.position) and monster.health>=19 and not monster.is_opponent_threat:
            #     if self.my_base.mana >= 10 and monster.shield_life==0:
            #         if hero.get_distance(monster.position)<2200:
            #             hero.cast_control(monster)
            #         else:
            #             hero.move(monster.position[0]+monster.speed[0], monster.position[1]+monster.speed[1])

            #     else:
            #         hero.move(monster.position[0]+monster.speed[0], monster.position[1]+monster.speed[1])

            # else:
            #     hero.move(monster.position[0]+monster.speed[0], monster.position[1]+monster.speed[1])

        else:
            hero.std()

        

    def farm(self, hero):
        should_farm = True
        opponent_hero_near_my_base = self.get_opponent_hero_near_my_base()
        if opponent_hero_near_my_base:
            if len([m for m in self.get_monsters() if m.get_distance(opponent_hero_near_my_base.position)<=2000]):
                should_farm = False
                self.stop_opponent_hero(hero, opponent_hero_near_my_base)

        if should_farm:

            monsters = self.get_monsters_near_me(hero)
            if monsters:
                monster = monsters[0]

                hero.move(monster.position[0]+monster.speed[0], monster.position[1]+monster.speed[1])

            else:
                hero.stf()

    def attack(self, hero):
        monsters = self.get_monsters_opponent(hero)
        if monsters:
            monster = monsters[0]

            if self.my_base.mana>=20 and monster.shield_life==0 and monster.get_distance(hero.position)<2200:

                if not monster.is_opponent_threat:
                    hero.cast_control(monster)
                elif monster.get_distance(hero.position)<1280:
                    hero.cast_wind(self.opponent_base.position[0], self.opponent_base.position[1])
                else:
                    hero.cast_shield(monster)

            else:
                hero.sta()

            


            # if self.my_base.mana >= 20 and monster.shield_life==0:
            
            #     if monster.get_distance(self.opponent_base.position) > hero.get_distance(self.opponent_base.position):

            #         #push
            #         if monster.get_distance(hero.position) <1280:
            #             hero.cast_wind(self.opponent_base.position[0], self.opponent_base.position[1])
                    
            #         #mind controll
            #         elif not monster.is_opponent_threat:
            #             hero.cast_control(monster)

            #         else:
            #             hero.move(monster.position[0], monster.position[1])
                
            #     else:
            #         #push
            #         if monster.get_distance(hero.position) <1280:
            #             hero.cast_wind(self.opponent_base.position[0], self.opponent_base.position[1])

            #         #mind control
            #         elif not monster.is_opponent_threat:
            #             hero.cast_control(monster)

            #         else:
            #             hero.cast_shield(monster)

            # else:
            #     hero.sta()
        else:
            hero.sta()

    
    def stop_opponent_hero(self,hero, oh):
        if hero.get_distance(oh.position) > 2200 and hero.get_distance(oh.position) < 3000 and hero.shield_life==0 and hero.base.mana >= 50:
            hero.cast_shield(hero)

        elif hero.get_distance(oh.position) < 2200 and hero.shield_life==0 and hero.base.mana >= 30:
            hero.cast_shield(hero)

        elif hero.get_distance(oh.position) < 1280 and hero.base.mana >= 10 and oh.shield_life==0 and oh.get_distance(self.my_base.position)<=4000:
            hero.cast_wind(oh.base.position[0], oh.base.position[1])
        else:
            hero.move(oh.position[0], oh.position[1])
        
    
    
    def initiate_turn(self):
        for h in self.my_base.heros.values():
            h.allocate = None

    def turn(self):
        for h in self.my_base.heros.values():
            if h.id == 0 or h.id == 3:
                self.defend(h)

            elif h.id == 1 or h.id == 4:
                # self.farm(h) 
                self.farm(h)

            elif h.id == 2 or h.id == 5:
                self.attack(h)

    def end_turn(self):
        for monster in self.monsters.values():
            monster.is_removed = True

        for h in self.opponent_base.heros.values():
            h.is_removed = True




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
    game.turn()
    game.end_turn()