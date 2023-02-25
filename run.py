import logging
import random
import re

from colorama import just_fix_windows_console

just_fix_windows_console()


def setup_logger(name, log_file, level=logging.DEBUG):
    # To setup as many loggers as you want
    handler = logging.FileHandler(log_file, 'w', 'utf-8')
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger


# 1. input validation
#
# 2. Board class
#     self.guesses = []
#     self.ships = []
#     sieze
#     name
#     type
#     num ships

class Cols:
    messagerow = 22
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
    # CLEARLINE = '\x1b[1K'  # clear the line
    # CLEARLINE = "\33[2K\r"
    # CLEARLINE = "\x1b2dK"

    @staticmethod
    def clearline(y):
        Cols.pos(1, y, " " * 80)

    # cursor positioning
    @staticmethod
    def pos(x, y, text, *nolinefeed):
        """
        # position cursor at x across, y down and print text
        """
        if nolinefeed:
            print(f"\x1b[{y};{x}H{text}", end='')
        else:
            print(f"\x1b[{y};{x}H{text}")

    @staticmethod
    def centerpad(text):
        """
        pad text so that its central in window (80 cols)
        """
        padlen = int((80 - len(text)) / 2)
        pad = " " * padlen
        return pad + text

    @staticmethod
    def printmessage(text):
        Cols.pos(1, Cols.messagerow, text)

    @staticmethod
    def clearmessage():
        Cols.pos(1, Cols.messagerow, " " * 80)


