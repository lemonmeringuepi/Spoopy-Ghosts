import pygame


# Size of the screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = 'Spoopy Ghosts'
# Colors according to RGB codes
GRAY_COLOR = (155, 155, 155)
RED_COLOR = (250, 100, 50)
# Determines how many times per second to refresh (FPS)
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont('chilanka', 75)


# Load images
border = pygame.transform.scale(pygame.image.load('grassMid.png'), (50, 50))
border_corner = pygame.transform.scale(pygame.image.load('grasscorner.png'), (50,50))
hud1 = pygame.transform.scale(pygame.image.load('hud_1.png'), (30,30))
hud2 = pygame.transform.scale(pygame.image.load('hud_2.png'), (30,30))
hud3 = pygame.transform.scale(pygame.image.load('hud_3.png'), (30,30))
hud4 = pygame.transform.scale(pygame.image.load('hud_4.png'), (30,30))
hud5 = pygame.transform.scale(pygame.image.load('hud_5.png'), (30,30))
hud6 = pygame.transform.scale(pygame.image.load('hud_6.png'), (30,30))
heart_full = pygame.transform.scale(pygame.image.load('hud_heartFull.png'), (30,30))
heart_empty = pygame.transform.scale(pygame.image.load('hud_heartEmpty.png'), (30,30))

class Game:

    TICK_RATE = 60


    
    def __init__(self, image_path, title, width, height):
        self.title = title
        self.width = width
        self.height = height
        # Create the window.
        self.game_screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)

        
        # Set background
        background_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(background_image, (width, height))
        self.game_screen.fill(GRAY_COLOR)
        


    def run_game_loop(self, level, life):
        is_game_over = False
        did_win = False
        y_direction = 0
        x_direction = 0

        player = PlayerCharacter('p3_walk02.png', 75, 360, 50, 75)
        star = GameObject('star.png', 670, 375, 50, 50)

        ghost_1 = Enemy('ghost_normal.png', 200, 200, 50, 75, 3, 5)
        ghost_2 = Enemy('ghost_normal.png', 550, 600, 50, 75, 7, 4)        
        ghost_3 = Enemy('ghost_normal.png', 700, 150, 50, 75, -2, -6)
        ghost_4 = Enemy('ghost_normal.png', 300, 650, 50, 75, 0, 8)
        ghost_5 = Enemy('ghost_normal.png', 450, 100, 50, 75, 2, 0)
        ghost_6 = Enemy('ghost_normal.png', 600, 300, 50, 75, 7, 4)

        enemies = [ghost_1, ghost_2, ghost_3, ghost_4, ghost_5, ghost_6]
        ghosts = enemies[0:level]
        level_labels = [hud1, hud2, hud3, hud4, hud5, hud6]

        # Function to load background and border tiles
        def load_background():
            self.game_screen.fill(GRAY_COLOR)
            self.game_screen.blit(self.image, (0,0))
            for x in range(15):
                self.game_screen.blit(border, (x*50, 750))
                self.game_screen.blit(pygame.transform.flip(border, False, True), (x*50, 0))
                self.game_screen.blit(pygame.transform.rotate(border, 90), (750, x*50))
                self.game_screen.blit(pygame.transform.rotate(border, 270), (0, x*50))                
            self.game_screen.blit(border_corner, (750, 750))
            self.game_screen.blit(pygame.transform.flip(border_corner, True, False), (0, 750))
            self.game_screen.blit(pygame.transform.flip(border_corner, True, True), (0, 0))
            self.game_screen.blit(pygame.transform.flip(border_corner, False, True), (750, 0))
            self.game_screen.blit(level_labels[level-1], (10,10))

        # Function to load life bar
        def load_life(life):
            if life == 3:
                for x in range(3):
                    self.game_screen.blit(heart_full, (680 + x*40, 10))
            elif life == 2:
                for x in range(2):
                    self.game_screen.blit(heart_full, (680 + x*40, 10))
                self.game_screen.blit(heart_empty, (760, 10))
            elif life == 1:
                self.game_screen.blit(heart_full, (680, 10))
                for x in range(2):
                    self.game_screen.blit(heart_empty, (720 + x*40, 10))
            else:
                for x in range(3):
                    self.game_screen.blit(heart_empty, (680 + x*40, 10))

        
        while not is_game_over:

            # Set keystrokes
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        if event.key == pygame.K_UP:
                            y_direction = 1
                        else:
                            y_direction = -1
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                        if event.key == pygame.K_RIGHT:
                            x_direction = 1
                        else:
                            x_direction = -1
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        y_direction = 0
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        x_direction = 0

            # Runs function to load background and border
            load_background()
            load_life(life)

            # Loads star and player
            star.draw(self.game_screen)            
            player.move(x_direction, y_direction, self.width, self.height)
            player.draw(self.game_screen)
            

            # Load enemies
            for boo in ghosts:
                boo.move(self.width, self.height)
                boo.draw(self.game_screen)


            # Check collision
            if player.detect_collision(star):
                is_game_over = True
                did_win = True
                text = font.render('You did it!', True, RED_COLOR)
                self.game_screen.blit(text, (250, 350))
                pygame.display.update()
                clock.tick(1)
                break
            else:
                for boo in ghosts:
                    if player.detect_collision(boo):
                        is_game_over = True
                        did_win = False
                        text = font.render('Womp Womp!', True, RED_COLOR)
                        self.game_screen.blit(text, (200, 350))
                        pygame.display.update()
                        clock.tick(1)
                        break

            
            pygame.display.update()
            clock.tick(self.TICK_RATE)

        if did_win and level < 6:
            self.run_game_loop(level + 1, life)
        elif did_win == False and life > 0:
            self.run_game_loop(level, life - 1)
        else:
            return

