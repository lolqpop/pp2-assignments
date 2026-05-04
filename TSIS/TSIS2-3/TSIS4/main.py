import pygame, sys
from game import SnakeGame, load_settings, save_settings, WIDTH, HEIGHT
from db import create_tables, get_top_10, get_personal_best

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

WHITE=(255,255,255); BLACK=(0,0,0); GREEN=(0,200,0); RED=(200,0,0); GRAY=(180,180,180)

font       = pygame.font.SysFont("Verdana", 24)
big_font   = pygame.font.SysFont("Verdana", 48)
small_font = pygame.font.SysFont("Verdana", 18)

settings = load_settings()

def draw_text(text, x, y, color=BLACK, f=font):
    screen.blit(f.render(text,True,color),(x,y))

def button(text, x, y, w, h):
    rect = pygame.Rect(x,y,w,h)
    pygame.draw.rect(screen,GRAY,rect)
    pygame.draw.rect(screen,BLACK,rect,2)
    lbl = font.render(text,True,BLACK)
    screen.blit(lbl, lbl.get_rect(center=rect.center))
    return rect

def events():
    evs = pygame.event.get()
    for e in evs:
        if e.type==pygame.QUIT: pygame.quit(); sys.exit()
    return evs

def username_screen():
    name = ""
    while True:
        screen.fill(WHITE)
        draw_text("Enter Username",210,160,BLACK,big_font)
        draw_text(name+"|",300,270)
        draw_text("Press ENTER to continue",260,350,BLACK,small_font)
        pygame.display.update()
        for e in events():
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_RETURN and name.strip(): return name.strip()
                elif e.key==pygame.K_BACKSPACE: name=name[:-1]
                elif len(name)<15 and e.unicode.isprintable(): name+=e.unicode


def game_over_screen(username, score, level):
    best = get_personal_best(username)   # актуальный рекорд после игры
    while True:
        screen.fill(WHITE)
        draw_text("Game Over",250,100,RED,big_font)
        draw_text(f"Score: {score}",320,210)
        draw_text(f"Level: {level}",320,250)
        draw_text(f"Personal Best: {best}",280,290,BLACK,small_font)
        retry_btn = button("Retry",    300,370,200,50)
        menu_btn  = button("Main Menu",300,440,200,50)
        pygame.display.update()
        for e in events():
            if e.type==pygame.MOUSEBUTTONDOWN:
                if retry_btn.collidepoint(e.pos):
                    score,level,_ = SnakeGame(screen,username).run()
                    best = get_personal_best(username)
                elif menu_btn.collidepoint(e.pos):
                    return

def leaderboard_screen():
    while True:
        screen.fill(WHITE)
        draw_text("Leaderboard",250,50,BLACK,big_font)
        draw_text("Rank  Name        Score  Level  Date",120,100,BLACK,small_font)
        try: rows = get_top_10()
        except: draw_text("Database error",300,250,RED); rows=[]
        y = 130
        for i,(uname,sc,lv,played_at) in enumerate(rows,1):
            draw_text(f"{i}. {uname[:10]:10} {sc:5} {lv:5} {str(played_at).split('.')[0]}",100,y,BLACK,small_font)
            y+=35
        back_btn = button("Back",300,520,200,50)
        pygame.display.update()
        for e in events():
            if e.type==pygame.MOUSEBUTTONDOWN and back_btn.collidepoint(e.pos): return


def settings_screen():
    global settings
    colors = [[0,200,0],[0,100,255],[200,0,0],[240,220,0]]
    while True:
        screen.fill(WHITE)
        draw_text("Settings",290,80,BLACK,big_font)
        grid_btn  = button(f"Grid: {'ON' if settings['grid'] else 'OFF'}",  270,190,260,50)
        sound_btn = button(f"Sound: {'ON' if settings['sound'] else 'OFF'}",270,260,260,50)
        color_btn = button("Change Snake Color",                             270,330,260,50)
        save_btn  = button("Save & Back",                                    270,430,260,50)
        pygame.draw.rect(screen,settings["snake_color"],(560,340,40,40))
        pygame.display.update()
        for e in events():
            if e.type==pygame.MOUSEBUTTONDOWN:
                if grid_btn.collidepoint(e.pos):  settings["grid"]=not settings["grid"]
                elif sound_btn.collidepoint(e.pos): settings["sound"]=not settings["sound"]
                elif color_btn.collidepoint(e.pos):
                    idx = colors.index(settings["snake_color"]) if settings["snake_color"] in colors else 0
                    settings["snake_color"] = colors[(idx+1)%len(colors)]
                elif save_btn.collidepoint(e.pos):
                    save_settings(settings); return


def main_menu():
    username = username_screen()
    while True:
        screen.fill(WHITE)
        draw_text("Snake Game",240,80,GREEN,big_font)
        draw_text(f"Player: {username}",300,150,BLACK,small_font)
        play_btn = button("Play",       300,220,200,50)
        lb_btn   = button("Leaderboard",300,290,200,50)
        set_btn  = button("Settings",   300,360,200,50)
        quit_btn = button("Quit",       300,430,200,50)
        pygame.display.update()
        for e in events():
            if e.type==pygame.MOUSEBUTTONDOWN:
                if play_btn.collidepoint(e.pos):
                    score,level,_ = SnakeGame(screen,username).run()
                    game_over_screen(username,score,level)
                elif lb_btn.collidepoint(e.pos):  leaderboard_screen()
                elif set_btn.collidepoint(e.pos): settings_screen()
                elif quit_btn.collidepoint(e.pos): pygame.quit(); sys.exit()

if __name__=="__main__":
    create_tables()
    main_menu()