# Hugo's part: top-down shooter game

# importing necessary modules
import sys, random, pygame
# putting functions in another file for readability
from Hugo_Library import random_colour,random_health_drop,random_location,calc_velocity,print_text,MySprite,Point,bullet
from pygame.locals import *

# initialization
pygame.init()
# set resolution and title
screen = pygame.display.set_mode((750, 750))
pygame.display.set_caption("Top-down Shooter Game | 顶视角射击游戏")
# define two types of font
font = pygame.font.Font(None, 36)
font2 = pygame.font.Font(None, 100)
# define a timer for frame settings
timer = pygame.time.Clock()

# create sprite(pygame actor) groups
P1_group = pygame.sprite.Group()
P2_group = pygame.sprite.Group()
health_group = pygame.sprite.Group()
# a list to hold all the bullets on the screen
Bullet = []

# create player1's sprite
P1 = MySprite()
P1.load("Hugo_assets/P1.png", 96, 96, 8)
# randomize spawn location and direction facing
P1.position = random_location()
P1.direction = random.randint(1,4)
# add it to sprite group
P1_group.add(P1)

# create player2's sprite
P2 = MySprite()
P2.load("Hugo_assets/P2.png", 96, 96, 8)
# randomize spawn location and direction facing
P2.position = random_location()
P2.direction = random.randint(1,4)
# add it to sprite group
P2_group.add(P2)

# create heath sprite
health = MySprite()
health.load("Hugo_assets/health.png", 32, 32, 1)
# randomize spawn location and direction facing
health.position = random_location()
# add it to sprite group
health_group.add(health)

# initialize all necessary variables
P1_win = False
P2_win = False
P1_moving = False
P2_moving = False
P1_health = 100
P2_health = 100
player_velocity = 3
boundary_x = (0, 660)
boundary_y = (30, 660)
# if the answer is correct and bullet is loaded
P1_power = False
P2_power = False

