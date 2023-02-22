# from colorama import just_fix_windows_console
import random

from colorama import just_fix_windows_console
# import time
# import logging

just_fix_windows_console()


# def setup_logger(name, log_file, level=logging.DEBUG):
#     # To setup as many loggers as you want
#     handler = logging.FileHandler(log_file, 'w', 'utf-8')
#     logger = logging.getLogger(name)
#     logger.setLevel(level)
#     logger.addHandler(handler)
#     return logger


# 1. input validation
#
# 2. Board class
#     self.guesses = []
#     self.ships = []
#     sieze
#     name
#     type
#     num ships

class Colors:
    """
    colors
    """
    RESETALL = '\x1b[0m'  # reset all (colors and brightness)
    BRIGHT = '\x1b[1m'  # bright
    DIM = '\x1b[2m'  # dim (looks same as normal brightness)
    NORMANL = '\x1b[22m'  # normal brightness

    # FOREGROUND:
    FGBLACK = '\x1b[30m'
    FGRED = '\x1b[31m'
    FGGREEN = '\x1b[32m'
    FGYELLOW = '\x1b[33m'
    FGBLUE = '\x1b[34m'
    FGMAGENTA = '\x1b[35m'
    FGCYAN = '\x1b[36m'
    FGWHITE = '\x1b[37m'
    FGRESET = '\x1b[39m'

    # BACKGROUND
    BGBLACK = '\x1b[40m'
    BGRED = '\x1b[41m'
    BGGREEN = '\x1b[42m'
    BGYELLOW = '\x1b[43m'
    BGBLUE = '\x1b[44m'
    BGMAGENTA = '\x1b[45m'
    BGCYAN = '\x1b[46m'
    BGWHITE = '\x1b[47m'
    BGRESET = '\x1b[49m'

    UNDERLINE_ON = "\033[4m"
    UNDERLINE_OFF = "\033[0m"
    # ESC[y;xH  # position cursor at x across, y down
    # ESC[y;xf  # position cursor at x across, y down
    # ESC[nA  # move cursor n lines up
    # ESC[nB  # move cursor n lines down
    # ESC[nC  # move cursor n characters forward
    # ESC[nD  # move cursor n characters backward

    # clear the screen
    CLS = '\x1b[2J'  # clear the screen

    # clear the line
    CLEARLINE = '\x1b[1K'  # clear the line

    # cursor positioning
    def position(x, y, text):
        """
        # position cursor at x across, y down and print text
        """
        print(f"\x1b[{y};{x}H{text}")


class Board:
    """
    board
    """
    def __init__(self, size, num_ships, name, type):
        self.size = size
        self.type = type
        if self.type == "pers":
            self.board = [["." for x in range(size)] for y in range(size)]
            # self.log = setup_logger("log", "pers.log")
        else:
            self.board = [["." for x in range(size)] for y in range(size)]
            # self.board[2][3] = "%"
            # self.log = setup_logger("log", "comp.log")
        self.num_ships = num_ships
        self.ships = []
        self.moves = []
        self.columns = [i for i in range(1, self.size + 1)]
        self.rows = [chr(ord(str(i)) + 49) for i in range(self.size)]
        print(self.columns)
        print(self.rows)
        while len(self.ships) < self.num_ships:
            a = random.randint(1, self.size)
            b = random.randint(1, self.size)
            if [a, b] not in self.ships:
                self.ships.append([a, b])

        self.name = name

    def setupboard(self):
        """ setup the board """
        pass

    def showboard(self):
        """ show the board """
        ship = "#"
        shell = Colors.BGRED+Colors.BRIGHT+"X"+Colors.RESETALL
        startcolumn = 3
        startrow = 5
        horizontalspacer = 3
        verticalspacer = 2
        if self.type == "comp":
            startcolumn = 30 + self.size
        Colors.position(startcolumn, startrow,
            f"{Colors.FGCYAN + Colors.BRIGHT + Colors.UNDERLINE_ON}{self.name}'s board{Colors.UNDERLINE_OFF}")
        columnlabel = " ".join([str(i) + " " for i in self.columns])
        Colors.position(startcolumn + 2, startrow + 2, f"{Colors.FGCYAN + Colors.BRIGHT}{columnlabel}")

        # Colors.position(startcolumn, startrow, f"{Colors.FGCYAN + Colors.BRIGHT}{self.name}'s board")
        for x in range(self.size):
            Colors.position(startcolumn,
                            (x * verticalspacer) + verticalspacer + startrow + 2,
                            f"{Colors.FGCYAN + Colors.BRIGHT + self.rows[x]}")
            for y in range(self.size):
                text = self.board[x][y]
                # if [x+1, y+1] in self.ships and self.type == "pers":
                if [x + 1, y + 1] in self.ships:
                    text = ship
                # self.log.debug(
                #     f"{x} {y} pos = {(x * horizontalspacer) + startcolumn},{(y * verticalspacer) + verticalspacer} text = [{text}]")
                Colors.position((x * horizontalspacer) + startcolumn + 2,
                                (y * verticalspacer) + verticalspacer + startrow + 2,
                                f"{Colors.FGYELLOW + Colors.BRIGHT + text}")
        print(Colors.RESETALL)


print(Colors.CLS)
compboard = Board(6, 5, "Computer", "comp")
compboard.showboard()
persboard = Board(6, 5, "Mark", "pers")
persboard.showboard()
print("\n\n\n")
print(f"{compboard.type}: {compboard.ships}")
print(f"{persboard.type}: {persboard.ships}")


# list = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
# ypos = 1
# print(Colors.CLS)
# while True:
#     for x in range(0, 11):
#         Colors.position(ypos, x, f"[{list[x]}]")
#     ypos += 10
#     time.sleep(1)
# y = x+1
# pos = lambda x, y: Cursor.POS(x, y)
# print('%s%s' % (pos(x, y), ' ' * 200), end=''+ str(x).replace("-", "")[0]) #f"{x}, {y}")


# x = input("")

def printCols():
    print("start")
    x = input("pause")
    print(Colors.FGRED + 'FGRED' + Colors.FGRESET)
    print(Colors.FGBLACK + 'FGBLACK' + Colors.FGRESET)
    print(Colors.FGGREEN + 'FGGREEN' + Colors.FGRESET)
    print(Colors.FGYELLOW + 'FGYELLOW' + Colors.FGRESET)
    print(Colors.FGBLUE + 'FGBLUE' + Colors.FGRESET)
    print(Colors.FGMAGENTA + 'FGMAGENTA' + Colors.FGRESET)
    print(Colors.FGCYAN + 'FGCYAN' + Colors.FGRESET)
    print(Colors.FGWHITE + 'FGWHITE' + Colors.FGRESET)

    print(Colors.BGRED + 'BGRED' + Colors.BGRESET)
    print(Colors.BGBLACK + 'BGBLACK' + Colors.BGRESET)
    print(Colors.BGGREEN + 'BGGREEN' + Colors.BGRESET)
    print(Colors.CLEARLINE)
    print(Colors.BGYELLOW + 'BGYELLOW' + Colors.BGRESET)
    print(Colors.BGBLUE + 'BGBLUE' + Colors.BGRESET)
    print(Colors.BGMAGENTA + 'BGMAGENTA' + Colors.BGRESET)
    print(Colors.BGCYAN + 'BGCYAN' + Colors.BGRESET)
    print(Colors.BGWHITE + 'BGWHITE' + Colors.BGRESET)
