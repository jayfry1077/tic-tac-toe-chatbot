import sys
import os
import codecs
import json

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))


from TTT_Settings_Module import MySettings

settings_file = os.path.join(os.path.dirname(__file__), "tic_tac_toe_settings.json")
game_state = os.path.join(os.path.dirname(__file__), "game_state.json")

ScriptName = "Tic Tac Toe"
Website = "YOUR_TWITCH_URL_HERE"
Description = "Starts a game of Tic Tac Toe"
Creator = "YOUR_CREATOR_NAME_HERE"
Version = "1.0.0.0"


class GameState(object):
    """ Load in saved settings file if available else set default values. """
    def __init__(self, CurrentBidFile = None):
        try:
            with codecs.open(CurrentBidFile, encoding='utf-8-sig', mode='r') as f:
                self.__dict__ = json.load(f, encoding='utf-8-sig')
        except:
            self.BOARD = ["U","U","U","U","U","U","U","U","U","U"]
            self.PLAYER_1 = True
            self.PLAYER_2 = False

    def Save(self, currentGameFile):
        """ Save settings contained within to .json and .js settings files. """
        try:
            with codecs.open(currentGameFile, encoding="utf-8-sig", mode="w+") as f:
                json.dump(self.__dict__, f, encoding="utf-8")
            with codecs.open(currentGameFile.replace("json", "js"), encoding="utf-8-sig", mode="w+") as f:
                f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8')))
        except:
            Parent.Log(ScriptName, "Failed to save game file.")
        return

    def Reset(self, currentGameFile):
        """ Reset settings files. """
        try:
            self.BOARD = ["U","U","U","U","U","U","U","U","U","U"]
            self.PLAYER_1 = True
            self.PLAYER_2 = False
            with codecs.open(currentGameFile, encoding="utf-8-sig", mode="w+") as f:
                json.dump(self.__dict__, f, encoding="utf-8")
            with codecs.open(currentGameFile.replace("json", "js"), encoding="utf-8-sig", mode="w+") as f:
                f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8')))
        except:
            Parent.Log(ScriptName, "Failed to save game file.")
        return

def Init():
    global my_settings
    global gameState
    global PLAYER_1_MARK
    global PLAYER_2_MARK

    PLAYER_1_MARK = 'X'
    PLAYER_2_MARK = 'O'

    gameState = GameState(game_state)

    my_settings = MySettings(settings_file)

    return

def Execute(data):
    if data.IsChatMessage() is True and data.GetParam(0).lower() == my_settings.Command.lower():


        # If they didn't pass a move, we just return.
        if data.GetParamCount() < 2:
            SendMessage(data, 'You need to start the game by making a move. Example: !TicTacToe 1')
            return

        # Cast user input to int 
        try:
            user_input = int(data.GetParam(1))

            # If they enter a number to large or to small
            if user_input < 1 or user_input > 9:
                SendMessage(data, '{} is out of range. Valid options are 1-9'.format(user_input))

                return

        except:
            Parent.Log(ScriptName, 'Invalid game option. {}'.format(data.GetParam(1)))
            SendMessage(data, '{} is not a valid integer.'.format(data.GetParam(1)))
            return

        # Set the marker and switch which player is active
        if gameState.PLAYER_1:
            gameState.BOARD[user_input] = PLAYER_1_MARK
            gameState.PLAYER_1 = False
            gameState.PLAYER_2 = True
        elif gameState.PLAYER_2:
            gameState.BOARD[user_input] = PLAYER_2_MARK
            gameState.PLAYER_1 = True
            gameState.PLAYER_2 = False

        # Print the board out to the chat
        SendMessage(data, " {} | {} | {} ".format(gameState.BOARD[1],gameState.BOARD[2],gameState.BOARD[3]))
        SendMessage(data, " {} | {} | {} ".format(gameState.BOARD[4],gameState.BOARD[5],gameState.BOARD[6]))
        SendMessage(data, " {} | {} | {} ".format(gameState.BOARD[7],gameState.BOARD[8],gameState.BOARD[9]))

        # Check if there isa winner or draw
        winner = determineWinner(gameState.BOARD)

        if winner != 'Running':
            SendMessage(data, winner)
            gameState.Reset(game_state)
        else:
            gameState.Save(game_state)
        
        return


    return

def Tick():
    return


def SendMessage(data, msg):
    if data.IsFromTwitch():
        Parent.SendStreamMessage(msg)

        return


def determineWinner(gameboard):
    # Horizontal
    if gameboard[1] != 'U' and gameboard[1] == gameboard[2] and gameboard[1] == gameboard[3]:
        return winningPlayer(gameboard[1])
    elif gameboard[4] != 'U' and gameboard[4] == gameboard[5] and gameboard[4] == gameboard[6]:
        return winningPlayer(gameboard[4])
    elif gameboard[7] != 'U' and gameboard[7] == gameboard[8] and gameboard[7] == gameboard[9]:
        return winningPlayer(gameboard[7])
    # Vertical
    elif gameboard[1] != 'U' and gameboard[1] == gameboard[4] and gameboard[1] == gameboard[7]:
        return winningPlayer(gameboard[1])
    elif gameboard[2] != 'U' and gameboard[2] == gameboard[5] and gameboard[2] == gameboard[8]:
        return winningPlayer(gameboard[2])
    elif gameboard[3] != 'U' and gameboard[3] == gameboard[6] and gameboard[3] == gameboard[9]:
        return winningPlayer(gameboard[3])
    # Diagional
    elif gameboard[1] != 'U' and gameboard[1] == gameboard[5] and gameboard[1] == gameboard[9]:
        return winningPlayer(gameboard[1])
    elif gameboard[3] != 'U' and gameboard[3] == gameboard[5] and gameboard[3] == gameboard[7]:
        return winningPlayer(gameboard[3])
    # Draw
    # If there are no more U's in the gameboard array, then all spaces are filled.
    # Since all spaces are filled, and none of the above were truthy, then its a draw
    elif 'U' not in gameboard:
        return 'Game is a Draw!'
    else:
        # If nothing above is true, then the game is still running.
        'Running'

def winningPlayer(marker):
    # If is not X then in O
    if marker == 'X':
        return 'Player 1 Wins'
    else:
        return 'Player 2 Wins'
