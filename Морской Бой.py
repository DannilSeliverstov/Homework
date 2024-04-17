from random import randint

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"


class BattleError(Exception):
    pass


class BattleOutOfBounds(BattleError):
    def __str__(self):
        return "Вы не можете выстрелить за пределы поля"


class BattleAlreadyShot(BattleError):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"


class BattleInvalidShip(BattleError):
    pass


class Vessel:
    def __init__(self, bow, length, orientation):
        self.bow = bow
        self.length = length
        self.orientation = orientation
        self.lives = length

    @property
    def dots(self):
        ship_points = []
        for i in range(self.length):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.orientation == 0:
                cur_x += i

            elif self.orientation == 1:
                cur_y += i

            ship_points.append(Dot(cur_x, cur_y))

        return ship_points

    def shooten(self, shot):
        return shot in self.dots


class Field:
    def __init__(self, hidden=False, size=6):
        self.size = size
        self.hidden = hidden

        self.hits = 0

        self.grid = [["O"] * size for _ in range(size)]

        self.used = []
        self.vessels = []

    def add_vessel(self, vessel):

        for p in vessel.dots:
            if self.out_of_bounds(p) or p in self.used:
                raise BattleInvalidShip()
        for p in vessel.dots:
            self.grid[p.x][p.y] = "■"
            self.used.append(p)

        self.vessels.append(vessel)
        self.contour(vessel)

    def contour(self, vessel, verbose=False):
        adjacent = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for p in vessel.dots:
            for dx, dy in adjacent:
                cur = Dot(p.x + dx, p.y + dy)
                if not (self.out_of_bounds(cur)) and cur not in self.used:
                    if verbose:
                        self.grid[cur.x][cur.y] = "T"
                    self.used.append(cur)

    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.grid):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hidden:
            res = res.replace("■", "O")
        return res

    def out_of_bounds(self, p):
        return not ((0 <= p.x < self.size) and (0 <= p.y < self.size))

    def shoot(self, p):
        if self.out_of_bounds(p):
            raise BattleOutOfBounds()

        if p in self.used:
            raise BattleAlreadyShot()

        self.used.append(p)

        for vessel in self.vessels:
            if p in vessel.dots:
                vessel.lives -= 1
                self.grid[p.x][p.y] = "X"
                if vessel.lives == 0:
                    self.hits += 1
                    self.contour(vessel, verbose=True)
                    print("Убит")
                    return False
                else:
                    print("Ранен")
                    return True

        self.grid[p.x][p.y] = "T"
        print("Промах")
        return False

    def reset(self):
        self.used = []


class Player:
    def __init__(self, field, opponent):
        self.field = field
        self.opponent = opponent

    def request_shot(self):
        raise NotImplementedError()

    def execute_shot(self):
        while True:
            try:
                target = self.request_shot()
                repeat = self.opponent.shoot(target)
                return repeat
            except BattleError as e:
                print(e)


class AI(Player):
    def request_shot(self):
        p = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {p.x + 1} {p.y + 1}")
        return p


class User(Player):
    def request_shot(self):
        while True:
            coordinates = input("Ход Игрока (пример: 1 1): ").split()

            if len(coordinates) != 2:
                print("Неверный ввод")
                continue

            x, y = coordinates

            if not (x.isdigit()) or not (y.isdigit()):
                print("Неверный ввод")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


class Game:
    def __init__(self, size=6):
        self.size = size
        user_field = self.random_field()
        ai_field = self.random_field()
        ai_field.hidden = True

        self.ai_player = AI(ai_field, user_field)
        self.user_player = User(user_field, ai_field)

    def random_field(self):
        field = None
        while field is None:
            field = self.generate_field()
        return field

    def generate_field(self):
        vessel_lengths = [3, 2, 2, 1, 1, 1, 1]
        field = Field(size=self.size)
        attempts = 0
        for length in vessel_lengths:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                vessel = Vessel(Dot(randint(0, self.size), randint(0, self.size)), length, randint(0, 1))
                try:
                    field.add_vessel(vessel)
                    break
                except BattleInvalidShip:
                    pass
        field.reset()
        return field


    def loop(self):
        num = 0
        while True:
            print("Доска игрока:")
            print(self.user_player.field)
            print("Доска компьютера:")
            print(self.ai_player.field)
            if num % 2 == 0:
                print("Ход игрока")
                repeat = self.user_player.execute_shot()
            else:
                repeat = self.ai_player.execute_shot()
            if repeat:
                num -= 1

            if self.ai_player.field.hits == 7:
                print("Пользователь выиграл")
                break

            if self.user_player.field.hits == 7:
                print("Компьютер выиграл")
                break
            num += 1

    def start(self):
        self.loop()


g = Game()
g.start()