class GameObject:

    def __init__(self, image_path, x, y, width, height):
        self.image = pygame.transform.scale(pygame.image.load(image_path), (width, height))
        self.x_pos = x
        self.y_pos = y

        self.width = width
        self.height = height

    def draw(self, background):
        background.blit(self.image, (self.x_pos, self.y_pos))
        
class PlayerCharacter(GameObject):

    # How many tiles the character moves per second
    SPEED = 10

    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)

    # Move function will move character up, down, left, and right
    def move(self, x_direction, y_direction, max_width, max_height):
        if y_direction > 0:
            self.y_pos -= self.SPEED
        elif y_direction < 0:
            self.y_pos += self.SPEED
        if x_direction > 0:
            self.x_pos += self.SPEED
        elif x_direction < 0:
            self.x_pos -= self.SPEED

        # Setting bounds
        if self.y_pos >= max_height - self.height - 50:
            self.y_pos = max_height - self.height - 50
        elif self.y_pos <= 50:
            self.y_pos = 50
        if self.x_pos >= max_width - self.width - 50:
            self.x_pos = max_width - self.width - 50
        elif self.x_pos <= 50:
            self.x_pos = 50

    def detect_collision(self, other_body):
        if ((self.y_pos <= other_body.y_pos <= (self.y_pos + self.height)) \
           or (self.y_pos <= (other_body.y_pos + other_body.height) <= (self.y_pos +self.height))) \
           and ((self.x_pos <= other_body.x_pos <= (self.x_pos + self.width)) \
           or (self.x_pos <= (other_body.x_pos + other_body.width) <= (self.x_pos +self.width))):
            return True
        else:
            return False

class Enemy(GameObject):


    def __init__(self, image_path, x, y, width, height, x_speed, y_speed):
        super().__init__(image_path, x, y, width, height)
        self.x_speed = x_speed
        self.y_speed = y_speed

    # Move function bounces character off of the walls
    def move(self, max_width, max_height):
        if self.x_pos <= 50:
            self.x_speed = abs(self.x_speed)
        if self.x_pos >= max_width - self.width - 50:
            self.x_speed = -abs(self.x_speed)
        if self.y_pos <= 50:
            self.y_speed = abs(self.y_speed)
        if self.y_pos >= max_height - self.height - 50:
            self.y_speed = -abs(self.y_speed)
        self.x_pos += self.x_speed
        self.y_pos += self.y_speed



pygame.init()

new_game = Game('bg_shroom.png', SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)
new_game.run_game_loop(1, 3)


pygame.quit()
quit()
