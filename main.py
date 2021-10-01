import pygame, sys, random
from pygame import display, event, image, transform, time,font, mixer

def draw_floor():
    screen.blit(floor, (floor_x_pos, 650))
    screen.blit(floor, (floor_x_pos + 432, 650))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (500, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop = (500, random_pipe_pos - 680))
    return bottom_pipe, top_pipe

def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipe(pipes):
    for pipe in pipes:

        if pipe.bottom >= 600:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes, score):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            mixer.Sound('./sound/sfx_hit.wav').play()
            return False, score
        if bird_rect.centerx == pipe.centerx:
            score += 0.5
            mixer.Sound('./sound/sfx_point.wav').play()
    if bird_rect.top <= -25 or bird_rect.bottom >= 650:
        mixer.Sound('./sound/sfx_swooshing.wav').play()
        return False, score
    return True, score

def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1, -bird_movement*3, 1)
    return new_bird

def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect

def score_display():
    score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
    score_rect = score_surface.get_rect(center = (216, 100))
    screen.blit(score_surface, score_rect)

def hightscore_display():
    score_surface = game_font.render(f'Hight Score: {int(hight_score)}', True, (255, 255, 255))
    score_rect = score_surface.get_rect(center=(216, 200))
    screen.blit(score_surface, score_rect)

    message_surface = image.load('./assets/message.png').convert_alpha()
    message_rect = message_surface.get_rect(center = ((216, 400)))
    screen.blit(message_surface, message_rect)

mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
screen = display.set_mode((432, 768))
display.set_caption('Flappy Bird')

clock = time.Clock()
game_font = font.Font('04B_19.TTF', 40)

score = 0
hight_score = 0
gravity = 0.25
game_active = False


# Create background
bg = image.load('./assets/background-night.png').convert()
bg = transform.scale2x(bg)

# Create floor
floor = image.load('./assets/floor.png').convert()
floor = transform.scale2x(floor)
floor_x_pos = 0

# Create bird
bird_down = transform.scale2x(image.load('./assets/yellowbird-downflap.png').convert_alpha())
bird_mid = transform.scale2x(image.load('./assets/yellowbird-midflap.png').convert_alpha())
bird_up = transform.scale2x(image.load('./assets/yellowbird-upflap.png').convert_alpha())
bird_list = [bird_down, bird_mid, bird_up]
bird_index = 0

bird = bird_list[bird_index]

# bird = image.load('./assets/yellowbird-midflap.png').convert_alpha()
# bird = transform.scale2x(bird)
bird_rect = bird.get_rect(center = (100, 384))
bird_movement = 0
birdflap = pygame.USEREVENT + 1
time.set_timer(birdflap, 200)

# Create pipe
pipe_surface = image.load('./assets/pipe-green.png').convert()
pipe_surface = transform.scale2x(pipe_surface)
pipe_list = []
pipe_height = [200, 300, 400]

# Create Timer
spawnpipe = pygame.USEREVENT
time.set_timer(spawnpipe, 1200)

# Audio
flap_sound = mixer.Sound('./sound/sfx_wing.wav')

# Game loop
while True:
    for e in event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                if game_active:
                    bird_movement = -7.5
                    flap_sound.play()
                else:
                    game_active = True
                    pipe_list.clear()
                    bird_rect.center = (100, 384)
                    bird_movement = 0
                    score = 0
        if e.type == spawnpipe:
            pipe_list.extend(create_pipe())
        if e.type == birdflap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, bird_rect = bird_animation()

    screen.blit(bg, (0, 0))
    if game_active:
        # bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active, score = check_collision(pipe_list, score)

        # pipes
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)

        # score
        score_display()
    else:
        if score > hight_score:
            hight_score = score
        hightscore_display()

    # floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -432:
        floor_x_pos = 0

    display.update()
    clock.tick(80)