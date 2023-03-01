from colorama import just_fix_windows_console

just_fix_windows_console()


class ScreenControl:
    # foreground:
    fgblack = "\x1b[30m"
    fgred = "\x1b[31m"
    fggreen = "\x1b[32m"
    fgyellow = "\x1b[33m"
    fgblue = "\x1b[34m"
    fgmagenta = "\x1b[35m"
    fgcyan = "\x1b[36m"
    fgwhite = "\x1b[37m"
    fgreset = "\x1b[39m"

    # background
    bgblack = "\x1b[40m"
    bgred = "\x1b[41m"
    bggreen = "\x1b[42m"
    bgyellow = "\x1b[43m"
    bgblue = "\x1b[44m"
    bgmagenta = "\x1b[45m"
    bgcyan = "\x1b[46m"
    bgwhite = "\x1b[47m"
    bgreset = "\x1b[49m"

    underline_on = "\033[4m"
    underline_off = "\033[0m"

    resetall = "\x1b[0m"  # reset all (colors and brightness)
    bright = "\x1b[1m"  # bright
    dim = "\x1b[2m"  # dim (looks same as normal brightness)
    normal = "\x1b[22m"  # normal brightness

    gridgap_x = 2
    gridgap_y = 3

    screenwidth = 80

    start_x = 1
    labelstart_x = 4
    labeldata_x = 11
    columnlabel_x = 18
    gridstart_x = 16
    rowlabel_x = 16
    playermessagestart_x = 2

    boardblocktop_y = 4
    boardblockbottom_y = 20
    move_y = 4
    hit_y = 6
    columnlabel_y = 1
    guess_y = 21
    gridstart_y = 2
    infomessage_y = 23
    gamemessage_y = 22
    playermessage_y = 17

    framecol = bgblue
    ship = bgmagenta + bright + " " + resetall
    shellhit = bgred + bright + " " + resetall
    shellmiss = bgyellow + " " + resetall
    empty = bgwhite + bright + " " + resetall

    def __init__(self, start_y, start_x):
        self.start_y = start_y
        self.start_x = start_x

    def showongrid(self, coord, text):
        x = (
            (self.start_x + ScreenControl.gridstart_x)
            + (int(coord[0]) * ScreenControl.gridgap_y)
            - 1
        )
        y = (
            self.start_y
            + ScreenControl.gridstart_y
            + (int(ScreenControl.let2num(coord[1])) * ScreenControl.gridgap_x)
        )

        # ScreenControl.log.debug(f"showongrid pos [{x}, {y}]\n")
        ScreenControl.pos(x, y, text)
        ScreenControl.pos(x + 1, y, text)
        ScreenControl.pos(x + 2, y, text)
        ScreenControl.pos(x, y + 1, text)
        ScreenControl.pos(x + 1, y + 1, text)
        ScreenControl.pos(x + 2, y + 1, text)
        # ScreenControl.pos(x+2, y+1, text)
        # ScreenControl.pos(x+2, y+2, text)
        # ScreenControl.pos(x, y+1, text)
        # ScreenControl.pause()
        print(ScreenControl.resetall)

    # def showongrid(self, coord, text):
    #     ScreenControl.log.debug(f"showongrid self.start_x: {self.start_x}")
    #     ScreenControl.log.debug(f"showongrid ScreenControl.gridstart_x: {ScreenControl.gridstart_x}")
    #     ScreenControl.log.debug(f"showongrid int(coord[0]): {int(coord[0])}")
    #     ScreenControl.log.debug(f"showongrid ScreenControl.gridgap: {ScreenControl.gridgap_x}")
    #
    #     x = (self.start_x + ScreenControl.gridstart_x) + (
    #             int(coord[0]) * ScreenControl.gridgap_y) -1
    #     y = self.start_y + ScreenControl.gridstart_y + (
    #             int(ScreenControl.let2num(coord[1])) * ScreenControl.gridgap_x)
    #     # ScreenControl.log.debug(
    #     #     f"showongrid ScreenControl.gridstart_x: {ScreenControl.gridstart_x}")
    #     # ScreenControl.log.debug(
    #     #     f"showongrid ScreenControl.gridstart_y: {ScreenControl.gridstart_y}")
    #     # ScreenControl.log.debug(f"showongrid self.start_x: {self.start_x}")
    #     ScreenControl.log.debug(f"showongrid pos [{x}, {y}]\n")
    #     ScreenControl.pos(x, y, text)
    #     print(ScreenControl.resetall)

    def printcolumnlabels(self, columnlist):
        columnlabel = " ".join([str(i) + " " for i in columnlist])
        # ScreenControl.log.debug(
        #     f"printcolumnlabels {self.start_x + ScreenControl.columnlabel_x} {self.start_y + ScreenControl.columnlabel_y}")
        ScreenControl.pos(
            self.start_x + ScreenControl.columnlabel_x,
            self.start_y + ScreenControl.columnlabel_y,
            f"{ScreenControl.fgcyan + ScreenControl.bright}{columnlabel}",
        )

    def printrowlabels(self, rowlist):
        for i in range(len(rowlist)):
            # ScreenControl.log.debug(
            #     f"printrowlabels {self.start_x + ScreenControl.rowlabel_x} {self.start_y + ScreenControl.gridgap_x + (i * 2)}")
            ScreenControl.pos(
                self.start_x + ScreenControl.rowlabel_x,
                self.start_y + ScreenControl.gridgap_x + (i * 2),
                rowlist[i],
            )

    @staticmethod
    def clearscreen():
        print("\x1b[2J")  # clear the screen

    @staticmethod
    def clearline(y):
        ScreenControl.pos(1, y, " " * 80)

    # cursor positioning
    @staticmethod
    def pos(x, y, text, *nolinefeed):
        """
        # position cursor at x across, y down and print text
        """
        if nolinefeed:
            print(f"\x1b[{y};{x}H{text}", end="")
        else:
            print(f"\x1b[{y};{x}H{text}")

    @staticmethod
    def center(row, text):
        """
        pad text so that its central in window (80 cols)
        """
        xpos = int((80 - len(text)) / 2)
        ScreenControl.pos(xpos, row, text)

    @staticmethod
    def setupdisplay():
        ScreenControl.clearscreen()
        ScreenControl.pos(
            ScreenControl.start_x,
            ScreenControl.boardblocktop_y,
            f"{ScreenControl.framecol + ScreenControl.bright}"
            + " " * ScreenControl.screenwidth
            + ScreenControl.resetall,
        )
        ScreenControl.pos(
            ScreenControl.start_x,
            ScreenControl.boardblockbottom_y,
            f"{ScreenControl.framecol + ScreenControl.bright}"
            + " " * ScreenControl.screenwidth
            + ScreenControl.resetall,
        )
        for x in range(
            ScreenControl.boardblocktop_y + 1, ScreenControl.boardblockbottom_y
        ):
            ScreenControl.pos(
                int(ScreenControl.screenwidth / 2),
                x,
                f"{ScreenControl.framecol + ScreenControl.bright}  {ScreenControl.resetall}",
            )
            ScreenControl.pos(
                ScreenControl.start_x,
                x,
                f"{ScreenControl.framecol + ScreenControl.bright} {ScreenControl.resetall}",
            )
            ScreenControl.pos(
                ScreenControl.screenwidth,
                x,
                f"{ScreenControl.framecol + ScreenControl.bright} {ScreenControl.resetall}",
            )

        ScreenControl.center(
            1,
            f"{ScreenControl.fgwhite + ScreenControl.bright + ScreenControl.underline_on + 'Welcome to Battleships' + ScreenControl.underline_off}",
        )
        ScreenControl.center(
            2,
            "You have 5 ships, as does the computer, "
            + "Columns are 1 to 6, rows are a to f.",
        )
        ScreenControl.center(
            3, "You can pick a square " + "in either order - eg 'a5' or '3c'"
        )
        ScreenControl.pos(1, 24, f"????: {ScreenControl.empty}", True)
        ScreenControl.pos(21, 24, f"ship: {ScreenControl.ship}", True)
        ScreenControl.pos(41, 24, f"hit:  {ScreenControl.shellhit}", True)
        ScreenControl.pos(61, 24, f"miss: {ScreenControl.shellmiss}", True)

    # ship = ScreenControl.bgmagenta + ScreenControl.bright + " " + ScreenControl.resetall
    # shellhit = ScreenControl.bgred + ScreenControl.bright + " " + ScreenControl.resetall
    # shellmiss = ScreenControl.bgyellow + " " + ScreenControl.resetall
    # empty = ScreenControl.bgwhite + ScreenControl.bright + " " + ScreenControl.resetall

    def printname(self, text):
        ScreenControl.pos(
            self.start_x + ScreenControl.labelstart_x,
            self.start_y,
            f"{ScreenControl.fgcyan + ScreenControl.bright + ScreenControl.underline_on}"
            + f"{text + ScreenControl.underline_off}",
        )
        ScreenControl.pos(
            self.start_x + ScreenControl.labelstart_x,
            self.start_y + ScreenControl.move_y,
            "Moves:",
        )
        ScreenControl.pos(
            self.start_x + ScreenControl.labelstart_x,
            self.start_y + ScreenControl.hit_y,
            "Hits:",
        )

    def updatemoves(self, text):
        ScreenControl.pos(
            self.start_x + ScreenControl.labeldata_x,
            self.start_y + ScreenControl.move_y,
            text,
        )

    def updatehits(self, text):
        ScreenControl.pos(
            self.start_x + ScreenControl.labeldata_x,
            self.start_y + ScreenControl.hit_y,
            text,
        )

    @staticmethod
    def printinfomessage(text):
        ScreenControl.clearinfomessage()
        ScreenControl.pos(ScreenControl.start_x, ScreenControl.infomessage_y, text)

    @staticmethod
    def printendgamemessage(text, *nolinefeed):
        ScreenControl.pos(
            ScreenControl.start_x,
            ScreenControl.gamemessage_y,
            " " * ScreenControl.screenwidth,
        )
        if nolinefeed:
            ScreenControl.pos(
                ScreenControl.start_x, ScreenControl.gamemessage_y, text, True
            )
        else:
            ScreenControl.pos(ScreenControl.start_x, ScreenControl.gamemessage_y, text)

    @staticmethod
    def clearinfomessage():
        ScreenControl.pos(
            ScreenControl.start_x,
            ScreenControl.infomessage_y,
            " " * ScreenControl.screenwidth,
        )

    def printplayermessage(self, text):
        ScreenControl.pos(
            self.start_x + ScreenControl.playermessagestart_x,
            self.start_y + ScreenControl.playermessage_y,
            text,
            True,
        )

    def clearplayermessage(self):
        ScreenControl.pos(
            self.start_x + ScreenControl.playermessagestart_x,
            self.start_x + ScreenControl.playermessage_y,
            " " * int(ScreenControl.screenwidth / 2),
            True,
        )

    @staticmethod
    def makeaguess():
        ScreenControl.pos(
            ScreenControl.start_x, ScreenControl.guess_y, "Make a guess: ", True
        )

    @staticmethod
    def num2let(num):
        return chr(ord(str(num)) + 49)

    @staticmethod
    def let2num(let):
        return chr(ord(str(let)) - 49)
