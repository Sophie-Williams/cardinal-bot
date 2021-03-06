#! python3
"""Cardinal Bot
Soreine soreine.plume@gmail.com

A bot program to automatically play the Cardinal flash game at
http://www.newgrounds.com/portal/view/634256

"""

import pyautogui
import time
import os
import logging
import sys
import random
import copy

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s.%(msecs)03d: %(message)s', datefmt='%H:%M:%S')
#logging.disable(logging.DEBUG) # uncomment to block debug log messages

# Global variables
GAME_WIDTH = 550
GAME_HEIGHT = 550 # the game screen is always 550 x 550
SQUARE_COLOR = (249, 8, 42)
WALL_COLOR = (176, 1, 26)

# various coordinates of objects in the game
GAME_REGION = () # (left, top, width, height) values coordinates of the entire game window
PLAY_COORDS = None # Coordinates of the play button
SQUARE_LOCATION = (GAME_WIDTH/2, GAME_HEIGHT/2)
RIGHT_WALL = (460, 275)
LEFT_WALL = (88, 270)
UP_WALL = (270, 88)
DOWN_WALL = (275, 460)

def main():
    """Runs the entire program. The Cardinal game must be visible on the
    screen and the PLAY button visible."""
    logging.debug('Program Started. Press Ctrl-C to abort at any time.')
    logging.debug('To interrupt mouse movement, move mouse to upper left corner.')
    getGameRegion()
    navigateGameWindow()
    startPlaying()


def imPath(filename):
    """A shortcut for joining the 'images/'' file path, since it is used
    so often. Returns the filename with 'images/' prepended."""
    return os.path.join('../images', filename)


def getGameRegion():
    """Obtains the region that the Cardinal game occupies on the screen
    and assigns it to GAME_REGION. The game must be at the start screen
    (where the PLAY button is visible)."""
    global GAME_REGION, PLAY_COORDS, GAME_CENTER

    # identify the top-left corner
    logging.debug('Finding game region...')
    region = pyautogui.locateOnScreen(imPath('top-left-corner.png'))
    if region is None:
        raise Exception('Could not find game on screen. Is the game visible?')

    # calculate the region of the entire game
    GAME_REGION = (region[0], region[1], GAME_WIDTH, GAME_HEIGHT)
    logging.debug('Game region found: %s' % (GAME_REGION,))

    # Calculate the position of the PLAY button
    PLAY_COORDS = (GAME_REGION[0] + 275, GAME_REGION[1] + 522)

    # Calculate the center of the screen
    GAME_CENTER = (GAME_REGION[0] + GAME_REGION[2]/2, GAME_REGION[1] + GAME_REGION[3]/2)

def navigateGameWindow():
    """Get the initial focus on the game window and mute the game, getting
    ready to play."""
    # Get focus on the game by clicking the center of the game region
    pyautogui.click(GAME_CENTER[0], GAME_CENTER[1], duration=1)

    # Mute game (it helps too because it disables some in-game effects :-p)
    pyautogui.press('m')


def newGame():
    """Start a new game by clicking on the PLAY button."""
    # click on Play
    pyautogui.click(PLAY_COORDS, duration=0.25)
    logging.debug('New game...')

def startPlaying():
    """The main game playing function. This function handles all aspects
    of game play, including starting a new game, playing and detecting
    game overs."""

    # Start a new game
    newGame()
    
    while True:
        # Wait until the square is at the center of the screen
        for i in range(0, 3):
            img = pyautogui.screenshot(region=GAME_REGION)
            if  img.getpixel(SQUARE_LOCATION) == SQUARE_COLOR:
                break
            elif i == 2:
                # After three attempts we can safely assume we lost.
                logging.debug('OK I lost... PLAY AGAIN :D')
                pyautogui.press('space');
                break
            else:
                logging.debug('Waiting for square...')
        
        logging.debug('Must move!')

        # The direction to go
        direction = None
        logging.debug('Checking walls')
        # Check for an opening in on of the 4 directions
        if not img.getpixel(LEFT_WALL) == WALL_COLOR:
            direction = 'left'
        elif not img.getpixel(RIGHT_WALL) == WALL_COLOR:
            direction = 'right'
        elif not img.getpixel(UP_WALL) == WALL_COLOR:
            direction = 'up'
        elif not img.getpixel(DOWN_WALL) == WALL_COLOR:
            direction = 'down'
            
        if direction is not None:
            pyautogui.press(direction)
            logging.debug('Moving ' + direction + '!')
            # Wait a moment for the square to move. This takes the
            # time to take a screenshot into account, and the time the
            # square leave the screen too.
            time.sleep(0.29) # As the screenshot time varies, this is a practical upper bound.
        else:
            logging.debug('No opening found...')


if __name__ == '__main__':
    main()