# main program
while True:
    # set frame rate to 30 fps
    timer.tick(30)
    ticks = pygame.time.get_ticks()

    # fetch the current event
    for event in pygame.event.get():
        if event.type == QUIT: sys.exit()
    # fetch what key's being pressed
    keys = pygame.key.get_pressed()

    # allow player1 to move
    # direction: 0 for north, 2 for east, 4 for south, 6 for west
    if keys[K_ESCAPE]:
        sys.exit()
    elif keys[K_w]:
        P1.direction = 0
        P1_moving = True
    elif keys[K_d]:
        P1.direction = 2
        P1_moving = True
    elif keys[K_s]:
        P1.direction = 4
        P1_moving = True
    elif keys[K_a]:
        P1.direction = 6
        P1_moving = True
    else:
        P1_moving = False

    # allow player2 to move
    # direction: 0 for north, 2 for east, 4 for south, 6 for west
    if keys[K_ESCAPE]:
        sys.exit()
    elif keys[K_UP]:
        P2.direction = 0
        P2_moving = True
    elif keys[K_RIGHT]:
        P2.direction = 2
        P2_moving = True
    elif keys[K_DOWN]:
        P2.direction = 4
        P2_moving = True
    elif keys[K_LEFT]:
        P2.direction = 6
        P2_moving = True
    else:
        P2_moving = False

    # only allow the players to move when the game is not over
    if not (P1_win or P2_win):
        # set animation frames based on player1's direction
        P1.first_frame = P1.direction * P1.columns
        P1.last_frame = P1.first_frame + P1.columns - 1
        if P1.frame < P1.first_frame:
            P1.frame = P1.first_frame
        # stop animating when P1 is not pressing a key
        if not P1_moving:
            P1.frame = P1.first_frame = P1.last_frame
        else:
            # move P1 in direction
            P1.velocity = calc_velocity(P1.direction, player_velocity)

        # set animation frames based on player2's direction
        P2.first_frame = P2.direction * P2.columns
        P2.last_frame = P2.first_frame + P2.columns - 1
        if P2.frame < P2.first_frame:
            P2.frame = P2.first_frame
        # stop animating when P2 is not pressing a key
        if not P2_moving:
            P2.frame = P2.first_frame = P2.last_frame
        else:
            # move P2 in direction
            P2.velocity = calc_velocity(P2.direction, player_velocity)
            
        # update players' sprites
        P1_group.update(ticks, 50)
        P2_group.update(ticks, 50)

        # move the player based on velocity and direction facing
        # player1
        if P1_moving:
            P1.X += P1.velocity.x
            P1.Y += P1.velocity.y
            # set boundary so that player cannot leave the screen
            if P1.X < boundary_x[0]:
                P1.X = boundary_x[0]
            elif P1.X > boundary_x[1]:
                P1.X = boundary_x[1]
            if P1.Y < boundary_y[0]:
                P1.Y = boundary_y[0]
            elif P1.Y > boundary_y[1]:
                P1.Y = boundary_y[1]
        # player2
        if P2_moving:
            P2.X += P2.velocity.x
            P2.Y += P2.velocity.y
            # set boundary so that player cannot leave the screen
            if P2.X < boundary_x[0]:
                P2.X = boundary_x[0]
            elif P2.X > boundary_x[1]:
                P2.X = boundary_x[1]
            if P2.Y < boundary_y[0]:
                P2.Y = boundary_y[0]
            elif P2.Y > boundary_y[1]:
                P2.Y = boundary_y[1]

        # update the health drop
        health_group.update(ticks, 50)

        # check for collision with health
        if pygame.sprite.collide_rect_ratio(0.5)(P1, health):
            # gain 10 health point
            P1_health += 10
            # prevent health from exceeding 100
            if P1_health > 100: P1_health = 100
            # spawn new health at random location
            health.X, health.Y = random_location()

        if pygame.sprite.collide_rect_ratio(0.5)(P2, health):
            # gain 10 health point
            P2_health += 10
            # prevent health from exceeding 100
            if P2_health > 100: P2_health = 100
            # spawn new health at random location
            health.X, health.Y = random_location()

    # check status of players to end the game
    if P1_health <= 0:
        P1_health = 0
        P2_win = True
    elif P2_health <= 0:
        P2_health = 0
        P1_win = True

    # clear the screen
    screen.fill((50, 50, 100))
    # draw sprites on the screen
    health_group.draw(screen)
    P1_group.draw(screen)
    P2_group.draw(screen)

    # show the status of two players
    print_text(font, 20, 540, f"Player1 ({P1_health}%), Charge status: {P1_power}")
    print_text(font, 20, 620, f"Player2 ({P2_health}%), Charge status: {P2_power}")

    # show the health point of the two players
    if not P2_win:
        pygame.draw.rect(screen, (50, 150, 50, 180), Rect(20, 570, P1_health * 2, 25))
    pygame.draw.rect(screen, (100, 200, 100, 180), Rect(20, 570, 200, 25), 2)
    if not P1_win:
        pygame.draw.rect(screen, (50, 150, 50, 180), Rect(20, 650, P2_health * 2, 25))
    pygame.draw.rect(screen, (100, 200, 100, 180), Rect(20, 650, 200, 25), 2)

    # charge the players for testing
    # players should be charged if they answer correctly in fully edition
    if pygame.key.get_pressed()[K_o]:
        P1_power = True
    if pygame.key.get_pressed()[K_p]:
        P2_power = True

    # let players fire
    if pygame.key.get_pressed()[K_1] and P1_power:
        P1_power = False
        Bullet.append(bullet(P1.X+45, P1.Y+40, P1, P1.direction))
    if pygame.key.get_pressed()[K_0] and P2_power:
        P2_power = False
        Bullet.append(bullet(P2.X+45, P2.Y+40, P2, P2.direction))

    # this list holds the bullets that need to be delete in next frame
    delete_bullets = []
    for i in range(len(Bullet)):
        # draw every bullet on the screen
        bullets = Bullet[i]
        pygame.draw.circle(screen, random_colour(), bullets.position_update(), 3)
        # cause the player to drop health when colliding and delete the bullet
        if bullets.collision_check(P1):
            P1_health -= random_health_drop()
            delete_bullets.append(i)
            # the bullet hits the player and causes it to move
            P1.velocity = calc_velocity(bullets.direction, 20)
            P1.X += P1.velocity.x
            P1.Y += P1.velocity.y
        if bullets.collision_check(P2):
            P2_health -= random_health_drop()
            delete_bullets.append(i)
            # the bullet hits the player and causes it to move
            P2.velocity = calc_velocity(bullets.direction, 20)
            P2.X += P2.velocity.x
            P2.Y += P2.velocity.y
        # delete the bullets that leave the screen
        not_in_screen = (bullets.x not in range(751) or (bullets.y not in range(751)))
        if not_in_screen:
            delete_bullets.append(i)

    # delete the bullets
    # I ignored the situation when two bullets need to be delete in one frame
    for x in delete_bullets:
        del Bullet[x]

    # show the winner when the game is over and delete the loser
    if P1_win:
        print_text(font2, 20, 60, "GAME OVER!!!", random_colour())
        print_text(font2, 20, 130, "Winner is P1", random_colour())
        # stop showing the loser
        P2_group = pygame.sprite.Group()
        # create the special effect for winner
        # basically just spinning the winner and shooting bullets
        if P1.direction != 6:
            P1.direction += 2
        else:
            P1.direction = 0
        Bullet.append(bullet(P1.X + 45, P1.Y + 40, P1, P1.direction))
    elif P2_win:
        print_text(font2, 20, 60, "GAME OVER!!!", random_colour())
        print_text(font2, 20, 130, "Winner is P2", random_colour())
        # stop showing the loser
        P1_group = pygame.sprite.Group()
        # create the special effect for winner
        # basically just spinning the winner and shooting bullets
        if P2.direction != 6:
            P2.direction += 2
        else:
            P2.direction = 0
        Bullet.append(bullet(P2.X + 45, P2.Y + 40, P2, P2.direction))
    # show the instruction of how to play the game
    print_text(font, 20, 0, "P1: WASD to move, 1 to shoot | P2 arrows to move, 0 to shoot")
    print_text(font, 20, 30, "O and P simulates correct answer for P1/P2")
    # update display
    pygame.display.update()