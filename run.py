import logging
import random
import re
from ScreenControl import ScreenControl


def setup_logger(name, log_file, level=logging.DEBUG):
    # To setup as many loggers as you want
    handler = logging.FileHandler(log_file, "w", "utf-8")
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger


class Board:
    # ship = ScreenControl.bgmagenta + ScreenControl.bright + " " + ScreenControl.resetall
    # shellhit = ScreenControl.bgred + ScreenControl.bright + " " + ScreenControl.resetall
    # shellmiss = ScreenControl.bgyellow + " " + ScreenControl.resetall
    # empty = ScreenControl.bgwhite + ScreenControl.bright + " " + ScreenControl.resetall
    # columnlabeloffset = 18
    # gridstartcolumnoffset = 18
    # columnrowoffset = 16
    startrow = 5
    log = setup_logger("log", "bg.log", level=logging.DEBUG)

    def __init__(self, size, num_ships, name, start_x):
        self.size = size
        self.screencontrol = ScreenControl(5, start_x)
        self.hits = 0
        self.num_ships = num_ships
        self.ships = []
        self.moves = []
        self.columns = [str(i) for i in range(1, self.size + 1)]
        self.rows = [ScreenControl.num2let(i) for i in range(self.size)]

        while len(self.ships) < self.num_ships:
            a = random.choice(self.columns)
            b = random.choice(self.rows)
            if not [a, b] in self.ships:
                self.ships.append([a, b])
        self.name = name

    @staticmethod
    def pause(*text):
        ScreenControl.pos(1, 24, "", True)
        if len(text) == 0:
            text = "pause"
        input(text)

    def setupboard(self):
        self.screencontrol.printname(
            f"{ScreenControl.fgcyan + ScreenControl.bright + ScreenControl.underline_on}"
            + f"{self.name + ScreenControl.underline_off}"
        )

        # columnlabel
        self.screencontrol.printcolumnlabels(self.columns)

        # rowlabel
        self.screencontrol.printrowlabels(self.rows)

        # grid
        for x in self.columns:  # range(1, self.size + 1):
            for y in self.rows:  # range(1, self.size + 1):
                # Board.log.debug(f"setupboard {x}, {y}")
                self.screencontrol.showongrid(
                    [x, y],
                    f"{ScreenControl.fgyellow + ScreenControl.bright}{ScreenControl.empty}{ScreenControl.resetall}",
                )
                # Board.pause("278")
        print(ScreenControl.resetall)

    def showships(self):
        for coord in self.ships:
            self.screencontrol.showongrid(coord, ScreenControl.ship)
        print(ScreenControl.resetall)

    def updateboard(
        self,
    ):
        pass

    def makeaguess(self):
        validcoord = []
        if self.name.lower().startswith("comp"):
            return self.makerandomguess()
        else:
            while True:
                ScreenControl.clearline(21)
                self.screencontrol.makeaguess()
                playerinput = input("")
                validcoord = self.validateinput(playerinput)
                if validcoord:
                    break
        return validcoord

    def processguess(self, guess, otherboard):
        self.moves.append(guess)
        if guess in otherboard.ships:
            self.hits += 1
            self.screencontrol.printplayermessage(f"{self.name} hit a ship at {guess}")
            otherboard.screencontrol.showongrid(guess, ScreenControl.shellhit)
        else:
            self.screencontrol.printplayermessage(f"{self.name} missed at {guess}")
            otherboard.screencontrol.showongrid(guess, ScreenControl.shellmiss)
        self.screencontrol.updatemoves(len(self.moves))
        self.screencontrol.updatehits(self.hits)
        if self.hits == len(otherboard.ships):
            ScreenControl.clearline(24)
            msg = "lose." if self.name.lower() == "computer" else "win."
            ScreenControl.printendgamemessage(
                f"{self.name} has sunk all of {otherboard.name}'s ships. - you {msg}"
            )
            ScreenControl.printinfomessage("Play again?")
            ans = input("")
            if ans.lower().startswith("y"):
                main()
            else:
                quit()

    def makerandomguess(self):
        resultlist = []
        while True:
            x = random.choice(self.columns)
            y = random.choice(self.rows)
            resultlist = [x, y]
            if resultlist not in self.moves:
                break
        return resultlist

    def validateinput(self, playerinput):
        """
        checks that our input is 2 chars long with a number in range and a
        letter in range
        """
        resultlist = []
        playerinput = playerinput.strip().lower()
        try:
            if len(playerinput) != 2:
                raise ValueError(
                    f"Input is 2 digits, a letter and a "
                    + f"number - you gave '{playerinput}'"
                )
            else:
                searchletters = "".join([str(i) for i in self.columns])
                searchnumbers = "".join([str(i) for i in self.rows])
                letnum = re.search(
                    "^[" + searchletters + "][" + searchnumbers + "]$", playerinput
                )
                numlet = re.search(
                    "^[" + searchnumbers + "][" + searchletters + "]$", playerinput
                )
            if letnum is not None:
                resultlist = [playerinput[0], playerinput[1]]
            elif numlet is not None:
                resultlist = [playerinput[::-1][0], playerinput[::-1][1]]
            else:
                raise ValueError(
                    f"input out of range, " + f"'{playerinput}' is not on the board"
                )

            if resultlist in self.moves:
                raise ValueError(f"Coordinate {playerinput} has already been targeted")
            else:
                ScreenControl.clearinfomessage()
                return resultlist
        except ValueError as e:
            ScreenControl.printinfomessage(f"{e}, please try again")
        return False


def startgame(playername):
    size = 6
    num_ships = 5
    playerboard = Board(size, num_ships, playername, 0)
    compboard = Board(size, num_ships, "Computer", 40)
    ScreenControl.setupdisplay()
    playerboard.setupboard()
    playerboard.showships()
    compboard.setupboard()
    # compboard.showships()

    while True:
        validcoord = playerboard.makeaguess()
        playerboard.processguess(validcoord, compboard)
        validcoord = compboard.makeaguess()
        compboard.processguess(validcoord, playerboard)
        # compboard.makeaguess(playerboard)
        # if (compboard.gameover or playerboard.gameover):
        #     playagain = input("Play again").lower()
        #     if (playagain.startswith("y")):
        #         startgame(playername)
        #     else:
        #         print("Thanks for playing.")
        #         quit()


def main():
    # playername = input("Please enter your name\n")
    playername = "Mark"
    startgame(playername)


main()