class Board:
    ship = "#"
    framecol = Cols.BGRED
    emptyspace = "-"
    shellhit = Cols.BGRED + Cols.BRIGHT + "X" + Cols.RESETALL
    shellmiss = "X"  # Cols.BGYELLOW + "X" + Cols.RESETALL
    startrow = 5
    horizontalspacer = 3
    verticalspacer = 2
    log = setup_logger("bs", "bs.log", level=logging.DEBUG)

    def __init__(self, size, num_ships, name, startcolumn):
        self.size = size
        # self.type = type
        self.startcolumn = startcolumn + 15
        # self.start = True
        self.board = [[Board.emptyspace for x in range(size)] for y in
                      range(size)]
        self.num_ships = num_ships
        self.ships = []
        self.moves = []
        self.columns = [str(i) for i in range(1, self.size + 1)]
        # Board.log.debug(f"{type} : self.columns {self.columns}")
        self.rows = [Board.num2let(i) for i in range(self.size)]
        # Board.log.debug(f"{type} : self.rows {self.rows}")
        # print(self.columns)
        # print(self.rows)

        while len(self.ships) < self.num_ships:
            a = random.choice(self.columns)
            b = random.choice(self.rows)
            if not [a, b] in self.ships:
                self.ships.append([a, b])
        # print(f"{type} : self.ships {self.ships}")
        # Board.pause()
        self.name = name

    @staticmethod
    def pause():
        input("pause")

    @staticmethod
    def num2let(num):
        return chr(ord(str(num)) + 49)

    @staticmethod
    def let2num(let):
        return chr(ord(str(let)) - 49)

    def setupboard(self):
        Cols.pos(1, 4,
                 f"{Board.framecol + Cols.BRIGHT}" + " " * 80 + Cols.RESETALL)
        Cols.pos(1, 20,
                 f"{Board.framecol + Cols.BRIGHT}" + " " * 80 + Cols.RESETALL)
        for x in range(5, (self.size * 2) + 8):
            Cols.pos(41, x,
                     f"{Board.framecol + Cols.BRIGHT} {Cols.RESETALL}")
            Cols.pos(1, x,
                     f"{Board.framecol + Cols.BRIGHT} {Cols.RESETALL}")
            Cols.pos(80, x,
                     f"{Board.framecol + Cols.BRIGHT} {Cols.RESETALL}")
        if self.name.lower().startswith("comp"):
            Board.printinstructions()
        columnlabel = " ".join([str(i) + " " for i in self.columns])
        Cols.pos(self.startcolumn + 2, Board.startrow + 1,
                 f"{Cols.FGCYAN + Cols.BRIGHT}{columnlabel}")
        Cols.pos(self.startcolumn - 11, Board.startrow,
                 f"{Cols.FGCYAN + Cols.BRIGHT + Cols.UNDERLINE_ON}" +
                 f"{self.name + Cols.UNDERLINE_OFF}")
        for x in range(self.size):
            Cols.pos(self.startcolumn, (
                    x * Board.verticalspacer) + Board.verticalspacer + Board.startrow,
                     f"{Cols.FGCYAN + Cols.BRIGHT + self.rows[x]}")
        yint = 0
        xint = 0
        # Board.log.debug(f"\n{self.name} self.ships = {self.ships}")
        for x in self.columns:  # range(1, self.size + 1):
            for y in self.rows:  # range(1, self.size + 1):
                yint = int(Board.let2num(y))
                xint = int(x) - 1
                #     Board.log.debug(
                #         f"{self.name}: found  {[x, self.rows[yint]]} in {self.ships} Found : {[x, self.rows[yint]] in self.ships}")
                #     Board.log.debug(
                #         f"{self.name} [{x}, {self.rows[int(Board.let2num(y))]}] putting a ship at [{x},{y}]")
                #
                # Board.log.debug(
                #     f"x = {x} y = {y} xint {xint} yint {yint}")
                Cols.pos(
                    (xint * Board.horizontalspacer) + self.startcolumn + 2,
                    ((yint + 1) * Board.verticalspacer) + Board.startrow,
                    f"{Cols.FGYELLOW + Cols.BRIGHT + self.board[xint][yint]}")
        print(Cols.RESETALL)

    def updateboard(self):
        pass
        # yint = 0
        # xint = 0
        #
        # # Board.log.debug(f"\n{self.name} self.ships = {self.ships}")
        # for x in self.columns:  # range(1, self.size + 1):
        #     for y in self.rows:  # range(1, self.size + 1):
        #         yint = int(Board.let2num(y))
        #         xint = int(x) - 1
        #         #     Board.log.debug(
        #         #         f"{self.name}: found  {[x, self.rows[yint]]} in {self.ships} Found : {[x, self.rows[yint]] in self.ships}")
        #         #     Board.log.debug(
        #         #         f"{self.name} [{x}, {self.rows[int(Board.let2num(y))]}] putting a ship at [{x},{y}]")
        #         #
        #         # Board.log.debug(
        #         #     f"x = {x} y = {y} xint {xint} yint {yint}")
        #         Cols.pos(
        #             (xint * Board.horizontalspacer) + self.startcolumn + 2,
        #             ((yint + 1) * Board.verticalspacer) + Board.startrow,
        #             f"{Cols.FGYELLOW + Cols.BRIGHT + self.board[xint][yint]}")
        # print(Cols.RESETALL)

    def makeaguess(self):
        i = 0
        validcoord = ""
        if self.name.lower().startswith("comp"):
            self.makerandomguess()
        else:
            while True:
                Cols.clearline(21)
                Cols.pos(1, 21, "Make a guess: ", True)
                Cols.pos(1, 1, "1234567890" *8)
                for i in range(1,24):
                    Cols.pos(1, i, str(i))
                playerinput = input("")
                Cols.clearmessage()
                validcoord = self.validateinput(playerinput)
                # Cols.pos(1, 23, f"{i}. validcoord = {validcoord}")
                i += 1
                if isinstance(validcoord, str):
                    break
        return validcoord;

    def processguess(self, guess):
        listguess = [guess[0], guess[1]]
        xint = int(guess[0]) - 1
        yint = int(Board.let2num(guess[1]))
        Board.log.debug(
            f"{self.name}:processguess({guess}) self.ships = {self.ships} : {listguess}")
        for i in range(0, len(self.board)):
            Board.log.debug(f"{i} : {self.board[i]}")
        if listguess in self.ships:
            self.moves.append(listguess)
            Board.log.debug(
                f"{self.name}:processguess() self.board[{xint}][{yint}]")
            # Board.log.debug(
            #     f"{self.name}:processguess() self.board[{xint}][{yint}] = {self.board[xint][yint]}")

            print("THIS BIT IS WRONG")
            print("THIS BIT IS WRONG")
            print("THIS BIT IS WRONG")
            print("THIS BIT IS WRONG")
            print("THIS BIT IS WRONG")

            if self.board[xint][yint] == Board.ship:
                Board.log.debug(
                    f"HIT!! self.board[{xint}][{yint}] = {self.board[xint][yint]}")
                self.board[xint][yint] = Board.shellhit
        else:
            Board.log.debug(
                f"MISS!! self.board[{xint}][{yint}] = {self.board[xint][yint]}")
            self.board[xint][yint] = Board.shellmiss
        Board.log.debug(f" moves : {self.moves}")

        self.updateboard()

    def makerandomguess(self):
        pass

    @staticmethod
    def clearMessage():
        Cols.clearline(22)

    def validateinput(self, playerinput):
        """
        checks that our input is 2 chars long with a number in range and a
        letter in range
        """
        playerinput = playerinput.strip().lower()
        try:
            if len(playerinput) != 2:
                raise ValueError(
                    f"Input is 2 digits, a letter and a " +
                    f"number - you gave '{playerinput}'"
                )
            else:
                searchletters = "".join([str(i) for i in self.columns])
                searchnumbers = "".join([str(i) for i in self.rows])
                letnum = re.search(
                    "^[" + searchletters + "][" + searchnumbers + "]$",
                    playerinput)
                numlet = re.search(
                    "^[" + searchnumbers + "][" + searchletters + "]$",
                    playerinput)
            if letnum is not None:
                # Board.log.debug(
                #     f"{self.name}:validateinput({playerinput}) returning: {playerinput}")
                return playerinput
            elif numlet is not None:
                # Board.log.debug(
                #     f"{self.name}:validateinput({playerinput}) returning: {playerinput[::-1]}")
                return playerinput[::-1]
            else:
                raise ValueError(f"input out of range, " +
                                 f"'{playerinput}' is not on the board")

        except ValueError as e:
            Cols.printmessage(f"{e}, please try again")
        return False

    @staticmethod
    def printinstructions():

        Cols.pos(1, 1,
                 f"{Cols.FGWHITE + Cols.BRIGHT + Cols.centerpad(Cols.UNDERLINE_ON + 'Welcome to Battleships' + Cols.UNDERLINE_OFF)}")
        Cols.pos(1, 2,
                 Cols.centerpad(
                     "You have 5 ships, as does the computer, " +
                     "Columns are 1 to 6, rows are a to f."))
        Cols.pos(1, 3,
                 Cols.centerpad("You can pick a square " +
                                "in either order - eg 'a5' or '3c'"))


def startgame(playername):
    size = 6
    num_ships = 5
    playerboard = Board(size, num_ships, playername, 0)
    compboard = Board(size, num_ships, "Computer", 40)
    print(Cols.CLS)
    while True:
        compboard.setupboard()
        playerboard.setupboard()
        Cols.pos(1, 21, "pause", True)
        compboard.updateboard()
        playerboard.updateboard()
        validcoord = playerboard.makeaguess()
        compboard.processguess(validcoord)
        # compboard.makeaguess(playerboard)
        # if (compboard.gameover or playerboard.gameover):
        #     playagain = input("Play again").lower()
        #     if (playagain.startswith("y")):
        #         startgame(playername)
        #     else:
        #         print("Thanks for playing.")
        #         quit()


print(Cols.CLS)
# playername = input("Please enter your name\n")
playername = "Mark"
startgame(playername)
