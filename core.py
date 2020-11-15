import sys, random
import pygame

def draw_ground(): # Draws 2 ground surfaces. Second one is right behind first
    screen.blit(ground_surface, (ground_x_position,920))
    screen.blit(ground_surface, (ground_x_position + 576,920))

def create_pipe(): # Creates rectangular over pipe_surface
    random_pipe_position = random.choice(pipe_size)
    bottom_pipe = pipe_surface.get_rect(midtop = (700,random_pipe_position))
    top_pipe = pipe_surface.get_rect(midbottom = (700,random_pipe_position - 300))
    
    return bottom_pipe, top_pipe

def draw_pipes(pipes): # Draws pipes
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe_surface = pygame.transform.flip(pipe_surface, False, True) # flip(surface, X, Y)
            screen.blit(flip_pipe_surface, pipe)

def move_pipes(pipes): # Pipe list movement
    for pipe in pipes:
        pipe.centerx -= 5
    
    return pipes

def check_collision(pipes): # Check for Bird collision with different surfaces
    for pipe in pipes:
        if bird_rectangular.colliderect(pipe): # Check if bird_rectangular colides with pipe via colliderect()
            hit_sound.play()
            return False
    
    if bird_rectangular.bottom >= 920: # Collision with the ground
        hit_sound.play()
        return False

    if bird_rectangular.top <= 0: # Collision with the top of the screen
        hit_sound.play()
        return False

    return True

def rotate_bird(bird): # Rotates bird surface to create Fly-Up and Fall-Down effects
    new_bird = pygame.transform.rotozoom(bird, -bird_movement*3, 1) # rotozoom(surface, angle, scale)

    return new_bird

def bird_animation_rectangular(): # Creates rectangular over different bird frames
    new_bird = bird_frames[bird_index]
    new_bird_rectangular = new_bird.get_rect(center = (100,bird_rectangular.centery)) # The Bird's X is always 100 while Y is changing so we get it from .centery

    return new_bird, new_bird_rectangular

def score_display(game_state): # Renders Score during game and High Score when game is over
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (250,250,250))
        score_rectangular = score_surface.get_rect(center = (288,50))
        screen.blit(score_surface, score_rectangular)
        if score >=1:
            score_sound.play()
    if game_state == 'game_over':
        score_surface = game_font.render(f'Your score: {int(score)}', True, (250,250,250))
        score_rectangular = score_surface.get_rect(center = (288,850))
        screen.blit(score_surface, score_rectangular)

        high_score_surface = game_font.render(f'High score: {int(high_score)}', True, (250,250,250))
        high_score_rectangular = high_score_surface.get_rect(center = (288,100))
        screen.blit(high_score_surface, high_score_rectangular)

def score_update(score, high_score): # Updates the High Score
    if score > high_score:
        high_score = score
    return high_score


pygame.mixer.pre_init(frequency = 44100, size = -16, channels = 5, buffer = 1024) # Pre initiates sound mixer to cut oof the sound delay
pygame.init()
screen = pygame.display.set_mode((567,1024))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf',40)

#Game Variables
gravity = 0.25
bird_movement = 0
game_is_active = False
game_start_surface = pygame.transform.scale2x(pygame.image.load('sprites/startgame.png').convert_alpha())
game_start_rectangular = game_start_surface.get_rect(center = (288,512))
game_over_surface = pygame.transform.scale2x(pygame.image.load('sprites/gameover.png').convert_alpha())
game_over_rectangular = game_over_surface.get_rect(center = (288,512))

#Game Icon & Name
window_icon = pygame.image.load('favicon.ico')
pygame.display.set_icon(window_icon)
pygame.display.set_caption('Flappy Bird')
score = 0
high_score = 0
score_sound = pygame.mixer.Sound('audio/point.wav')

#Background
bg_surface = pygame.image.load('sprites/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface) # Scales original to 2X

#Ground
ground_surface = pygame.image.load('sprites/base.png').convert()
ground_surface = pygame.transform.scale2x(ground_surface)
ground_x_position = 0

#Pipes
pipe_surface = pygame.image.load('sprites/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
#Pipe list for rectangular wrapping
pipe_list = []
pipe_size = [400, 600, 800]
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

#Bird
# convert_alpha() keeps alpha channel of the original image
bird_downflap = pygame.transform.scale2x(pygame.image.load('sprites/bluebird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('sprites/bluebird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('sprites/bluebird-upflap.png').convert_alpha())
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rectangular = bird_surface.get_rect(center = (100,512)) # Puts rectangular around bird_surface
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)
flap_sound = pygame.mixer.Sound('audio/wing.wav')
death_sound = pygame.mixer.Sound('audio/die.wav')
hit_sound = pygame.mixer.Sound('audio/hit.wav')

while True: # Loops the game to have it running on the screen
    for event in pygame.event.get(): # Game Event loop
        if event.type == pygame.QUIT: # Closing a game successfully
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN: # Checks for keyboard input
            if event.key == pygame.K_SPACE and game_is_active: # If Keyboard input == SPACE and Game is active
                bird_movement = 0 # Resest movement to exclude gravity 
                bird_movement -= 12
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_is_active == False: # Restars the Game is SPACE was pressed
                game_is_active = True
                # Clearing pipe_list, Moving bird and Score to the default possision and Restarting bird movement
                pipe_list.clear()
                bird_rectangular.center = (100,512)
                bird_movement = 0
                score = 0
        if event.type == pygame.MOUSEBUTTONDOWN: # Check for mouse input
            if (event.button == 1 or event.button == 3) and game_is_active: # 1 == Left Mouse Button // 3 == Right Mouse Button. If Mouse Button Click and Game is active
                bird_movement = 0 # Resest movement to exclude gravity 
                bird_movement -= 12
                flap_sound.play()
        if event.type == SPAWNPIPE: # Adds more pipes
            pipe_list.extend(create_pipe())
        if event.type == BIRDFLAP: # Animates the bird while using the list index
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            
            bird_surface, bird_rectangular = bird_animation_rectangular()

    # Background
    screen.blit(bg_surface, (0,0)) # Starts drawing from Top Left corner of the window
    
    # Start Game
    #screen.blit(game_start_surface, (100,200))

    #Ground
    ground_x_position -= 1 # Moves ground every frame
    draw_ground()
    if ground_x_position <= -576: # If first ground_surface is out of picture - restarts X point for it. For continuous ground effect
        ground_x_position = 0

    if game_is_active:
        #Bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rectangular.centery += bird_movement # Moves bird_rectangular on Y with bird_movement
        screen.blit(rotated_bird, bird_rectangular)
        game_is_active = check_collision(pipe_list)
        
        #Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        score += 0.01
        score_display('main_game')
    else:
        pygame.time.delay(700)
        high_score = score_update(score, high_score)
        screen.blit(game_over_surface,game_over_rectangular)
        score_display('game_over')
        #death_sound.play().fadeout(800)
        #if death_sound.get_num_channels() > 1:
         #   death_sound.set_volume(0.0)

    
    
    pygame.display.update() # Redraws the image for game display
    clock.tick(120) # Max Framerate


pygame.quit()

# Clear out sound channels after Game Over to cut off the repeat.
# Fix Hit sound
# Fix death sound playback