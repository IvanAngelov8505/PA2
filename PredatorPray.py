import random
import time
pred_birth = 20     # After how many clocks it reproduces
prey_birth = 7
pred_health = 10     # Starting health of a predator


class Creature:
    habitat = []
    creatures = []

    @classmethod
    def getCount(cls):
        creatures_count = [0, 0]
        for creature in cls.creatures:
            if isinstance(creature, Predator):
                creatures_count[0] += 1
            else:
                creatures_count[1] += 1
        return creatures_count

    def __init__(self, x, y):
        self.pos_x = x
        self.pos_y = y
        Creature.creatures.append(self)
        Creature.habitat[y][x] = self
        self.birthrate = random.randint(self.birthrate-5, self.birthrate+5)

    def move(self, keep_original=False):
        directions = ["up", "down", "left", "right"]
        random.shuffle(directions)
        for direction in directions:
            if self.move_if_possible(direction, keep_original):
                return True

    def remove(self):
        Creature.habitat[self.pos_y][self.pos_x] = None
        Creature.creatures.remove(self)

    def move_if_possible(self, direction, keep_original):

        # left
        if direction == "left" and self.pos_x > 0 and Creature.habitat[self.pos_y][self.pos_x - 1] is None:
            Creature.habitat[self.pos_y][self.pos_x - 1] = self
            if not keep_original:
                Creature.habitat[self.pos_y][self.pos_x] = None
            self.pos_x -= 1
            return True

        # right
        limit = len(Creature.habitat[0])-1
        if direction == "right" and self.pos_x < limit and Creature.habitat[self.pos_y][self.pos_x + 1] is None:
            Creature.habitat[self.pos_y][self.pos_x + 1] = self
            if not keep_original:
                Creature.habitat[self.pos_y][self.pos_x] = None
            self.pos_x += 1
            return True

        # up
        if direction == "up" and self.pos_y > 0 and Creature.habitat[self.pos_y - 1][self.pos_x] is None:
            Creature.habitat[self.pos_y - 1][self.pos_x] = self
            if not keep_original:
                Creature.habitat[self.pos_y][self.pos_x] = None
            self.pos_y -= 1
            return True

        # down
        if direction == "down" and self.pos_y < len(Creature.habitat)-1 and Creature.habitat[self.pos_y + 1][self.pos_x] is None:
            Creature.habitat[self.pos_y + 1][self.pos_x] = self
            if not keep_original:
                Creature.habitat[self.pos_y][self.pos_x] = None
            self.pos_y += 1
            return True

        return False

    def reproduce(self):
        self.birthrate -= 1
        if self.birthrate < 0:
            currx, curry = self.pos_x, self.pos_y
            if self.move(False):
                self.reset_birthrate()
                type(self)(currx, curry)


class Predator(Creature):
    birthrate = pred_birth
    health = pred_health

    def reset_birthrate(self):
        self.birthrate = random.randint(pred_birth-5, pred_birth+5)

    def move(self, keep_original=False):
        if self.hunt():
            self.health = pred_health
        else:
            if self.health < 0:
                self.remove()
                return
            self.health -= 1
            super().move(keep_original)
        return True

    def hunt(self):
        if self.pos_x > 0 and isinstance(Creature.habitat[self.pos_y][self.pos_x - 1], Prey):
            Creature.creatures.remove(Creature.habitat[self.pos_y][self.pos_x - 1])
            Creature.habitat[self.pos_y][self.pos_x - 1] = self
            Creature.habitat[self.pos_y][self.pos_x] = None
            self.pos_x -= 1
            return True

        # right
        limit = len(Creature.habitat[0])-1
        if self.pos_x < limit and isinstance(Creature.habitat[self.pos_y][self.pos_x + 1], Prey):
            Creature.creatures.remove(Creature.habitat[self.pos_y][self.pos_x + 1])
            Creature.habitat[self.pos_y][self.pos_x + 1] = self
            Creature.habitat[self.pos_y][self.pos_x] = None
            self.pos_x += 1
            return True

        # up
        if self.pos_y > 0 and isinstance(Creature.habitat[self.pos_y - 1][self.pos_x], Prey):
            Creature.creatures.remove(Creature.habitat[self.pos_y - 1][self.pos_x])
            Creature.habitat[self.pos_y - 1][self.pos_x] = self
            Creature.habitat[self.pos_y][self.pos_x] = None
            self.pos_y -= 1
            return True

        # down
        if self.pos_y < len(Creature.habitat)-1 and isinstance(Creature.habitat[self.pos_y + 1][self.pos_x], Prey):
            Creature.creatures.remove(Creature.habitat[self.pos_y + 1][self.pos_x])
            Creature.habitat[self.pos_y + 1][self.pos_x] = self
            Creature.habitat[self.pos_y][self.pos_x] = None
            self.pos_y += 1
            return True


        return False

    def __repr__(self):
        return "X"


class Prey(Creature):
    birthrate = 10


    def reset_birthrate(self):
        self.birthrate = 10

    def __repr__(self):
        return "O"


class Habitat:

    def __init__(self, height=10, width=20, predators=50, prey=50):
        self.width = width
        self.height = height
        self.grid = []
        for i in range(height):
            row = [None] * width
            self.grid.append(row)
        Creature.habitat = self.grid
        self.spawn(Predator, predators)
        self.spawn(Prey, prey)

    def show(self):
        for row in Creature.habitat:
            print("|", end="")
            for cell in row:
                print("." if cell is None else cell, end="  ")
            print("|")

    def spawn(self, cls, count=10):
        if count < self.width * self.height:
            for i in range(count):
                valid_spot = False
                row, col = 0, 0
                while not valid_spot:
                    col = random.randint(0, self.width-1)
                    row = random.randint(0, self.height-1)
                    valid_spot = Creature.habitat[row][col] is None
                Creature.habitat[row][col] = cls(col, row)

    def emulate(self, sleep=0.3, show=True):
        clocks = 0
        while True:
            clocks += 1
            start = time.perf_counter()
            for creature in Creature.creatures:
                creature.reproduce()
                try:
                    creature.move()
                except:
                    pass
            end = time.perf_counter()
            if show:
                difference = end - start
                if sleep > difference:
                    time.sleep(sleep-difference)
                    print("Sleep can be shorter")
                print("\n\n")
                print("-"*self.width*3)
                self.show()
                type_count = Creature.getCount()
                print(f"Clocks: {clocks} \t Predators: {type_count[0]} \t Prey: {type_count[1]}")
                print("-" * self.width * 3)
                if type_count[0] == 0 or type_count[1] == 0:
                    break
            elif clocks % 100 == 0:
                type_count = Creature.getCount()
                print(f"Clocks: {clocks} \t Predators: {type_count[0]} \t Prey: {type_count[1]}")
                if type_count[0] == 0 or type_count[1] == 0:
                    break


f = Habitat(height=40, width=40, predators=30, prey=100)
f.emulate(sleep=0.2, show=False)





