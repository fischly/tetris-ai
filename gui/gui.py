import pygame

from tetris.Piece import Piece
import gui.color as color
from gui.sprites.background import Background


WIN_SIZE = (800, 680)

FIELD_UPPER_MARGIN = 20
FIELD_LEFT_MARGIN = 240



FIELD_BACKGROUND_ALPHA = 178

CELL_SIZE = 32
CELL_GAP = 2

FONT_SIZE = 16

colors = [color.PURPLE, color.ORANGE, color.BLUE, color.YELLOW, color.CYAN, color.GREEN, color.RED]


# derived constants
FIELD_BACKGROUND_POS = (WIN_SIZE[0] / 2 - (CELL_SIZE * 10 + FIELD_UPPER_MARGIN * 2) / 2, 0)
QUEUE_BACKGROUND_POS = (WIN_SIZE[0] / 2 + (CELL_SIZE * 10 + FIELD_UPPER_MARGIN * 2) / 2 + FIELD_UPPER_MARGIN, FIELD_UPPER_MARGIN)

class Gui:
    def __init__(self, shape=(20, 10), sleep=66):
        pygame.init()
    
        self.shape = shape
        self.sleep = sleep
        
        self.win = pygame.display.set_mode(WIN_SIZE)
        pygame.display.set_caption('tetris_ai')
        
        self.background = Background(WIN_SIZE)
        
        self.grid_background = pygame.Surface((CELL_SIZE * 10 + FIELD_UPPER_MARGIN * 2, WIN_SIZE[1]))
        self.grid_background.set_alpha(FIELD_BACKGROUND_ALPHA)
        self.grid_background.fill((0, 0, 0))
        
        self.queue_background = pygame.Surface((CELL_SIZE * 4 + CELL_GAP + FIELD_UPPER_MARGIN * 2, (CELL_SIZE * 2 + CELL_GAP) * 5 + 6 * FIELD_UPPER_MARGIN))
        self.queue_background.set_alpha(FIELD_BACKGROUND_ALPHA)
        self.queue_background.fill((0, 0, 0))
        
        self.sound_quad = pygame.mixer.Sound('gui/quad.wav')
        self.sound_tspin = pygame.mixer.Sound('gui/tspin.wav')
        self.sound_clear = pygame.mixer.Sound('gui/clear.wav')
        
    
    def render_field(self, field):
        for x, row in enumerate(field):
            for y, cell in enumerate(row):
                
                if cell == -1:
                    continue
                
                render_x = y * CELL_SIZE + CELL_GAP + FIELD_LEFT_MARGIN
                render_y = x * CELL_SIZE + CELL_GAP + FIELD_UPPER_MARGIN
                
                rect = pygame.Rect(render_x, render_y, CELL_SIZE - 2 * CELL_GAP, CELL_SIZE - 2 * CELL_GAP)
                pygame.draw.rect(self.win, colors[int(cell)], rect)
    
#     def render_piece(self, piece):
#         piece_color = colors[piece.pdata.piece_id]
        
        
#         for x, y in piece.pdata.data[piece.rot]:            
#             piece_x = x + piece.pos[0]
#             piece_y = y + piece.pos[1]
            
#             render_x = piece_y * CELL_SIZE + CELL_GAP + FIELD_LEFT_MARGIN
#             render_y = piece_x * CELL_SIZE + CELL_GAP + FIELD_UPPER_MARGIN
            
#             piece_rect = pygame.Rect(render_x, render_y, CELL_SIZE - 2 * CELL_GAP, CELL_SIZE - 2 * CELL_GAP)
        
#             pygame.draw.rect(self.win, piece_color, piece_rect)
    
    def _render_piece(self, piece, pos):
        piece_color = colors[piece.pdata.piece_id]
        
        for x, y in piece.pdata.data[piece.rot]:
            render_x = y * CELL_SIZE + CELL_GAP + pos[1]
            render_y = x * CELL_SIZE + CELL_GAP + pos[0]
            
            piece_rect = pygame.Rect(render_x, render_y, CELL_SIZE - 2 * CELL_GAP, CELL_SIZE - 2 * CELL_GAP)
            
            pygame.draw.rect(self.win, piece_color, piece_rect)
            
    def render_piece(self, piece): 
        px = piece.pos[0] * CELL_SIZE + FIELD_UPPER_MARGIN
        py = piece.pos[1] * CELL_SIZE + FIELD_LEFT_MARGIN
        
        self._render_piece(piece, (px, py))
    
    def render_queue(self, queue):
        
        for idx, piece in enumerate(queue):
            px = QUEUE_BACKGROUND_POS[1] + FIELD_UPPER_MARGIN * (idx + 1) + CELL_SIZE * 2 * idx
            py = QUEUE_BACKGROUND_POS[0] + FIELD_UPPER_MARGIN
            
            self._render_piece(Piece(piece), (px, py))
            
    def draw(self, field, piece, queue):
        try:
            pygame.time.delay(self.sleep)
        except KeyboardInterrupt:
            pass

        self.win.fill(color.BLACK)
        self.background.draw(self.win)
        
        self.win.blit(self.grid_background, FIELD_BACKGROUND_POS)
        self.win.blit(self.queue_background, QUEUE_BACKGROUND_POS)
        
        self.render_field(field)
        self.render_queue(queue)
        self.render_piece(piece)

        pygame.display.update()
    
    def play_sound_quad(self):
        pygame.mixer.Sound.play(self.sound_quad)
    
    def play_sound_tspin(self):
        pygame.mixer.Sound.play(self.sound_tspin)
        
    def play_sound_clear(self):
        pygame.mixer.Sound.play(self.sound_clear)
    