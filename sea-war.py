# Imports
import pygame
import random

# Initialize game engine
pygame.init()


# Window
WIDTH = 800
HEIGHT = 700
SIZE = (WIDTH, HEIGHT)
TITLE = "Battle For Tortuga"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)


# Timer
clock = pygame.time.Clock()
refresh_rate = 60

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

# Fonts
FONT_SM = pygame.font.Font("assets/fonts/piratefont.ttf", 24)
FONT_MD = pygame.font.Font("assets/fonts/piratefont.ttf", 32)
FONT_LG = pygame.font.Font("assets/fonts/piratefont.ttf", 64)
FONT_XL = pygame.font.Font("assets/fonts/piratefont.ttf", 96)

# Images
black_ship1 = pygame.image.load('Assets/Images/Ships/ship1.png')
black_ship2 = pygame.image.load('Assets/Images/Ships/ship6.png')
black_ship3 = pygame.image.load('Assets/Images/Ships/ship11.png')

blue_ship1 = pygame.image.load('Assets/Images/Ships/ship4.png')
blue_ship2 = pygame.image.load('Assets/Images/Ships/ship9.png')
blue_ship3 = pygame.image.load('Assets/Images/Ships/ship14.png')

yellow_ship1 = pygame.image.load('Assets/Images/Ships/ship5.png')
yellow_ship2 = pygame.image.load('Assets/Images/Ships/ship10.png')
yellow_ship3 = pygame.image.load('Assets/Images/Ships/ship15.png')

cannon_img =  pygame.image.load('Assets/Images/Weapons/cannon.png')
cannonball_img = pygame.image.load('Assets/Images/Weapons/cannonBall.png')
sea = pygame.image.load("Assets/Images/Effects/sea.png")
pirate_boat = pygame.image.load("Assets/Images/Effects/pirateboat.png")
cross_bones = pygame.image.load("Assets/Images/Effects/crossbones.png")

player_img1 = black_ship1
player_img2 = black_ship2
player_img3 = black_ship3

mob_img1 = blue_ship1
mob_img2 = blue_ship2
mob_img3 = blue_ship3

yacht_img1 = yellow_ship1
yacht_img2 = yellow_ship2
yacht_img3 = yellow_ship3

#Sound
pygame.mixer.music.load("Assets/Sounds/background_dank_music.ogg")
yell = pygame.mixer.Sound("Assets/Sounds/pirateyell.ogg")
death = pygame.mixer.Sound("Assets/Sounds/deathyell.ogg")
boom = pygame.mixer.Sound("Assets/Sounds/boom.ogg")

# Stages
START = 0
PLAYING = 1
END = 2
BEAT = 3

# Game classes
class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.speed = 5
        self.shield = 3
        self.shot_timer = 0

    def move_left(self):
        self.rect.x -= self.speed
        
    def move_right(self):
        self.rect.x += self.speed

    def shoot(self):
        if self.shot_timer <= 0:
            laser = Laser(cannonball_img)
            laser.rect.centerx = self.rect.centerx
            laser.rect.centery = self.rect.top
            lasers.add(laser)
            self.shot_timer = 40
        

    def update(self, bombs,cannons):
        self.shot_timer -= 1
        hit_list_1 = pygame.sprite.spritecollide(self, bombs, True, pygame.sprite.collide_mask)
        hit_list_2 = pygame.sprite.spritecollide(self, cannons, True, pygame.sprite.collide_mask)
        players = player.sprites()
        
        for hit in hit_list_1:
            self.shield -= 1
            boom.play()

        for hit in hit_list_2:
            self.shield = 0
            

        hit_list_1 = pygame.sprite.spritecollide(self, mobs, False, pygame.sprite.collide_mask)
        hit_list_2 = pygame.sprite.spritecollide(self,yachts, False, pygame.sprite.collide_mask)

        if len(hit_list_1) > 0 or len(hit_list_2) > 0:
            self.shield = 0
        

        if self.shield == 2:
            self.image = player_img2

        if self.shield == 1:
            self.image = player_img3
            
        if self.shield == 0:
            self.kill()
            death.play()

        if self.rect.right < 0:
            self.rect.left = WIDTH

        if self.rect.left > WIDTH:
            self.rect.right = 0

        
    
class Laser(pygame.sprite.Sprite):
    
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()

        self.speed = 5

    def update(self):
        self.rect.y -= self.speed

        if self.rect.bottom < 0:
            self.kill()


