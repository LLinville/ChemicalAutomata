import pygame
import colorsys

# initialize game engine
from reactor.Reactor import Reactor

pygame.init()
# set screen width/height and caption
size = [640, 480]
screen = pygame.display.set_mode(size)
pygame.display.set_caption('My Game')
# initialize clock. used later in the loop.
clock = pygame.time.Clock()

atomWidth = 10
atomBorder = 1
numElements = 3
numStates = 3

reactor = Reactor((10, 10))

def incrementState(reactor):
    reactor.react()
    reactor.removeBadBonds()
    reactor.move()


def drawState():
    state = reactor.getCells()
    for row in state:
        for cell in row:
            if cell is not None:

def colorWheel(numberOfColors, saturation):
    hues = [1.0 * n / numberOfColors for n in range(numberOfColors)]
    rgb = [colorsys.hsv_to_rgb(hue, saturation, 1) for hue in hues]

stateColors = [[colorWheel(numElements, 1.0 * state / numStates) for state in range(numStates)] for element in range(numElements)]


# Loop until the user clicks close button
done = False
while done == False:
    # write event handlers here
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    # write game logic here

    # clear the screen before drawing
    incrementState(reactor)
    drawState()
    # write draw code here

    pygame.display.update()
    # run at 20 fps
    clock.tick(20)

# close the window and quit
pygame.quit()