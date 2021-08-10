from checkers.constants import COLOR
import pygame
class Button:  #class to handle button functionality
    def __init__(self, text,  pos, font, color=COLOR.BLACK, func = None): #constructor 
        self.x, self.y = pos 
        self.origin_color = color
        self.font = pygame.font.SysFont("Arial", font) #font to use
        self.text = self.font.render(text, 1, COLOR.WHITE)
        if func != None: #set onclick function, use change color to draw
            self.func = func
        self.change_color(color)

 
    def change_color(self, color):
        self.size = self.text.get_size() #get text size
        self.surface = pygame.Surface(self.size) #get surface
        self.surface.fill(color) #fill with color
        self.surface.blit(self.text, (0, 0)) #draw text 
        self.color = color #set color (update color stored)
        self.border_rect = pygame.Rect(self.x-12, self.y-7, self.size[0]+24, self.size[1]+14) #make rect for border
        self.rect = pygame.Rect(self.x-10, self.y-5, self.size[0]+20, self.size[1]+10) #rect for inside
 
    def draw(self,win):
        pygame.draw.rect(win,COLOR.DARK_GREY,(self.border_rect)) #draw outline
        pygame.draw.rect(win,self.color,(self.rect)) #draw inside fill
        win.blit(self.surface, (self.x, self.y)) #draw text
 
    def click(self, event): #check if clicked
        x, y = pygame.mouse.get_pos() #get x,y
        if event.type == pygame.MOUSEBUTTONDOWN: #if button down
            if pygame.mouse.get_pressed()[0]: #if left click
                if self.rect.collidepoint(x, y): #if click inside rect 
                    self.func() #run stored function
    


 
 

