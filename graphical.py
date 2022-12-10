import board
import pygame
import time
from random import choice, randrange

get_color = lambda : (randrange(30, 256), randrange(30, 256), randrange(30, 256))
W, H = 10, 20
TILE = 35
GAMEWIDTH = W * TILE + 300
GAMEHEIGHT = H * TILE + 100
GAME_RES = GAMEWIDTH, GAMEHEIGHT
TETRIS_TYPE = False
FPS = 30
BEST_SCORE_FILE_NAME = "best_score"
figure_rect = pygame.Rect(0,0,TILE-2,TILE-2)
anim_count, anim_speed, anim_limit = 0, 60, 2000

class Button():
    def __init__(self, x, y, image):
        width = image.get_width()
        height = image.get_height()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
        
    def draw(self):
        action = False
        #get mouse pos
        pos = pygame.mouse.get_pos()
        
        #check mousver and click
        if self.rect.collidepoint(pos): 
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                print("clicked")
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False     
                
        game_sc.blit(self.image, (self.rect.x, self.rect.y))
        
        return action
        

def draw_text(text, font, text_col, x, y):
    text_img = font.render(text, True, text_col)
    text_width = text_img.get_width()
    game_sc.blit(text_img, ((x - text_width)/2, y))
    
def draw_scores(text_col):
    X = []
    with open(BEST_SCORE_FILE_NAME+".txt", "r+") as file:            
        for line in file:
            X.append(line)
    if len(X) < 9:
        smaller = len(X)
    else:
        smaller = 9
    for i in range(0,smaller):
        index = str(i+1)
        text = index + "." + " " + X[i]
        text = text[:-1]
        text_img = font.render(text, True, text_col)
        text_width = text_img.get_width()
        game_sc.blit(text_img, ((GAMEWIDTH - text_width)/2, 50+50 * (i+1)))
        
def draw_board():
    for a in range(H):
        for b in range(W):
            if game_board.board[a][b] == 1:
                figure_rect.y = a * TILE
                figure_rect.x = b * TILE
                pygame.draw.rect(game_sc, pygame.Color('red'), figure_rect)
 
def draw_help():
    score_text = "Score: " +str(game_board.score)
    draw_text(score_text, extra_extra_font, 'yellow', GAMEWIDTH * 2 - 400, GAMEHEIGHT * 0.02)
    lines_text = "Lines: " + str(game_board.lines)
    draw_text(lines_text, extra_extra_font, 'yellow', GAMEWIDTH * 2 - 400, GAMEHEIGHT * 0.08)
    level_text = "Level: " + str(game_board.level)
    draw_text(level_text, extra_extra_font, 'yellow', GAMEWIDTH * 2 - 400, GAMEHEIGHT * 0.14)
    best_score_text = "Best score: " + str(game_board.best_score)
    draw_text(best_score_text, extra_extra_font, 'yellow', GAMEWIDTH * 2 - 300, GAMEHEIGHT * 0.20)   
    best_score_text = "Next block"
    draw_text(best_score_text, extra_extra_font, 'yellow', GAMEWIDTH * 2 - 400, GAMEHEIGHT * 0.28)               

def draw_block():
    for a in range(game_board.current_block.size()[0]):
        for b in range(game_board.current_block.size()[1]):
            if game_board.current_block.shape[a][b] == 1:
                x = game_board.current_block_pos[1] + b + 1
                y = game_board.current_block_pos[0] + a + 1
                figure_rect.y = y * TILE - TILE
                figure_rect.x = x * TILE - TILE
                pygame.draw.rect(game_sc, pygame.Color('white'), figure_rect)
                  
def draw_burn(row, amount):
    for j in range(amount ):
        for i in range(W):
               figure_rect
               figure_rect.y = (row - j )* TILE 
               figure_rect.x = i * TILE 
               pygame.draw.rect(game_sc, get_color(), figure_rect)
               pygame.display.flip()
               clock.tick(20)   
            
def draw_next():
    for a in range(game_board.next_block.size()[0]):
        for b in range(game_board.next_block.size()[1]):
            if game_board.next_block.shape[a][b] == 1:
                figure_rect.y = a * TILE + 220
                figure_rect.x = b * TILE + 530
                pygame.draw.rect(game_sc, pygame.Color('white'), figure_rect)
                
def init():
    pygame.init()
    global game_board, extra_extra_font, menu_img, replay_img, game_sc, bg, grid, extra_font, clock, TEXT_COLOR, font, ispaused, start_img, quit_img, leaderboard_img, back_img, return_img, pause_img
    game_board = board.Board(H, W)
    game_board.start(1)
    TEXT_COLOR = ('white')
    game_sc = pygame.display.set_mode(GAME_RES)
    extra_font = pygame.font.Font('font.ttf', 36)
    extra_extra_font = pygame.font.Font('font.ttf', 20)
    font = pygame.font.SysFont("ubuntu", 36)
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    bg = pygame.image.load('img/bg2.jpg').convert()
    replay_img = pygame.image.load('img/button_replay.png').convert_alpha()
    menu_img = pygame.image.load('img/button_menu.png').convert_alpha()
    start_img = pygame.image.load('img/button_start.png').convert_alpha()
    quit_img = pygame.image.load('img/button_quit.png').convert_alpha()
    leaderboard_img = pygame.image.load('img/button_leaderboard.png').convert_alpha()
    back_img = pygame.image.load('img/button_back.png').convert_alpha()
    pause_img = pygame.image.load('img/button_pause.png').convert_alpha()
    return_img = pygame.image.load('img/button_return.png').convert_alpha()
    grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)]
    
