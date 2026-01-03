import pygame
import random
import sys

pygame.init()
WIDTH, HEIGHT = 900,800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Card Game")

# Colors
BACKGROUND = (25, 25, 40)
CARD_BACK = (30, 136, 229)
CARD_FRONT = (240, 240, 240)
RED = (255, 50, 100)
WHITE = (255, 255, 255)
GREEN = (50, 255, 150)
BLUE = (50, 150, 255)
YELLOW = (255, 235, 50)
PURPLE = (180, 70, 230)
ORANGE = (255, 150, 50)
PINK = (255, 100, 180)

CARD_COLORS = [RED, GREEN, BLUE, YELLOW, PURPLE, ORANGE, PINK]
SYMBOLS = ["★", "❤", "♦", "♠", "♣", "♫", "☀", "☁", "⚡", "❄"]

class Card:
    def __init__(self, x, y, symbol, color):
        self.x = x
        self.y = y
        self.width = 100
        self.height = 140
        self.symbol = symbol
        self.color = color
        self.is_flipped = False
        self.is_matched = False
        self.flip_animation = 0
        self.flip_speed = 0.1
        
    def draw(self, surface):
        if self.is_matched:
            return
            
        
        pygame.draw.rect(surface, (0, 0, 0, 100), 
                        (self.x + 5, self.y + 5, self.width, self.height), 
                        border_radius=10)
        
        card_color = CARD_FRONT if self.is_flipped else CARD_BACK
        pygame.draw.rect(surface, card_color, 
                        (self.x, self.y, self.width, self.height), 
                        border_radius=10)
        
        
        border_color = self.color if self.is_flipped else (200, 200, 255)
        pygame.draw.rect(surface, border_color, 
                        (self.x, self.y, self.width, self.height), 
                        3, border_radius=10)
        
        if self.is_flipped:
            
            font = pygame.font.Font(None, 60)
            text = font.render(self.symbol, True, self.color)
            surface.blit(text, (self.x + self.width//2 - text.get_width()//2,
                              self.y + self.height//2 - text.get_height()//2))
            
            
            small_font = pygame.font.Font(None, 30)
            corner_text = small_font.render(self.symbol, True, self.color)
            surface.blit(corner_text, (self.x + 10, self.y + 10))
            surface.blit(corner_text, (self.x + self.width - 30, self.y + self.height - 40))
        else:
            
            pattern_color = (20, 80, 180)
            for i in range(5):
                pygame.draw.circle(surface, pattern_color,
                                 (self.x + 20 + i*15, self.y + 20), 8)
                pygame.draw.circle(surface, pattern_color,
                                 (self.x + self.width - 20 - i*15, self.y + self.height - 20), 8)
            
            
            font = pygame.font.Font(None, 70)
            text = font.render("?", True, (255, 255, 255))
            surface.blit(text, (self.x + self.width//2 - text.get_width()//2,
                              self.y + self.height//2 - text.get_height()//2))
    
    def update(self):
        if self.is_flipped and self.flip_animation < 1:
            self.flip_animation += self.flip_speed
        elif not self.is_flipped and self.flip_animation > 0:
            self.flip_animation -= self.flip_speed
            
    def is_clicked(self, pos):
        return (self.x <= pos[0] <= self.x + self.width and
                self.y <= pos[1] <= self.y + self.height and
                not self.is_matched)
    
    def flip(self):
        self.is_flipped = not self.is_flipped

class Game:
    def __init__(self):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 28)
        self.cards = []
        self.selected_cards = []
        self.moves = 0
        self.matches = 0
        self.game_won = False
        self.time_elapsed = 0
        self.create_board()
        
    def create_board(self):
        self.cards = []
        self.selected_cards = []
        self.moves = 0
        self.matches = 0
        self.game_won = False
        self.time_elapsed = 0
        
        
        pairs = []
        for i in range(8):  
            symbol = SYMBOLS[i % len(SYMBOLS)]
            color = CARD_COLORS[i % len(CARD_COLORS)]
            pairs.extend([(symbol, color), (symbol, color)])
            
        random.shuffle(pairs)
        
        
        for i in range(16):
            row = i // 4
            col = i % 4
            x = 150 + col * 130
            y = 100 + row * 160
            symbol, color = pairs[i]
            self.cards.append(Card(x, y, symbol, color))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                    
                if event.key == pygame.K_r:
                    self.create_board()
                    
                if self.game_won and event.key == pygame.K_SPACE:
                    self.create_board()
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not self.game_won:  
                    pos = pygame.mouse.get_pos()
                    for card in self.cards:
                        if card.is_clicked(pos) and not card.is_flipped:
                            if len(self.selected_cards) < 2:
                                card.flip()
                                self.selected_cards.append(card)
                                self.moves += 1
                                break
    
    def update(self):
        if not self.game_won:
            self.time_elapsed += 1/60  
            
        for card in self.cards:
            card.update()
            
        
        if len(self.selected_cards) == 2:
            card1, card2 = self.selected_cards
            if card1.symbol == card2.symbol:
                
                card1.is_matched = True
                card2.is_matched = True
                self.matches += 1
                self.selected_cards = []
                
                
                if self.matches == 8:
                    self.game_won = True
            else:
                
                pygame.time.wait(800)
                card1.flip()
                card2.flip()
                self.selected_cards = []
    
    def draw(self):
        self.screen.fill(BACKGROUND)
        
        
        title = self.font.render("Memory Card Game", True, (255, 255, 255))
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 20))
        
       
        for card in self.cards:
            card.draw(self.screen)
        
        
        stats_bg = pygame.Rect(20, 20, 120, 120)
        pygame.draw.rect(self.screen, (40, 40, 60), stats_bg, border_radius=10)
        pygame.draw.rect(self.screen, (100, 100, 180), stats_bg, 2, border_radius=10)
        
        moves_text = self.small_font.render(f"Moves: {self.moves}", True, WHITE)
        self.screen.blit(moves_text, (40, 40))
        
        matches_text = self.small_font.render(f"Matches: {self.matches}/8", True, GREEN)
        self.screen.blit(matches_text, (40, 70))
        
        time_text = self.small_font.render(f"Time: {int(self.time_elapsed)}s", True, BLUE)
        self.screen.blit(time_text, (40, 100))
        
        
        controls = [
            "Click cards to flip",
            "Find matching pairs",
            "R: New Game",
            "ESC: Quit"
        ]
        
        for i, text in enumerate(controls):
            control = self.small_font.render(text, True, WHITE)
            self.screen.blit(control, (WIDTH - control.get_width() - 20, 40 + i * 30))
        
        
        if self.game_won:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))
            
            win_text = self.font.render("YOU WIN!", True, YELLOW)
            self.screen.blit(win_text, (WIDTH//2 - win_text.get_width()//2, HEIGHT//2 - 80))
            
            stats = self.small_font.render(
                f"Moves: {self.moves} | Time: {int(self.time_elapsed)} seconds", 
                True, WHITE)
            self.screen.blit(stats, (WIDTH//2 - stats.get_width()//2, HEIGHT//2 - 20))
            
            restart = self.small_font.render("Press SPACE for new game or R to restart", 
                                           True, GREEN)
            self.screen.blit(restart, (WIDTH//2 - restart.get_width()//2, HEIGHT//2 + 40))
    
    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()