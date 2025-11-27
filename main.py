import pygame
import sys
from settings import *
from sprites import Cloud, BackgroundMountain
from game import run_game
from editor import run_editor
from ui import Button
from utils import get_map_list, create_default_map
from settings_menu import SettingsMenu

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pixel Forts Battle")
    clock = pygame.time.Clock()
    
    clouds = [Cloud() for _ in range(10)]
    mountains = [
        BackgroundMountain(0, 150, (100, 100, 120)),
        BackgroundMountain(200, 220, (80, 80, 100)),
        BackgroundMountain(450, 180, (90, 90, 110)),
        BackgroundMountain(700, 250, (75, 75, 95)),
        BackgroundMountain(950, 190, (85, 85, 105)),
    ]
    
    btn_play = Button(SCREEN_WIDTH//2 - 120, 220, 240, 50, "PLAY GAME", (50, 150, 50), (70, 200, 70))
    btn_editor = Button(SCREEN_WIDTH//2 - 120, 290, 240, 50, "MAP EDITOR", (50, 50, 150), (70, 70, 200))
    btn_settings = Button(SCREEN_WIDTH//2 - 120, 360, 240, 50, "SETTINGS", (150, 150, 50), (200, 200, 70))
    btn_quit = Button(SCREEN_WIDTH//2 - 120, 430, 240, 50, "QUIT", (150, 50, 50), (200, 70, 70))
    buttons = [btn_play, btn_editor, btn_settings, btn_quit]
    
    selected_map = None
    state = "MENU"
    running = True
    
    while running:
        map_list = get_map_list()
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if state == "MENU":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if btn_play.is_clicked(mouse_pos, True):
                        result = run_game(screen, clock, selected_map)
                        if result == "QUIT":
                            running = False
                    elif btn_editor.is_clicked(mouse_pos, True):
                        run_editor(screen, clock, selected_map)
                    elif btn_settings.is_clicked(mouse_pos, True):
                        # Open settings menu
                        settings_menu = SettingsMenu()
                        state = "SETTINGS"
                    elif btn_quit.is_clicked(mouse_pos, True):
                        running = False
                    for i, map_name in enumerate(map_list[:6]):
                        map_rect = pygame.Rect(SCREEN_WIDTH//2 - 130, 445 + i * 25, 260, 22)
                        if map_rect.collidepoint(mouse_pos):
                            selected_map = map_name
            elif state == "SETTINGS":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if settings_menu.save_btn.is_clicked(mouse_pos, True):
                        if settings_menu.save_settings():
                            state = "MENU"
                    elif settings_menu.cancel_btn.is_clicked(mouse_pos, True):
                        settings_menu.cancel_changes()
                        state = "MENU"
                settings_menu.handle_event(event)
        
        if state == "MENU":
            for btn in buttons:
                btn.update(mouse_pos)
            from ui import draw_menu
            draw_menu(screen, clouds, mountains, buttons, selected_map, map_list)
        elif state == "SETTINGS":
            settings_menu.update(mouse_pos)
            settings_menu.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()