import pygame
from settings import *
from ui import Button, InputBox

class SettingsMenu:
    def __init__(self):
        self.health_input = InputBox(SCREEN_WIDTH//2 - 100, 150, 200, 40, str(INITIAL_PLAYER_HEALTH))
        self.ammo_input = InputBox(SCREEN_WIDTH//2 - 100, 220, 200, 40, str(INITIAL_PLAYER_AMMO))
        self.speed_input = InputBox(SCREEN_WIDTH//2 - 100, 290, 200, 40, str(PLAYER_SPEED))
        self.rotation_speed_input = InputBox(SCREEN_WIDTH//2 - 100, 360, 200, 40, str(CANNON_ROTATION_SPEED))
        self.entry_radius_input = InputBox(SCREEN_WIDTH//2 - 100, 430, 200, 40, str(CANNON_ENTRY_RADIUS))
        
        self.save_btn = Button(SCREEN_WIDTH//2 - 120, 520, 240, 50, "Save Settings", (50, 150, 50), (70, 200, 70))
        self.cancel_btn = Button(SCREEN_WIDTH//2 - 120, 580, 240, 50, "Cancel", (150, 50, 50), (200, 70, 70))
        
        self.inputs = [self.health_input, self.ammo_input, self.speed_input, 
                      self.rotation_speed_input, self.entry_radius_input]
        
        # Store original values for cancel
        self.original_values = {
            'health': INITIAL_PLAYER_HEALTH,
            'ammo': INITIAL_PLAYER_AMMO,
            'speed': PLAYER_SPEED,
            'rotation_speed': CANNON_ROTATION_SPEED,
            'entry_radius': CANNON_ENTRY_RADIUS
        }
    
    def handle_event(self, event):
        for input_box in self.inputs:
            result = input_box.handle_event(event)
            if result:
                return True
        return False
    
    def update(self, mouse_pos):
        self.save_btn.update(mouse_pos)
        self.cancel_btn.update(mouse_pos)
    
    def draw(self, surface):
        # Draw background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(overlay, (0, 0, 0, 200), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        surface.blit(overlay, (0, 0))
        
        # Draw settings panel
        panel = pygame.Surface((600, 500), pygame.SRCALPHA)
        pygame.draw.rect(panel, (30, 30, 50), (0, 0, 600, 500), border_radius=15)
        pygame.draw.rect(panel, GOLD, (0, 0, 600, 500), 3, border_radius=15)
        surface.blit(panel, (SCREEN_WIDTH//2 - 300, 100))
        
        # Draw title
        title = font_large.render("GAME SETTINGS", True, GOLD)
        surface.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 110))
        
        # Draw labels and inputs
        labels = [
            "Initial Health:",
            "Initial Ammo:",
            "Player Speed:",
            "Cannon Rotation Speed:",
            "Cannon Entry Radius:"
        ]
        
        y_positions = [150, 220, 290, 360, 430]
        
        for i, (label, y) in enumerate(zip(labels, y_positions)):
            label_surf = font_medium.render(label, True, WHITE)
            surface.blit(label_surf, (SCREEN_WIDTH//2 - 280, y + 10))
            self.inputs[i].draw(surface)
        
        # Draw buttons
        self.save_btn.draw(surface)
        self.cancel_btn.draw(surface)
        
        # Draw hint
        hint = font_small.render("Click outside input boxes to save values", True, (180, 180, 180))
        surface.blit(hint, (SCREEN_WIDTH//2 - hint.get_width()//2, 650))
    
    def save_settings(self):
        """Save the settings to the settings module"""
        global INITIAL_PLAYER_HEALTH, INITIAL_PLAYER_AMMO, PLAYER_SPEED, CANNON_ROTATION_SPEED, CANNON_ENTRY_RADIUS
        
        try:
            # Update the global variables
            INITIAL_PLAYER_HEALTH = int(self.health_input.text)
            INITIAL_PLAYER_AMMO = int(self.ammo_input.text)
            PLAYER_SPEED = float(self.speed_input.text)
            CANNON_ROTATION_SPEED = float(self.rotation_speed_input.text)
            CANNON_ENTRY_RADIUS = float(self.entry_radius_input.text)
            
            # Write the changes to the settings file
            self._write_settings_to_file()
            return True
        except ValueError:
            return False
    
    def _write_settings_to_file(self):
        """Write the current settings to the settings.py file"""
        import os
        settings_file_path = os.path.join(os.path.dirname(__file__), 'settings.py')
        
        # Read the current settings file
        with open(settings_file_path, 'r') as f:
            lines = f.readlines()
        
        # Find and replace the settings values
        new_lines = []
        for line in lines:
            if line.strip().startswith('INITIAL_PLAYER_HEALTH ='):
                new_lines.append(f'INITIAL_PLAYER_HEALTH = {INITIAL_PLAYER_HEALTH}\n')
            elif line.strip().startswith('INITIAL_PLAYER_AMMO ='):
                new_lines.append(f'INITIAL_PLAYER_AMMO = {INITIAL_PLAYER_AMMO}\n')
            elif line.strip().startswith('PLAYER_SPEED ='):
                new_lines.append(f'PLAYER_SPEED = {PLAYER_SPEED}\n')
            elif line.strip().startswith('CANNON_ROTATION_SPEED ='):
                new_lines.append(f'CANNON_ROTATION_SPEED = {CANNON_ROTATION_SPEED}\n')
            elif line.strip().startswith('CANNON_ENTRY_RADIUS ='):
                new_lines.append(f'CANNON_ENTRY_RADIUS = {CANNON_ENTRY_RADIUS}\n')
            else:
                new_lines.append(line)
        
        # Write the updated content back to the file
        with open(settings_file_path, 'w') as f:
            f.writelines(new_lines)
    
    def cancel_changes(self):
        """Restore original values"""
        global INITIAL_PLAYER_HEALTH, INITIAL_PLAYER_AMMO, PLAYER_SPEED, CANNON_ROTATION_SPEED, CANNON_ENTRY_RADIUS
        
        INITIAL_PLAYER_HEALTH = self.original_values['health']
        INITIAL_PLAYER_AMMO = self.original_values['ammo']
        PLAYER_SPEED = self.original_values['speed']
        CANNON_ROTATION_SPEED = self.original_values['rotation_speed']
        CANNON_ENTRY_RADIUS = self.original_values['entry_radius']
        
        # Update input boxes with original values
        self.health_input.text = str(INITIAL_PLAYER_HEALTH)
        self.ammo_input.text = str(INITIAL_PLAYER_AMMO)
        self.speed_input.text = str(PLAYER_SPEED)
        self.rotation_speed_input.text = str(CANNON_ROTATION_SPEED)
        self.entry_radius_input.text = str(CANNON_ENTRY_RADIUS)