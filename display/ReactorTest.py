import pygame

# initialize game engine
pygame.init()
# set screen width/height and caption
size = [640, 480]
screen = pygame.display.set_mode(size)
pygame.display.set_caption('My Game')
# initialize clock. used later in the loop.
clock = pygame.time.Clock()




def incrementState(reactor):
    reactor.react()
    reactor.removeBadBonds()
    reactor.move()


def drawState()


# Loop until the user clicks close button
done = False
while done == False:
    # write event handlers here
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    # write game logic here

    # clear the screen before drawing
    incrementState()
    drawState()
    # write draw code here

    pygame.display.update()
    # run at 20 fps
    clock.tick(20)

# close the window and quit
pygame.quit()