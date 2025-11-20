import pygame
from States.Core.StateClass import State


class SettingsState(State):
    def __init__(self, nextState=None):
        super().__init__(nextState)
        self.returnState = nextState

        self.menuSurface = pygame.Surface((400, 200), pygame.SRCALPHA)
        self.menuSurface.fill((50, 50, 50, 200))

        self.stackSurface = pygame.Surface((900, 600), pygame.SRCALPHA)
        self.tvOverlay = pygame.image.load('Graphics/Backgrounds/CRT.png').convert_alpha()
        self.tvOverlay = pygame.transform.scale(self.tvOverlay, (1300, 750))

        # Font
        self.font = pygame.font.Font("Graphics/Text/m6x11.ttf", 28)

        # High Contrast Card toggle
        self.highContrast = False  # default
        self.toggleRect = pygame.Rect(100, 80, 200, 50)  # rectangle for toggle button

        # Back button
        self.backRect = pygame.Rect(150, 150, 100, 40)

    def update(self):
        self.draw()

    def draw(self):
        if hasattr(State, 'screenshot') and State.screenshot:
            self.screen.blit(State.screenshot, (0, 0))


        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))  # adjust alpha for more/less transparency
        self.screen.blit(overlay, (0, 0))

        menuColor = (50, 50, 50, 200)  # you already use SRCALPHA
        pygame.draw.rect(self.menuSurface, menuColor, self.menuSurface.get_rect(), border_radius=10)

        toggleColor = (0, 200, 0) if self.highContrast else (200, 0, 0)
        pygame.draw.rect(self.menuSurface, toggleColor, self.toggleRect)
        textColor = (255, 255, 255)
        toggleText = self.font.render(f"High Contrast: {'ON' if self.highContrast else 'OFF'}", True, textColor)
        toggleTextRect = toggleText.get_rect(center=self.toggleRect.center)
        self.menuSurface.blit(toggleText, toggleTextRect)

        pygame.draw.rect(self.menuSurface, (80, 80, 80), self.backRect)
        backText = self.font.render("Back", True, textColor)
        backTextRect = backText.get_rect(center=self.backRect.center)
        self.menuSurface.blit(backText, backTextRect)

        self.screen.blit(self.menuSurface, (450, 250)) # center-ish
        self.screen.blit(self.tvOverlay, (0, 0))



    def userInput(self, events):
        if events.type == pygame.QUIT:
            self.isFinished = True
            self.nextState = "GameState"

        elif events.type == pygame.MOUSEBUTTONDOWN:
            # Toggle high contrast
            if self.toggleRect.collidepoint(events.pos[0] - 450, events.pos[1] - 250):
                self.highContrast = not self.highContrast

            # Go back
            elif self.backRect.collidepoint(events.pos[0] - 450, events.pos[1] - 250):
                self.isFinished = True
                self.nextState = "GameState"