def game():
    inmenu = True
    inleaderboard = False
    gameover = False
    ingame = False
    drawn = False
    paused = False
    spressed = False
    init()   
    while True:
        while inmenu:
            if drawn == False:
                game_sc.blit(bg, (0,0))
                
                draw_text("TETRIS", extra_font, 'yellow',GAMEWIDTH, GAMEHEIGHT * 0.05)
                start_button = Button((GAMEWIDTH - start_img.get_width())/ 2, GAMEHEIGHT * 0.20, start_img)
                leaderboard_button = Button((GAMEWIDTH - leaderboard_img.get_width())/ 2, GAMEHEIGHT * 0.35, leaderboard_img)
                quit_button = Button((GAMEWIDTH - quit_img.get_width())/ 2, GAMEHEIGHT * 0.50, quit_img)
                drawn = True
            if start_button.draw():
                global start
                start = time.time()
                inmenu = False
                ingame = True
                drawn = False
            if leaderboard_button.draw():
                inmenu = False
                inleaderboard = True  
                drawn = False
            if quit_button.draw():
                inmenu = False
                pygame.quit()    
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:              
                    pygame.quit()

            pygame.display.flip()
            clock.tick(FPS)  

        while inleaderboard:
            if drawn == False:
                game_sc.blit(bg, (0,0))
                draw_text("LEADERBOARDS", extra_font, 'yellow', GAMEWIDTH, GAMEHEIGHT * 0.05)
                back_button = Button((GAMEWIDTH - back_img.get_width())/ 2, GAMEHEIGHT * 0.80, back_img)
                draw_scores(TEXT_COLOR)
                drawn = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            if back_button.draw():
                inleaderboard = False
                inmenu = True
                drawn = False

            pygame.display.flip()
            clock.tick(FPS)

        while gameover:
            if drawn == False:
                game_sc.blit(bg, (0,0))
                draw_text("GAME OVER", extra_font, 'yellow', GAMEWIDTH, GAMEHEIGHT * 0.3)
                replay_button = Button((GAMEWIDTH - replay_img.get_width())/ 5 * 1, GAMEHEIGHT * 0.5, replay_img)
                menu_button = Button((GAMEWIDTH - menu_img.get_width())/ 5 * 4, GAMEHEIGHT * 0.5, menu_img)
                drawn = True
            if replay_button.draw():
                gameover = False
                ingame = True
                drawn = False
                game_board.start(1)
                            
            if menu_button.draw():
                gameover = False
                ingame = False
                inmenu = True
                drawn = False
                game_board.start(1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            pygame.display.flip()
            clock.tick(FPS)
            
        while ingame:
            if not game_board.is_game_over():
                if game_board.is_burn():
                    draw_burn(game_board.burn_row, game_board.burn_amount)
                    game_board.was_burn = False
                    game_board.burn_amount  = 0 
                game_sc.blit(bg, (0,0))
                [pygame.draw.rect(game_sc, (40,40,40), i_rect, 1) for i_rect in grid] 
                draw_block()    
                draw_board()
                draw_help()
                draw_next()
            if drawn == False:
                game_sc.blit(bg, (0,0))
                [pygame.draw.rect(game_sc, (40,40,40), i_rect, 1) for i_rect in grid] 
                pause_button = Button((GAMEWIDTH - pause_img.get_width())/ 3, GAMEHEIGHT * 0.90, pause_img)
                quit_button = Button((GAMEWIDTH - quit_img.get_width())/ 3 * 2, GAMEHEIGHT * 0.90, quit_img)
                drawn = True
            if quit_button.draw():
                inleaderboard = False
                inmenu = True
                ingame = False
                game_board.start(1)
                drawn = False
                
            if pause_button.draw():
                paused = True
                
            if time.time() - start >= 1 / game_board.level:  
                game_board.move_block("down")
                start = time.time()
                spressed = False
                    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if pygame.key.get_pressed()[pygame.K_p]:
                    paused = True
                if pygame.key.get_pressed()[pygame.K_LEFT]:
                    game_board.move_block("left")
                if pygame.key.get_pressed()[pygame.K_RIGHT]:
                    game_board.move_block("right")
                if pygame.key.get_pressed()[pygame.K_UP]:
                    game_board.rotate_block()
                if pygame.key.get_pressed()[pygame.K_DOWN]:
                    game_board.move_block("down")
                if pygame.key.get_pressed()[pygame.K_SPACE] and spressed == False:
                    game_board.drop()
                    spressed = True
                    
            if game_board.is_game_over():
                for i in range(W):
                    for j in range(H):
                        figure_rect
                        figure_rect.y = j * TILE 
                        figure_rect.x = i * TILE 
                        pygame.draw.rect(game_sc, get_color(), figure_rect)
                        pygame.display.flip()
                        clock.tick(100)
                print("Game over")
                gameover = True
                ingame = False
                drawn = False
                    
            while paused:
                game_sc.blit(bg, (0,0))
                draw_text("Game is paused...", font, TEXT_COLOR, GAMEWIDTH, GAMEHEIGHT * 0.30)
                button_return = Button((GAMEWIDTH - return_img.get_width())/2, GAMEHEIGHT * 0.40, return_img)
                if button_return.draw():
                    paused = False
                    drawn = False
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
                    if pygame.key.get_pressed()[pygame.K_p]:
                        drawn = False
                        paused = False
                pygame.display.flip()
                clock.tick(FPS)
            pygame.display.flip()
            clock.tick(FPS)

