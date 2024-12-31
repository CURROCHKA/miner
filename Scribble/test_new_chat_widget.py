import time
import pygame

import pygame_widgets
from pygame_widgets.textbox import TextBox
from pygame_widgets.mouse import Mouse, MouseState


class MyTextBox(TextBox):
    def __init__(self, win: pygame.Surface, x: int, y: int, width: int, height: int, isSubWidget=False, **kwargs):
        super().__init__(win, x, y, width, height, isSubWidget, **kwargs)
        self.selected_text = []

    def listen(self, events):
        if not self._hidden and not self._disabled:
            if self.keyDown:
                self.updateRepeatKey()

            mouseState = Mouse.getMouseState()
            x, y = Mouse.getMousePos()

            if mouseState == MouseState.CLICK:
                if self.contains(x, y):
                    self.selected = True
                    self.showCursor = True
                    self.cursorTime = time.time()

                else:
                    self.selected = False
                    self.showCursor = False
                    self.cursorTime = time.time()

            keys = pygame.key.get_pressed()

            if keys[pygame.K_LCTRL] and keys[pygame.K_a]:
                self.selected_text = self.getText()
                # TODO fill the selected text with a spec color (blue by default)

            # Keyboard Input
            if self.selected:
                for event in events:
                    if event.type == pygame.KEYDOWN:
                        self.showCursor = True
                        self.keyDown = True
                        self.repeatKey = event
                        self.repeatTime = time.time()

                        if event.key == pygame.K_BACKSPACE:
                            if self.cursorPosition != 0:
                                self.maxLengthReached = False
                                if len(self.selected_text) != 0:
                                    self.erase_selected_text()
                                else:
                                    self.text.pop(self.cursorPosition - 1)
                                self.onTextChanged(*self.onTextChangedParams)

                            self.cursorPosition = max(self.cursorPosition - 1, 0)

                        elif event.key == pygame.K_DELETE:
                            if not self.cursorPosition >= len(self.text):
                                self.maxLengthReached = False
                                self.text.pop(self.cursorPosition)
                                self.onTextChanged(*self.onTextChangedParams)

                        elif event.key == pygame.K_RETURN:
                            self.onSubmit(*self.onSubmitParams)

                        elif event.key == pygame.K_RIGHT:
                            self.cursorPosition = min(self.cursorPosition + 1, len(self.text))

                        elif event.key == pygame.K_LEFT:
                            self.cursorPosition = max(self.cursorPosition - 1, 0)

                        elif event.key == pygame.K_END:
                            self.cursorPosition = len(self.text)

                        elif event.key == pygame.K_ESCAPE:
                            if not self.escape:
                                self.selected = False
                                self.showCursor = False
                                self.escape = True
                                self.repeatKey = None
                                self.keyDown = None
                                self.firstRepeat = True

                        elif not self.maxLengthReached:
                            symbol = event.unicode
                            if len(symbol) > 0:
                                if not (0 <= ord(symbol) <= 32):
                                    self.text.insert(self.cursorPosition, symbol)
                                    self.cursorPosition += 1
                                    self.onTextChanged(*self.onTextChangedParams)

                    elif event.type == pygame.KEYUP:
                        self.repeatKey = None
                        self.keyDown = None
                        self.firstRepeat = True
                        self.escape = False

    def erase_selected_text(self):
        string = self.getText()
        start = string.find(self.selected_text)
        end = start + len(self.selected_text) - 1
        self.text = self.text[:start] + self.text[end + 1:]
        self.cursorPosition = 0


if __name__ == '__main__':
    def output():
        print(len(textbox.getText()))
        textbox.setText('')


    pygame.init()
    win = pygame.display.set_mode((1000, 600))

    textbox = MyTextBox(win, 100, 100, 800, 80, fontSize=50, borderColour=(255, 0, 0),
                        textColour=(0, 200, 0), onSubmit=output, radius=10,
                        borderThickness=5, placeholderText='Enter something:')

    run = True
    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                quit()

        win.fill((255, 255, 255))

        pygame_widgets.update(events)
        pygame.display.update()