class Mob(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.health = 2
        
        
    
    def drop_bomb(self):
        bomb = Bomb(cannonball_img)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.bottom
        bombs.add(bomb)
    
    def update(self, lasers, player):
        hit_list = pygame.sprite.spritecollide(self, lasers, True, pygame.sprite.collide_mask)
        
        if len(hit_list) > 0:
            self.health -= 1
            player.score += 3141519625359
            boom.play()

        if self.health == 1:
            self.image = mob_img3
            
        if self.health == 0:
            self.kill()
            yell.play()
            
class Bomb(pygame.sprite.Sprite):
    
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
        
        if self.rect.top > HEIGHT:
            self.kill()
            
class Yacht(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.health = 3
        
        
    
    def drop_cannon(self):
        cannon = Cannon(cannon_img)
        cannon.rect.centerx = self.rect.centerx
        cannon.rect.centery = self.rect.bottom
        cannons.add(cannon)
    
    def update(self, lasers, player):
        hit_list = pygame.sprite.spritecollide(self, lasers, True, pygame.sprite.collide_mask)
        
        if len(hit_list) > 0:
            self.health -= 1
            player.score += 6282028240608
            boom.play()

        if self.health == 2:
            self.image = yacht_img2

        if self.health == 1:
            self.image = yacht_img3
            
        if self.health == 0:
            self.kill()
            yell.play()
            
        

class Cannon(pygame.sprite.Sprite):
    
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
        
        if self.rect.top > HEIGHT:
            self.kill()
            
            
    
class Fleet:

    def __init__(self, mobs, speed):
        self.mobs = mobs
        self.moving_right = True
        self.speed = speed
        self.bomb_rate = 60

    def move(self):
        reverse = False
        
        for m in mobs:
            if self.moving_right:
                m.rect.x += self.speed
                if m.rect.right >= WIDTH:
                    reverse = True
            else:
                m.rect.x -= self.speed
                if m.rect.left <=0:
                    reverse = True

        if reverse == True:
            self.moving_right = not self.moving_right
            for m in mobs:
                m.rect.y += 32
        

    def choose_bomber(self):
        rand = random.randrange(0, self.bomb_rate)
        all_mobs = mobs.sprites()
        
        if len(all_mobs) > 0 and rand == 0:
            return random.choice(all_mobs)
        else:
            return None
        
    def update(self):
        all_mobs = mobs.sprites()
        
        if len(all_mobs) == 0:
            stage = END
        
        self.move()

        bomber = self.choose_bomber()
        if bomber != None:
            bomber.drop_bomb()

class Flock:

    def __init__(self, yachts,speed):
        self.yachts = yachts
        self.moving_left = True
        self.speed = speed
        self.bomb_rate = 90

    def move(self):
        reverse = False
        
        for y in yachts:
            if self.moving_left:
                y.rect.x -= self.speed
                if y.rect.left <= 0:
                    reverse = True
            else:
                y.rect.x += self.speed
                if y.rect.right >=WIDTH:
                    reverse = True

        if reverse == True:
            self.moving_left = not self.moving_left
            
        

    def choose_bomber(self):
        rand = random.randrange(0, self.bomb_rate)
        all_yachts = yachts.sprites()
        
        if len(all_yachts) > 0 and rand == 0:
            return random.choice(all_yachts)
        else:
            return None
        
    def update(self):
        self.move()

        bomber = self.choose_bomber()
        if bomber != None:
            bomber.drop_cannon()

    


# Game helper functions
def show_title_screen():
    title_text = FONT_LG.render("Battle for Tortuga", 1, WHITE)
    title_text_rect = title_text.get_rect(center = (WIDTH/2 , 300))
    screen.blit(pirate_boat, [0,0])
    screen.blit(title_text, title_text_rect)

def show_death_screen():
    death_text = FONT_LG.render("You Have Died", 1, WHITE)
    death_text_rect = death_text.get_rect(center = (WIDTH/2 , 300))
    cross_bones_rect = cross_bones.get_rect(center = (WIDTH/2 , 350))
    screen.blit(cross_bones, cross_bones_rect)
    screen.blit(death_text, death_text_rect)

def show_stats(player):
    score_text = FONT_MD.render("score " + str(player.score), 1, WHITE)
    shield_text = FONT_MD.render("shield", 1, WHITE)
    level_text = FONT_MD.render("level " + str(player.level), 1, WHITE)
    
    if ship.shield == 3:
        pygame.draw.rect(screen, WHITE, [118, 74, 100, 18])
        pygame.draw.rect(screen, GREEN, [118, 74, 100, 18])
    elif ship.shield == 2:
        pygame.draw.rect(screen, WHITE, [118, 74, 100, 18])
        pygame.draw.rect(screen, GREEN, [118, 74, 67, 18])
    elif ship.shield == 1:
        pygame.draw.rect(screen, WHITE, [118, 74, 100, 18])
        pygame.draw.rect(screen, GREEN, [118, 74, 33, 18])
    else:
        pygame.draw.rect(screen, RED, [118, 74, 100, 18])


    screen.blit(score_text, [32, 32])
    screen.blit(shield_text, [32, 64])
    screen.blit(level_text, [700, 32])
   
def setup():
    global ship, mobs, stage, player, bombs, lasers, fleet, flock, yachts, cannons
    
    # sprite groups
    mobs = pygame.sprite.Group()
    
    yachts = pygame.sprite.Group()

    
    # Make game objects
    ship = Ship(358, 570, player_img1)
    mob1 = Mob(228, 64, mob_img1)
    mob2 = Mob(356, 64, mob_img1)
    mob3 = Mob(484, 64, mob_img1)
    mobs.add(mob1, mob2, mob3)
    fleet = Fleet(mobs, 3)
    flock = Flock(yachts, 2)
            
    #Make sprite groups
    player = pygame.sprite.GroupSingle()
    player.add(ship)
    player.score = 0

    lasers = pygame.sprite.Group()
    bombs = pygame.sprite.Group()
    cannons = pygame.sprite.Group()

    # set level
    player.level = 1

    # set stage
    stage = START

def level_change():
    global ship, mobs, stage, player, bombs, lasers, fleet, flock, yachts, cannons
    stage = PLAYING
    if player.level == 2:
        mob1 = Mob(228, 64, mob_img1)
        mob2 = Mob(356, 64, mob_img1)
        mob3 = Mob(484, 64, mob_img1)
        mob4 = Mob(228, -60, mob_img1)
        mob5 = Mob(356, -60, mob_img1)
        mob6 = Mob(484, -60, mob_img1)
        mobs.add(mob1, mob2, mob3, mob4, mob5, mob6)
        fleet = Fleet(mobs, 3)
        flock = Flock(yachts, 2)
    if player.level == 3:
        mob1 = Mob(228, 64, mob_img1)
        mob2 = Mob(356, 64, mob_img1)
        mob3 = Mob(484, 64, mob_img1)
        yacht1 = Yacht(100, 100, yacht_img1)
        yacht2 =  Yacht(350, 100, yacht_img1)
        mobs.add(mob1, mob2, mob3)
        yachts.add(yacht1, yacht2) 
        fleet = Fleet(mobs, 3)
        flock = Flock(yachts, 2)
    if player.level == 4:
        mob1 = Mob(228, 64, mob_img1)
        mob2 = Mob(356, 64, mob_img1)
        mob3 = Mob(484, 64, mob_img1)
        mob4 = Mob(228, -60, mob_img1)
        mob5 = Mob(356, -60, mob_img1)
        mob6 = Mob(484, -60, mob_img1)
        yacht1 = Yacht(100, 100, yacht_img1)
        yacht2 =  Yacht(350, 100, yacht_img1)
        mobs.add(mob1, mob2, mob3, mob4, mob5, mob6)
        yachts.add(yacht1, yacht2)
        fleet = Fleet(mobs, 3)
        flock = Flock(yachts, 2)
    if player.level >= 5:
        mob1 = Mob(228, 64, mob_img1)
        mob2 = Mob(356, 64, mob_img1)
        mob3 = Mob(484, 64, mob_img1)
        mob4 = Mob(228, -60, mob_img1)
        mob5 = Mob(356, -60, mob_img1)
        mob6 = Mob(484, -60, mob_img1)
        yacht1 = Yacht(100, 100, yacht_img1)
        yacht2 =  Yacht(350, 100, yacht_img1)
        mobs.add(mob1, mob2, mob3, mob4, mob5, mob6)
        yachts.add(yacht1, yacht2)
        fleet = Fleet(mobs, (player.level * 1.1))
        flock = Flock(yachts, (player.level * 7/8))
    
# Game loop
setup()
done = False

while not done:
    # Event processing (React to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if stage == START:
                if event.key == pygame.K_SPACE:
                    stage = PLAYING
            elif stage == PLAYING:
                if event.key == pygame.K_SPACE:
                    ship.shoot()
            
                    
            elif stage == END:
                if event.key == pygame.K_SPACE:
                    setup()
                    
    if stage == PLAYING:
        pygame.mixer.music.pause()
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_a] or pressed[pygame.K_LEFT]:
            ship.move_left()
        elif pressed[pygame.K_d] or pressed[pygame.K_RIGHT]:
            ship.move_right()

    if stage == START:
        pygame.mixer.music.play(1)
   
    
    # Game logic (Check for collisions, update points, etc.)
    if stage == PLAYING:
        player.update(bombs, cannons)
        lasers.update()   
        mobs.update(lasers, player)
        yachts.update(lasers,player)
        bombs.update()
        cannons.update()
        fleet.update()
        flock.update()

        if len(player) == 0:
            stage = END
        all_mobies = mobs.sprites() + yachts.sprites()
        if len(all_mobies) == 0:
            stage = BEAT
    elif stage == BEAT:
                player.level += 1
                level_change()

    
        
    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    screen.blit(sea, [0,0])
    lasers.draw(screen)
    player.draw(screen)
    bombs.draw(screen)
    cannons.draw(screen)
    mobs.draw(screen)
    yachts.draw(screen)
    show_stats(player)

    if stage == START:
        show_title_screen()
    if stage == END:
        show_death_screen()


    
    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()


    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
