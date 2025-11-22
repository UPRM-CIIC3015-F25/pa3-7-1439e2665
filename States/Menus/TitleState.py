import pygame
from States.Core.StateClass import State
import math
from moviepy import VideoFileClip, vfx
import sys
import os


class StartState(State):
    def __init__(self, nextState: str = ""):
        super().__init__(nextState)
        # ----------------------------- Background --------------------------------
        # ----------------------------- Video Background --------------------------------

        self.video_path = "Graphics/Backgrounds/introBackground.mp4"
        self.clip = VideoFileClip(self.video_path).resized((1300, 750))

        # Create a frame generator and initialize first frame
        self.frame_generator = self.clip.iter_frames(fps=30, dtype='uint8')
        self.current_frame = next(self.frame_generator)

        # For blitting
        self.backgroundRect = pygame.Rect(0, 0, 1300, 750)

        self.clock = pygame.time.Clock()
        self.running = True

        # ----------------------------- Title -------------------------------------
        self.titleImage = pygame.image.load('Graphics/Backgrounds/balatroTitle.png')
        original_width, original_height = self.titleImage.get_size()
        scale_factor = 700 / original_width
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)
        self.baseTitleSize = (new_width, new_height)
        self.title = pygame.transform.scale(self.titleImage, self.baseTitleSize)
        self.titleRect = self.title.get_rect(midtop=(650, 30))

        # Breathing animation variables for title
        self.breathAmplitude = 10  # pixels (not directly used, just for reference)
        self.breathSpeed = 0.005   # smaller = slower breathing
        self.breathTime = 0

        # ----------------------------- Text --------------------------------------
        self.textFont1 = pygame.font.Font('Graphics/Text/m6x11.ttf', 50)
        self.textFont2 = pygame.font.Font('Graphics/Text/m6x11.ttf', 40)
        self.textPlay = self.textFont1.render("PLAY", True, 'white')
        self.textInstructions = self.textFont2.render("HELP", True, 'white')
        self.textSettings = self.textFont2.render("SETTINGS", True, 'white')
        self.textQuit = self.textFont1.render("QUIT", True, 'white')

        # ----------------------------- Title Card --------------------------------
        self.titleCardImage = pygame.image.load('Graphics/Backgrounds/titleCard.png')
        self.baseCardSize = (150, 220)
        self.titleCard = pygame.transform.scale(self.titleCardImage, self.baseCardSize)
        self.titleCardRect = self.titleCard.get_rect(topleft=(575, 150))
        self.mouseDragging = False
        self.isMouseInCard = False

        # ----------------------------- button Bar --------------------------------
        bar_width = 800
        self.buttonBar = pygame.Rect(self.titleRect.x - (bar_width - 690) // 2, 540, bar_width, 120)
        self.buttonBarSurface = pygame.Surface((bar_width, 120), pygame.SRCALPHA)

        # Buttons
        self.buttonPlay = pygame.Rect(0, 0, 190, 75)
        self.buttonInstructions = pygame.Rect(0, 0, 180, 50)
        self.buttonSettings = pygame.Rect(0, 0, 180, 50)
        self.buttonQuit = pygame.Rect(0, 0, 200, 75)

        total_width = self.buttonPlay.width + self.buttonInstructions.width + self.buttonSettings.width + self.buttonQuit.width
        spacing = (self.buttonBar.width - total_width) // 5  # even spacing

        x = spacing
        self.buttonPlay.topleft = (x, (self.buttonBar.height - self.buttonPlay.height) // 2)
        x += self.buttonPlay.width + spacing
        self.buttonSettings.topleft = (x, (self.buttonBar.height - self.buttonSettings.height) // 2)
        x += self.buttonSettings.width + spacing
        self.buttonInstructions.topleft = (x, (self.buttonBar.height - self.buttonInstructions.height) // 2)
        x += self.buttonInstructions.width + spacing
        self.buttonQuit.topleft = (x, (self.buttonBar.height - self.buttonQuit.height) // 2)

        # ----------------------------- TV Overlay --------------------------------
        self.tvOverlay = pygame.image.load('Graphics/Backgrounds/CRT.png').convert_alpha()
        self.tvOverlay = pygame.transform.scale(self.tvOverlay, (1300, 750))

        # ----------------------------- Help Screen --------------------------------
        self.showHelpScreen = False
        self.helpFont = pygame.font.Font('Graphics/Text/m6x11.ttf', 30)
        self.helpText = [
            "Welcome to Balatro!",
            "Goal: Play the best hand and win the game.",
            "1. Select up to 5 Cards by clicking on them.",
            "2. Play your hand with the 'PLAY' button.",
            "3. Sort your hand using 'Rank' or 'Suit'.",
            "4. Discard unwanted Cards with the 'QUIT' button.",
            "5. Have fun and enjoy the game!"
        ]

        # Overlay state
        # Buttons for overlay
        # in __init__
        self.showPlayOverlay = False
        self.overlaySurface = pygame.Surface((400, 200), pygame.SRCALPHA)
        self.overlaySurface.fill((50, 50, 50, 200))

        # Overlay buttons
        self.buttonNewGame = pygame.Rect(50, 50, 120, 50)
        self.buttonLoadGame = pygame.Rect(230, 50, 120, 50)

        # Text
        self.textFontOverlay = pygame.font.Font('Graphics/Text/m6x11.ttf', 30)
        self.textNewGame = self.textFontOverlay.render("NEW GAME", True, 'white')
        self.textLoadGame = self.textFontOverlay.render("LOAD GAME", True, 'white')

        # Example: New Game Deck buttons
        self.buttonNormalDeck = pygame.Rect(50, 50, 120, 50)
        self.buttonBlueDeck = pygame.Rect(200, 50, 120, 50)
        self.buttonRedDeck = pygame.Rect(350, 50, 120, 50)
        self.buttonGoldDeck = pygame.Rect(500, 50, 120, 50)

        self.deckOptions = ["Normal", "Blue", "Red", "Gold"]
        self.selectedDeckIndex = 0  # default to Normal
        self.deckCycleRect = pygame.Rect(270, 120, 50, 40)  # adjust position inside overlay

        # Text surfaces
        self.textNormalDeck = self.textFontOverlay.render("Normal", True, 'white')
        self.textBlueDeck = self.textFontOverlay.render("Blue Deck", True, 'white')
        self.textRedDeck = self.textFontOverlay.render("Red Deck", True, 'white')
        self.textGoldDeck = self.textFontOverlay.render("Gold Deck (+$5)", True, 'white')

    def has_save_file(self):
        save_file = "settings.json"  # or whatever your save filename is
        return os.path.isfile(save_file) and os.path.getsize(save_file) > 0

    # ----------------------------- Update ------------------------------------
    def update(self):
        try:
            frame = next(self.frame_generator)
            self.current_frame = next(self.frame_generator)
        except StopIteration:
            # Restart generator when video ends
            print("Looping bg...")
            self.frame_generator = self.clip.iter_frames(fps=30, dtype='uint8')
            self.current_frame = next(self.frame_generator)

        # Convert frame to Pygame surface
        frame_surface = pygame.surfarray.make_surface(self.current_frame.swapaxes(0, 1))
        State.screen.blit(frame_surface, self.backgroundRect)

        self.breathTime += self.breathSpeed  # increment small delta each frame
        self.updateBreathTitle()
        self.draw()

    # ----------------------------- Draw --------------------------------------
    def draw(self):
        frame_surface = pygame.surfarray.make_surface(self.current_frame.swapaxes(0, 1))
        State.screen.blit(frame_surface, (0, 0))
        State.screen.blit(self.title, self.titleRect)
        State.screen.blit(self.titleCard, self.titleCardRect)

        pygame.draw.rect(State.screen, (50, 50, 50), self.buttonBar)
        self.buttonBarSurface.fill((0, 0, 0, 0))
        self.drawbuttons()
        State.screen.blit(self.buttonBarSurface, self.buttonBar)

        # Draw CRT overlay on top
        State.screen.blit(self.tvOverlay, (0, 0))

        # Draw Help Screen Overlay if active
        if self.showHelpScreen:
            self.drawHelpScreen()

        if self.showPlayOverlay:
            overlayRect = self.overlaySurface.get_rect(center=(650, 375))
            State.screen.blit(self.overlaySurface, overlayRect)

            # New Game button
            pygame.draw.rect(State.screen, (0, 200, 0), self.buttonNewGame.move(overlayRect.topleft))
            State.screen.blit(self.textNewGame,
                              self.textNewGame.get_rect(center=self.buttonNewGame.move(overlayRect.topleft).center))

            # Load Game button
            load_enabled = self.has_save_file()
            color = (0, 0, 200) if load_enabled else (100, 100, 100)
            pygame.draw.rect(State.screen, color, self.buttonLoadGame.move(overlayRect.topleft))
            State.screen.blit(self.textLoadGame,
                              self.textLoadGame.get_rect(center=self.buttonLoadGame.move(overlayRect.topleft).center))

            # Deck selector text
            deckText = self.textFontOverlay.render(f"Deck: {self.deckOptions[self.selectedDeckIndex]}", True, 'white')
            deckTextRect = deckText.get_rect(topleft=(50 + overlayRect.x, 120 + overlayRect.y))
            State.screen.blit(deckText, deckTextRect)

            # Cycle button
            pygame.draw.rect(State.screen, (255, 140, 0), self.deckCycleRect.move(overlayRect.topleft))
            arrowText = self.textFontOverlay.render(">", True, 'white')
            arrowRect = arrowText.get_rect(center=self.deckCycleRect.move(overlayRect.topleft).center)
            State.screen.blit(arrowText, arrowRect)

    # ----------------------------- Help Screen --------------------------------
    def drawHelpScreen(self):
        overlay = pygame.Surface((1300, 750), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))  # semi-transparent dark overlay
        State.screen.blit(overlay, (0, 0))

        start_y = 150
        for i, line in enumerate(self.helpText):
            text_surf = self.helpFont.render(line, True, 'white')
            text_rect = text_surf.get_rect(center=(650, start_y + i * 50))
            State.screen.blit(text_surf, text_rect)

        closeText = self.helpFont.render("Click anywhere to close", True, 'yellow')
        closeRect = closeText.get_rect(center=(650, 700))
        State.screen.blit(closeText, closeRect)

    # ----------------------------- Draw Buttons --------------------------------
    def drawbuttons(self):
        mousePos = pygame.mouse.get_pos()
        mousePosbuttonBar = (mousePos[0] - self.buttonBar.x, mousePos[1] - self.buttonBar.y)

        def draw_button(rect, base_color, hover_color, text_surface):
            is_hover = rect.collidepoint(mousePosbuttonBar)
            color = hover_color if is_hover else base_color
            pygame.draw.rect(self.buttonBarSurface, color, rect, border_radius=20)
            text_rect = text_surface.get_rect(center=rect.center)
            self.buttonBarSurface.blit(text_surface, text_rect)

        play_base, play_hover = (30, 144, 255), (0, 191, 255)
        settings_base, settings_hover = (255, 140, 0), (255, 165, 0)
        instruct_base, instruct_hover = (30, 255, 33), (100, 255, 33)
        quit_base, quit_hover = (178, 34, 34), (255, 69, 58)

        draw_button(self.buttonPlay, play_base, play_hover, self.textPlay)
        draw_button(self.buttonSettings, settings_base, settings_hover, self.textSettings)
        draw_button(self.buttonInstructions, instruct_base, instruct_hover, self.textInstructions)
        draw_button(self.buttonQuit, quit_base, quit_hover, self.textQuit)

    # ----------------------------- Breathing Animation for Title ------------------------
    def updateBreathTitle(self):
        scale = 1 + math.sin(self.breathTime) * 0.05  # 5% scaling
        newWidth = int(self.baseTitleSize[0] * scale)
        newHeight = int(self.baseTitleSize[1] * scale)
        self.title = pygame.transform.scale(self.titleImage, (newWidth, newHeight))
        self.titleRect = self.title.get_rect(midtop=self.titleRect.midtop)

    # ----------------------------- User Input --------------------------------
    def userInput(self, events):
        mousePos = pygame.mouse.get_pos()
        mousePosbuttonBar = (mousePos[0] - self.buttonBar.x, mousePos[1] - self.buttonBar.y)
        self.isMouseInCard = self.titleCardRect.collidepoint(mousePos)

        if events.type == pygame.QUIT:
            self.isFinished = True
            self.nextState = None

        if events.type == pygame.KEYDOWN and events.key == pygame.K_ESCAPE and not self.showPlayOverlay:
            self.isFinished = True
            self.nextState = None
        elif events.type == pygame.KEYDOWN and events.key == pygame.K_ESCAPE and self.showPlayOverlay:
            self.showPlayOverlay = False

                    # Mouse events
        if events.type == pygame.MOUSEBUTTONDOWN:
            if self.showPlayOverlay:
                overlayRect = self.overlaySurface.get_rect(center=(650, 375))
                mousePosOverlay = (events.pos[0] - overlayRect.x, events.pos[1] - overlayRect.y)

                # --------- NEW GAME ---------
                if self.buttonNewGame.collidepoint(mousePosOverlay):
                    self.buttonSound.play()
                    self.showPlayOverlay = False
                    self.isFinished = True
                    self.nextState = "GameState"

                    State.nextDeckType = self.deckOptions[self.selectedDeckIndex]

                    # Delete old save file for new game
                    save_file = "savegame.json"
                    if os.path.isfile(save_file):
                        os.remove(save_file)

                # --------- LOAD GAME ---------
                elif self.buttonLoadGame.collidepoint(mousePosOverlay) and self.has_save_file():
                    self.buttonSound.play()
                    self.showPlayOverlay = False
                    self.isFinished = True
                    self.nextState = "GameState"

                elif self.deckCycleRect.collidepoint(mousePosOverlay):
                    self.buttonSound.play()
                    # Cycle to the next deck
                    self.selectedDeckIndex += 1
                    if self.selectedDeckIndex >= len(self.deckOptions):
                        self.selectedDeckIndex = 0

            elif self.showHelpScreen:
                self.showHelpScreen = False  # close help overlay on click
            elif self.isMouseInCard:
                self.mouseDragging = True
            elif self.buttonQuit.collidepoint(mousePosbuttonBar):
                self.buttonSound.play()
                self.isFinished = True
                self.nextState = None
            elif self.buttonPlay.collidepoint(mousePosbuttonBar):
                self.buttonSound.play()
                self.showPlayOverlay = True
            elif self.buttonInstructions.collidepoint(mousePosbuttonBar):
                self.buttonSound.play()
                self.showHelpScreen = True  # show help overlay

            elif self.buttonSettings.collidepoint(mousePosbuttonBar):
                State.screenshot = self.screen.copy()
                self.buttonSound.play()
                self.isFinished = True
                self.nextState = "SettingsState"

        elif events.type == pygame.MOUSEBUTTONUP:
            self.mouseDragging = False

        elif events.type == pygame.MOUSEMOTION:
            if self.mouseDragging:
                self.titleCardRect.center = mousePos
            else:
                if self.isMouseInCard:
                    self.titleCardRect = self.titleCard.get_rect(center=self.titleCardRect.center)
                else:
                    self.titleCardRect = self.titleCard.get_rect(topleft=(575, 150))