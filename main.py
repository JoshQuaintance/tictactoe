from GameBoard import GameBoard
import PyInquirer as inquirer
from time import sleep


def main():

    while(True):

        Game = GameBoard()

        while (not Game.done):
            Game.clear()
            Game.draw()

            if (not Game.done):
                Game.move()
            Game.draw()

        playAgain = 'y'

        while (playAgain == 'y'):
            questions = [
                {
                    'type': 'input',
                    'name': 'playagain',
                    'message': 'Do you want to play again (Press [y] to play again | Press [n] for NO)?'
                }
            ]

            playAgain = inquirer.prompt(questions)['playagain']

            if playAgain.lower() not in 'ny':
                continue

            playAgain = True if playAgain == 'y' else False

            if playAgain:
                print('Running Again')
                sleep(.5)
            else:
                print('Exitting')
                exit()


if __name__ == '__main__':
    main()
