from os import system, name
import random
from time import sleep
import PyInquirer as inquirer
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import webbrowser


class GameBoard:
    def __init__(self):
        self.clear()
        self.UserChar = 'X'
        self.round = 1
        self.turn = 'X'
        self.__Board = [
            ['1', '2', '3'],
            ['4', '5', '6'],
            ['7', '8', '9'],
        ]

        self.done = False

        self.map = {
            1: [0, 0],
            2: [0, 1],
            3: [0, 2],
            4: [1, 0],
            5: [1, 1],
            6: [1, 2],
            7: [2, 0],
            8: [2, 1],
            9: [2, 2],
        }

        self.printTitle()

        self.lastMove = ''

        difficultyQuestion = [
            {
                'type': 'list',
                'name': 'diffQ',
                'message': 'Choose your difficulty: ',
                'choices': ['Easy', 'Medium', 'Hard']

            }
        ]

        self.difficulty = inquirer.prompt(difficultyQuestion)['diffQ']

        print()
        print('Coin Flipping To Choose Who Start First ...')
        headsOrTails = ['Heads', 'Tails']
        coinFlipQuestion = [
            {
                'type': 'list',
                'name': 'coinFlip',
                'message': 'Choose heads or tails: ',
                'choices': headsOrTails
            }
        ]

        userCoin = inquirer.prompt(coinFlipQuestion)['coinFlip']

        flip = random.randint(0, 10)
        flip = 1 if flip >= 5 else 0

        winner = 'You' if userCoin == headsOrTails[flip] else 'Bot'

        self.UserChar = 'X' if winner == 'You' else 'O'
        self.botChar = 'X' if winner == 'Bot' else 'O'

        print()
        #         It's Tails. Bot won! Bot will start first.
        print('+--------------------------------------------+')
        print(f'|{" "*44}|')
        print(f'| It\'s {headsOrTails[flip]:^5}. {winner:^3} won! {winner:^3} will start first. |')
        print(f'| Your character is {self.UserChar:<1}.                       |')
        print(f'|{" "*44}|')
        print('+--------------------------------------------+')
        print()

        input('Press [Enter] to start the game')

    def rickRoll(self):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        # Get current volume
        currentVolumeDb = volume.GetMasterVolumeLevel()
        volume.SetMute(0, None)
        volume.SetMasterVolumeLevel(-0.0, None)

        webbrowser.open('https://www.youtube.com/watch?v=YddwkMJG1Jo')

    def printTitle(self):
        print('=============================================')
        print('=          The Impossible TicTacToe         =')
        print('=               Made by: Josh               =')
        print('=============================================')

        print('\n Let\' Start!')
        print()
        return

    def clear(self):
        if name == 'nt':
            system('cls')
        else:
            system('clear')

    def getCords(self, boxChosen: int):
        row = self.map[boxChosen][0]
        col = self.map[boxChosen][1]
        return [row, col]

    def ask(self):
        if (self.done):
            return

        self.turn = self.botChar

        while (True):
            boxChosen = input('Where do you want to play? ')

            if (boxChosen.isdigit()):
                boxChosen = int(boxChosen)
            else:
                continue

            if (boxChosen < 1 or boxChosen > 9):
                continue

            row, col = self.getCords(boxChosen)

            if (self.__Board[row][col] in 'XO'):
                print('Box Filled')
                continue

            self.__Board[row][col] = self.UserChar

            self.lastMove = boxChosen
            break

        self.draw()

    def getOutcomes(self, char: str, filter: bool = True):
        board = self.__Board

        char = self.UserChar if char == 'usr' else self.botChar
        enemychar = 'O' if char == 'X' else 'X'

        outcomes = []

        for rows in board:
            if (filter):
                if (enemychar not in set(rows)):
                    outcomes.append(set(rows))
            else:
                outcomes.append(set(rows))

        # Check Vertically
        for i in range(1, 4):
            vert = []

            for j in range(i, 10, 3):
                row, col = self.getCords(j)

                vert.append(board[row][col])

            if filter:
                if (enemychar not in set(vert)):
                    outcomes.append(set(vert))
            else:
                outcomes.append(set(vert))

        dr = [board[i][i] for i in range(3)]
        dl = [board[i][2 - i] for i in range(3)]

        if filter:
            if (enemychar not in set(dr)):
                outcomes.append(set(dr))

            if (enemychar not in set(dl)):
                outcomes.append(set(dl))
        else:
            outcomes.append(set(dr))
            outcomes.append(set(dl))

        # Sort the outcomes by the shortest length
        outcomes = sorted(outcomes, key=len)

        return outcomes

    def botInit(self):
        self.turn = self.UserChar

        if (self.difficulty == 'Easy'):
            return self.easyBot()

        if (self.difficulty == 'Medium'):
            return self.mediumBot()

        if (self.difficulty == 'Hard'):
            return self.hardBot()

        self.draw()

    def easyBot(self):
        if (self.done):
            return
        board = self.__Board

        print('Bot Choosing ...')

        # Sleep for a bit so user can see what's happening
        sleep(.5)

        while (True):
            randomBox = random.randint(1, 9)

            row, col = self.getCords(randomBox)

            if (board[row][col] in 'XO'):
                continue
            else:
                self.lastMove = board[row][col]
                self.__Board[row][col] = self.botChar

            break

        self.draw()

    def mediumBot(self):
        if (self.done):
            return
        if (self.round < 2):
            return self.easyBot()

        print('Bot Choosing ...')

        # Sleep for a bit so user can see what's happening
        sleep(.5)

        outcomes = self.getOutcomes('bot')

        if (len(outcomes) < 1):
            return self.easyBot()

        # Get the first outcome (which should be the best)
        decided = [x for x in outcomes[0] if x.isdigit()][0]

        self.lastMove = decided

        # get row and column
        row, col = self.getCords(int(decided))

        # Apply the bot's character into the box
        self.__Board[row][col] = self.botChar

        self.draw()

    def hardBot(self):
        if (self.done):
            return

        print('Bot Choosing ...')

        # Sleep for a bit so user can see what's happening
        sleep(.5)

        if (self.round == 1):
            row, col = self.getCords(5)
            if (self.UserChar not in self.__Board[row][col]):
                self.__Board[row][col] = self.botChar
                self.lastMove = '5'
                self.draw()
                return
            else:
                None

        def getBox(_outcomes):
            return [x for x in _outcomes[0] if x.isdigit()][0]

        usrOutcomes = self.getOutcomes('usr')
        botOutcomes = self.getOutcomes('bot')

        # If the bot has a guaranteed win take the win
        if (len(botOutcomes) > 0 and len(botOutcomes[0]) == 2):
            winBox = getBox(botOutcomes)

            row, col = self.getCords(int(winBox))

            self.__Board[row][col] = self.botChar
            self.lastMove = winBox

        # OTHERWISE

        # Check if the user have a guaranteed win
        # if they do, block it
        elif (len(usrOutcomes) > 0 and len(usrOutcomes[0]) == 2):
            blockingBox = getBox(usrOutcomes)

            row, col = self.getCords(int(blockingBox))

            self.__Board[row][col] = self.botChar
            self.lastMove = blockingBox

        # OTHERWISE

        # ? Code to check
        # # If the bot character doesn't exist in the board
        # elif (not any(self.botChar in sl for sl in self.__Board)):

        #     # If the  user character exist in the board
        #     if (any(self.UserChar in sl for sl in self.__Board)):

        #         # Get all the blocking outcomes
        #         # Get all the outcomes unfiltered
        #         # Then get all the outcomes that have the user character in it
        #         blockingOutcomes = [list(x) for x in self.getOutcomes(self.UserChar, False) if self.UserChar in x ]

        #         # From all the blocking outcomes, pick a random one
        #         randomBlock = blockingOutcomes[random.randint(0, len(blockingOutcomes) - 1)]

        #         # Get the largest number (so it will pick the farthest block from the user)
        #         biggestNum = max([ int(x) for x in randomBlock if x.isdigit() ])

        #         # Get rows and columns
        #         row, col = self.getCords(biggestNum)

        #         # Apply
        #         self.__Board[row][col] = self.botChar
        #         self.lastMove = biggestNum

        #     # OTHERWISE (The user didn't start)
        #     else:
        #         # Run the medium bot
        #         self.mediumBot()

        # # Just try to win
        else:
            self.mediumBot()

        self.draw()

    def move(self):
        if (not self.done):

            # If the user is the 'x'
            if (self.UserChar == 'X'):
                self.ask()
                self.botInit()
            else:
                self.botInit()
                self.ask()
            self.round += 1
        else:
            return

    def draw(self):
        self.clear()

        turn = 'Your' if self.turn == self.UserChar else 'Bot\'s'
        print(f'    It\'s {turn} turn ')
        print('=======================')
        print()

        for idx, Row in enumerate(self.__Board):

            # Top Part
            print(f'{" ":^7}|{" ":^7}|{" ":^7}', end="")
            print()

            # Second Part | This is where the Character lives
            print(f'{Row[0]:^7}|{Row[1]:^7}|{Row[2]:^7}', end="")
            print()

            # Bottom Part
            print(f'{" ":^7}|{" ":^7}|{" ":^7}', end="")
            print()

            # If it's not the last line, print the separator
            if (idx < 2):
                print('-------+-------+-------')

        if (self.lastMove != ''):
            lastOne = "X" if self.turn == "O" else "O"
            print('+-------------------+')
            print(f'|{" "*19}|')
            print(f'|  {"You" if lastOne == self.UserChar else "Bot":^1} chose box {self.lastMove:^1}  |')
            print(f'|{" "*19}|')
            print('+-------------------+')
            print()

        if (self.round > 2):
            self.check()

    def won(self, charWon):
        print(f'{charWon} WON!')

        if charWon == self.botChar:
            self.rickRoll()


        self.done = True

    def checkLine(self, line):
        # Put it in a set which removes duplicates
        lineSet = set(line)

        if (len(lineSet) > 1):
            return None

        winning = 'X' if 'X' in lineSet else 'O'

        self.won(winning)

    def check(self):
        # Copy the current board array
        board = self.__Board

        # Check each row if there is a winner
        for rows in board:
            self.checkLine(rows)

        for i in range(1, 4):
            vert = []

            for j in range(i, 10, 3):
                row, col = self.getCords(j)
                vert.append(board[row][col])

            self.checkLine(vert)

        # These 2 lines will check diagonally
        self.checkLine([board[i][i] for i in range(3)])
        self.checkLine([board[i][2 - i] for i in range(3)])

        tie = True

        # Check for ties
        for r in board:
            for c in r:
                if c.isdigit():
                    tie = False

        if tie:
            print('Tie')
            self.done = True
            self.rickRoll()
            return
