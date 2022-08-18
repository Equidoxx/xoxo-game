from random import randint
class WrongIndexError(Exception): ...

class Cell:
    def __init__(self):
        self.value = 0

    def __bool__(self):
        return not bool(self.value)

class TicTacToe:
    FREE_CELL = 0  # свободная клетка
    HUMAN_X = 1  # крестик (игрок - человек)
    COMPUTER_O = 2  # нолик (игрок - компьютер)

    def __init__(self):
        self.pole = tuple(tuple(Cell() for _ in '123') for _ in '123')
        self.is_draw = self.is_computer_win = self.is_human_win = False

    def init(self):
        self.__init__()

    def check_index(self, item):
        if not isinstance(item, int) or not 1 <= item <= 9:
            raise WrongIndexError("Введите номер клетки, число от 1 до 9")
        x, y = (item - 1) // 3, (item - 1) % 3
        if not self.pole[x][y]:
            raise WrongIndexError("Клетка уже занята, введите другой номер клетки")
        return (x, y)


    def __getitem__(self, item):
        self.check_index(item)
        return self.pole[item[0]][item[1]].value

    def __setitem__(self, key, value):
        self.check_index(key)
        self.pole[key[0]][key[1]].value = value
        self.check_for_win()

    def show(self):
        print('-' * 9)
        for row in self.pole:
            for item in row:
                if item.value == 0:
                    print(' # ', end='')
                elif item.value == 1:
                    print(' X ', end='')
                elif item.value == 2:
                    print(' O ', end='')
            print()

    def human_go(self):
        print("Введите номер клетки для хода:")
        while True:
            try:
                cell_num = int(input())
                x, y = self.check_index(cell_num)
            except ValueError:
                print('Пожалуйста введите число')
            except WrongIndexError as z:
                print(z)
            else:
                break


        self.pole[x][y].value = 1
        self.check_for_win()

    def computer_go(self):
        x, y = randint(0, 2), randint(0, 2)
        while self.pole[x][y].value:
            x, y = randint(0, 2), randint(0, 2)
        self.pole[x][y].value = 2
        self.check_for_win()

    def check_for_win(self):
        m = self.pole
        fl = None
        for i in range(3):
            if m[i][0].value == m[i][1].value == m[i][2].value != 0:
                fl = (i, 0)
                break
            if m[0][i].value == m[1][i].value == m[2][i].value != 0:
                fl = (0, i)
                break
        if m[0][0].value == m[1][1].value == m[2][2].value != 0:
            fl = (0, 0)
        if m[0][2].value == m[1][1].value == m[2][0].value != 0:
            fl = (0, 2)
        if fl:
            if m[fl[0]][fl[1]].value == 1:
                self.is_human_win = True
                return
            else:
                self.is_computer_win = True
                return
        for row in m:
            for i in row:
                if not i.value:
                    fl = True
        if not fl:
            self.is_draw = True

    @property
    def is_human_win(self):
        return self.__is_human_win

    @is_human_win.setter
    def is_human_win(self, value):
        self.__is_human_win = value

    @property
    def is_computer_win(self):
        return self.__is_computer_win

    @is_computer_win.setter
    def is_computer_win(self, value):
        self.__is_computer_win = value

    @property
    def is_draw(self):
        return self.__is_draw

    @is_draw.setter
    def is_draw(self, value):
        self.__is_draw = value

    def __bool__(self):
        return not (self.is_draw or self.is_human_win or self.is_computer_win)


game = TicTacToe()
while True:
    game.init()
    while game:
        game.show()
        game.human_go()
        game.computer_go()
    if game.is_human_win:
        print('Поздравляю вы победили!!!')
    answ = input('Хотите сыграть еще раз? [да]:  ')
    if answ.lower() != 'да':
        break