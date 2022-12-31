import sys
import math


def intersect_points(m, r, xc, yc):
    a = m*m + 1
    b = -2*(xc - m*yc)
    c = xc*xc + yc*yc
    d = math.sqrt(b*b - 4*a*c)

    x1 = (-b + d)/(2*a)
    x2 = (-b - d)/(2*a)

    y1 = m*x1
    y2 = m*x2

    return (x1, y1, x2, y2)

class Entity:
    def __init__(self, entity_id, x, y, vx=-1, vy=-1, health=-1, near_base=-1, threat_for=-1):
        self.id = entity_id
        self.position = (x, y)
        self.speed = (vx, vy)
        self.health = health
        self.near_base = near_base
        self.is_my_threat = threat_for == 1
        self.is_opponent_threat = threat_for == 2

        self.is_removed = False
    
    @property
    def speed_value(self):
        return math.hypot(self.speed[0], self.speed[1])

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
    def __init__(self, entity_id, x, y, base=None):
        super().__init__(entity_id, x, y)
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

    # def act(self, monster):
    #     if self.id == 0 or self.id == 3:
    #         #hero near opponent base
    #         if self.get_distance(monster.position) <= 1280:
    #             print(f"SPELL WIND {game.opponent_base.position[0]} {game.opponent_base.position[1]}")
    #         else:
    #             print(f"MOVE {monster.position[0]} {monster.position[1]}")
    #     else:
    #         #hero near my base
    #         if monster.get_distance(self.base.position) <= 2000:
    #             print(f"SPELL WIND 8788 4536")
    #         else:
    #             print(f"MOVE {monster.position[0]} {monster.position[1]} moving {monster.id}")

    def act(self):
        monster = self.allocate
        if monster:
            if self.id == 0 or self.id == 3:
                #hero near opponent base
                #monster can contain opponent hero or monster for this hero
                if self.get_distance(monster.position) <= 1280 and self.base.mana >=10:
                    print(f"SPELL WIND {game.opponent_base.position[0]} {game.opponent_base.position[1]}")
                    self.base.mana -= 10
                else:
                    print(f"MOVE {monster.position[0]} {monster.position[1]}")
            
            else:
                #hero near my base
                if monster.get_distance(self.base.position) <= 3100:
                    if self.get_distance(monster.position) <= 1280 and self.base.mana >=10:
                        print(f"SPELL WIND 8788 4536")
                        self.base.mana -= 10
                    else:
                        print(f"MOVE {monster.position[0]} {monster.position[1]} moving {monster.id} mana{self.base.mana}")
                else:
                    print(f"MOVE {monster.position[0]} {monster.position[1]} bd {round(monster.get_distance(self.base.position))}")

        else:
            print(f"MOVE {self.rest_position[0]} {self.rest_position[1]} rest")


    #should only call from opponent hero
    # def get_nearest_hero_mine(self):
    #     heros = sorted(game.my_base.heros.values(), key=lambda h: self.get_distance(h.position))

    #     return heros[0]


    def get_rest_point(self):
        pass


class Monster(Entity):
    def __init__(self, entity_id, x, y, vx, vy, health, near_base, threat_for):
        super().__init__(entity_id, x, y, vx, vy, health, near_base, threat_for)

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
            h.act()
        
        
        
        
        
        # for i, h in enumerate(self.my_base.heros.values()):
        #     if h.id == 0 or h.id == 3:
        #         monsters = sorted(game.get_monsters_opponent(), key=lambda m: m.get_distance(h.position))

        #     else:
        #         monsters = sorted(self.get_monsters(), key=lambda m: (-m.get_rank(), m.get_distance(self.my_base.position)))
            
        #     if monsters:
        #         m = monsters[(i-1)%len(monsters)]
        #         h.act(m)

        #     else:
        #         print(f"MOVE {h.rest_position[0]} {h.rest_position[1]} rest")

    
    
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
            hero = game.my_base.heros.get(_id, Hero(_id, x, y, game.my_base))
            game.my_base.heros[_id] = hero
            hero.update_properties(x, y)

        elif _type == 0:
            monster = game.monsters.get(_id, Monster(_id, x, y, vx, vy, health, near_base, threat_for))
            game.monsters[_id] = monster
            monster.update_properties(x, y, vx, vy, health, near_base, threat_for)

        # elif _type == 2:
        #     hero = game.opponent_base.heros.get(_id, Hero(_id, x, y, game.opponent_base))
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
