import curses
import time
import board
import os
import readchar
import graphical
import sys 

menu = ['Play', 'Level:', 'Scoreboard', 'Exit']

BOARD_WIDTH = 10
BOARD_HEIGHT = 20

GAME_WINDOW_WIDTH = 2 * BOARD_WIDTH + 2
GAME_WINDOW_HEIGHT = BOARD_HEIGHT + 2

HELP_WINDOW_WIDTH = 19
HELP_WINDOW_HEIGHT = 7

STATUS_WINDOW_HEIGHT = 12
STATUS_WINDOW_WIDTH = HELP_WINDOW_WIDTH

TITLE_HEIGHT = 6

LEFT_MARGIN = 3
BEST_SCORE_FILE_NAME = "best_score"
TITLE_WIDTH = FOOTER_WIDTH = 50

menulevel = 1
inprogram = True
inmenu = True
ingame = False
inscoreboard = False
pause = False

#defines a type of tetris game
#0 for console version, 1 for graphical version
#default 0
TETRIS_TYPE = 0 

def init_colors():
    """Init colors"""

    curses.init_pair(99, 8, curses.COLOR_BLACK)  # 1 - grey
    curses.init_pair(98, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(97, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(96, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(95, curses.COLOR_BLACK, curses.COLOR_WHITE)

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_BLACK, 13)  # 13 - pink
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
    curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_WHITE)

def draw_menu(window, selected_row_idx):
    window.clear()
    window.border()
    h, w = window.getmaxyx()
    for idx, row in enumerate(menu):
        x = w//2 - len(row)//2
        y = h//2 - len(menu)//2 + idx
        if idx == selected_row_idx:
            window.attron(curses.color_pair(25))
            window.addstr(y, x, row)
            if row == "Level:":
                window.addstr(y, x+6, str(menulevel))
            window.attroff(curses.color_pair(25))
        else:
            window.addstr(y, x, row)
            if row == "Level:":
                window.addstr(y, x+6, str(menulevel))    
    draw_menu_title(window)           
    window.refresh()

def draw_menu_title(window):
    window.addstr(1, 7, "#####  ####  #####  ###    #   ####",
                  curses.color_pair(98))
    window.addstr(2, 7, "  #    #       #    #  #   #  #",
                  curses.color_pair(98))
    window.addstr(3, 7, "  #    ###     #    # #    #   ###",
                  curses.color_pair(98))
    window.addstr(4, 7, "  #    #       #    #  #   #      #",
                  curses.color_pair(98))
    window.addstr(5, 7, "  #    ####    #    #   #  #  ####",
                  curses.color_pair(98))
    window.refresh()

def init_main_menu():
    
    window = curses.newwin(GAME_WINDOW_HEIGHT+TITLE_HEIGHT, TITLE_WIDTH, 0, 0)
    curses.init_pair(25, curses.COLOR_BLACK, curses.COLOR_WHITE)
    window.nodelay(True)
    window.keypad(1)
    return window

def init_game_window():
    """Create and return game window"""

    window = curses.newwin(GAME_WINDOW_HEIGHT, GAME_WINDOW_WIDTH, TITLE_HEIGHT, LEFT_MARGIN)
    window.nodelay(True)
    window.keypad(1)

    return window

def init_status_window():
    """Create and return status window"""

    window = curses.newwin(
        STATUS_WINDOW_HEIGHT, STATUS_WINDOW_WIDTH, TITLE_HEIGHT, GAME_WINDOW_WIDTH + 5)
    return window

def draw_scoreboard(window):
    window.clear()
    
    h, w = window.getmaxyx()
    
    X = []
    with open(BEST_SCORE_FILE_NAME+".txt", "r+") as file:            
        for line in file:
            X.append(line)
    if len(X) < 9:
        smaller = len(X)
    else:
        smaller = 9
    h1 = h//2 - smaller
    w1 = w//2
    string = "Top Scores:"
    window.addstr(h1, w1-len(string)//2, string)
    for i in range(0,smaller):
        window.addstr(i+h1+2, w1-len(str(i+1))-1, "#" + str(i+1) + " " + X[i])
    string = "Menu - ESC"
    window.addstr(smaller+h1+3, w1-len(string)//2, string)
    window.border()
    window.refresh()

def init_scoreboard_window():
    window = curses.newwin(GAME_WINDOW_HEIGHT+TITLE_HEIGHT, TITLE_WIDTH, 0, 0)
    curses.init_pair(25, curses.COLOR_BLACK, curses.COLOR_WHITE)
    window.nodelay(True)
    window.keypad(1)
    return window

def draw_game_window(window):
    """Draw game window"""

    window.border()

    # draw board
    for a in range(BOARD_HEIGHT):
        for b in range(BOARD_WIDTH):
            if game_board.board[a][b] == 1:
                window.addstr(a + 1, 2 * b + 1, "  ", curses.color_pair(96))
            else:
                # draw net
                window.addstr(a + 1, 2 * b + 1, " .", curses.color_pair(99))

    # draw current block
    for a in range(game_board.current_block.size()[0]):
        for b in range(game_board.current_block.size()[1]):
            if game_board.current_block.shape[a][b] == 1:
                x = 2 * game_board.current_block_pos[1] + 2 * b + 1
                y = game_board.current_block_pos[0] + a + 1
                window.addstr(y, x, "  ", curses.color_pair(
                    game_board.current_block.color))

    if game_board.is_game_over():
        go_title = " Game Over "
        ag_title = " Enter - play again "

        window.addstr(int(GAME_WINDOW_HEIGHT*.4), (GAME_WINDOW_WIDTH -
                      len(go_title))//2, go_title, curses.color_pair(95))
        window.addstr(int(GAME_WINDOW_HEIGHT*.5), (GAME_WINDOW_WIDTH -
                      len(ag_title))//2, ag_title, curses.color_pair(95))

    if pause:
        p_title = " Pause "
        window.addstr(int(GAME_WINDOW_HEIGHT * .4), (GAME_WINDOW_WIDTH - len(p_title)) // 2, p_title,
                      curses.color_pair(95))

    window.refresh()

def draw_status_window(window):
    """Draw status window"""

    if game_board.is_game_over():
        return

    # hack: avoid clearing (blinking)
    for row in range(1, STATUS_WINDOW_HEIGHT - 1):
        window.addstr(row, 2, "".rjust(STATUS_WINDOW_WIDTH - 3, " "))

    window.border()

    window.addstr(1, 2, f"Score: {game_board.score}")
    window.addstr(2, 2, f"Lines: {game_board.lines}")
    window.addstr(3, 2, f"Level: {game_board.level}")
    window.addstr(4, 2, f"Best Score:{game_board.best_score}")

    start_col = int(STATUS_WINDOW_WIDTH / 2 - game_board.next_block.size()[1])

    for row in range(game_board.next_block.size()[0]):
        for col in range(game_board.next_block.size()[1]):
            if game_board.next_block.shape[row][col] == 1:
                window.addstr(6 + row, start_col + 2 * col, "  ",
                              curses.color_pair(game_board.next_block.color))

    window.refresh()
    pass

def draw_help_window():
    """Draw help window"""

    window = curses.newwin(HELP_WINDOW_HEIGHT, HELP_WINDOW_WIDTH, TITLE_HEIGHT + STATUS_WINDOW_HEIGHT,
                           GAME_WINDOW_WIDTH + 5)

    window.border()

    window.addstr(1, 2, "Move    - ← ↓ →")
    window.addstr(2, 2, "Drop    - space")
    window.addstr(3, 2, "Rotate  - ↑")
    window.addstr(4, 2, "Pause   - p")
    window.addstr(5, 2, "Quit    - ESC")

    window.refresh()

def draw_title():
    """Draw title"""

    window = curses.newwin(TITLE_HEIGHT, TITLE_WIDTH-3, 1, 3)
    window.addstr(0, 4, "#####  ####  #####  ###    #   ####",
                  curses.color_pair(98))
    window.addstr(1, 4, "  #    #       #    #  #   #  #",
                  curses.color_pair(98))
    window.addstr(2, 4, "  #    ###     #    # #    #   ###",
                  curses.color_pair(98))
    window.addstr(3, 4, "  #    #       #    #  #   #      #",
                  curses.color_pair(98))
    window.addstr(4, 4, "  #    ####    #    #   #  #  ####",
                  curses.color_pair(98))
    window.refresh()

if __name__ == "__main__":
    print("Choose for a tetris version you'd like to play")
    print("[0] for console version")    
    print("[1] for graphical version")
    print("Any other key to exit")
    TETRIS_TYPE = readchar.readchar()
    if (TETRIS_TYPE == '0'):
        print("Starting tetris in console mode...")
        os.system('mode con: cols=50 lines=28')
        try:
            while inprogram:    
                current_row = 0
                scr = curses.initscr()
                curses.beep()
                curses.noecho()
                curses.cbreak()
                curses.start_color()
                curses.curs_set(0)
                init_colors()
                menu_window = init_main_menu()
                while inmenu:
                    draw_menu(menu_window, current_row)
                    draw_menu_title(menu_window)
                    key = menu_window.getch()
                    if key == curses.KEY_UP and current_row > 0:
                        current_row -= 1
                    elif key == curses.KEY_DOWN and current_row < len(menu)-1:
                        current_row += 1
                    elif ((key == curses.KEY_LEFT) or (key in [10, 13])) and (current_row == 1):
                        if menulevel >=2:
                            menulevel -= 1
                    elif ((key == curses.KEY_RIGHT) or (key in [10, 13])) and (current_row == 1):
                        menulevel += 1
                    elif key == curses.KEY_ENTER or key in [10, 13]:
                        if current_row == 0:
                            game_board = board.Board(BOARD_HEIGHT, BOARD_WIDTH)
                            game_board.start(menulevel)
                            old_score = game_board.score
                            ingame = True
                            menu_window.clear()
                            menu_window.refresh()
                            draw_title()
                            draw_help_window()
                            game_window = init_game_window()
                            status_window = init_status_window()
                            draw_game_window(game_window)
                            draw_status_window(status_window)
                            start = time.time()
                            while ingame:
                                key_event = game_window.getch()
                                # hack: redraw it on resize
                                if key_event == curses.KEY_RESIZE:
                                    draw_title()
                                    draw_help_window()
                                    draw_game_window(game_window)
                                if key_event == 27:
                                    ingame = False  
                                if not game_board.is_game_over():
                                    if not pause:
                                        if time.time() - start >= 1 / game_board.level:
                                            game_board.move_block("down")
                                            start = time.time()
                                        if key_event == curses.KEY_UP:
                                            game_board.rotate_block()
                                        elif key_event == curses.KEY_DOWN:
                                            game_board.move_block("down")
                                        elif key_event == curses.KEY_LEFT:
                                            game_board.move_block("left")
                                        elif key_event == curses.KEY_RIGHT:
                                            game_board.move_block("right")
                                        elif key_event == ord(" "):
                                            game_board.drop()
                                    if key_event == ord("p"):
                                        pause = not pause
                                        game_window.nodelay(not pause)
                                else:
                                    curses.beep()
                                    game_window.nodelay(False)
                                    if key_event == ord("\n"):
                                        game_board.start(menulevel)
                                        game_window.nodelay(True)
                                draw_game_window(game_window)
                                if old_score != game_board.score:
                                    draw_status_window(status_window)
                                    old_score = game_board.score
                        if current_row == 1:
                            menulevel += 1
                        if current_row == 2:
                            menu_window.clear()
                            menu_window.refresh()
                            inscoreboard = True
                            scoreboard_window = init_scoreboard_window()
                            while inscoreboard:
                                draw_scoreboard(scoreboard_window)
                                key = scoreboard_window.getch()
                                if key == 27:
                                    inscoreboard = False
                        if current_row == len(menu)-1:
                            inprogram = False
                            break
                    elif key == 27:
                        inprogram = False
                        break
        finally:
            curses.endwin()
    if (TETRIS_TYPE == '1'):
        print("Starting tetris in graphical mode...")
        graphical.game()
    sys.exit()
