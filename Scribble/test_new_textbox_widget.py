import time
import pygame

import pygame_widgets
from pygame_widgets.textbox import TextBox
from pygame_widgets.mouse import Mouse, MouseState


class MyTextBox(TextBox):
    def __init__(self, win: pygame.Surface, x: int, y: int, width: int, height: int, isSubWidget=False, **kwargs):
        super().__init__(win, x, y, width, height, isSubWidget, **kwargs)
        self.selected_text = []
        self.select_start_index = 0
        self.select_end_index = 0
        # TODO The text is highlighted only in the row, but not in the column.
        self.buffer = []

        self.selected_text_colour = kwargs.get('selectedTextColour', (0, 0, 255))

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
                    self.select_start_index = self.select_end_index = 0
                    self.set_cursor_position(x)
                    self.select_start_index = self.select_end_index = self.cursorPosition

                else:
                    self.selected = False
                    self.showCursor = False
                    self.cursorTime = time.time()

            elif mouseState == MouseState.DRAG:
                if self.contains(x, y):
                    self.set_cursor_position(x)
                    self.select_end_index = self.cursorPosition
                    self.select_text()

            # Keyboard Input
            if self.selected:
                for event in events:
                    if event.type == pygame.KEYDOWN:
                        self.showCursor = True
                        self.keyDown = True
                        self.repeatKey = event
                        self.repeatTime = time.time()

                        if event.key == pygame.K_BACKSPACE:
                            self.maxLengthReached = False
                            if self.selected_text:
                                self.erase_text()
                            elif self.cursorPosition != 0:
                                self.text.pop(self.cursorPosition - 1)
                                self.onTextChanged(*self.onTextChangedParams)

                                self.cursorPosition = max(self.cursorPosition - 1, 0)

                        elif event.key == pygame.K_DELETE:
                            if self.selected_text:
                                self.erase_text()
                            elif not self.cursorPosition >= len(self.text):
                                self.maxLengthReached = False
                                self.text.pop(self.cursorPosition)
                                self.onTextChanged(*self.onTextChangedParams)

                        elif event.key == pygame.K_RETURN:
                            self.onSubmit(*self.onSubmitParams)

                        elif event.key == pygame.K_RIGHT:
                            self.cursorPosition = min(self.cursorPosition + 1, len(self.text))
                            self.reset_select()

                        elif event.key == pygame.K_LEFT:
                            self.cursorPosition = max(self.cursorPosition - 1, 0)
                            self.reset_select()

                        elif event.key == pygame.K_HOME:
                            self.cursorPosition = 0
                            self.reset_select()

                        elif event.key == pygame.K_END:
                            self.cursorPosition = len(self.text)
                            self.reset_select()

                        elif event.key == pygame.K_ESCAPE:
                            if not self.escape:
                                self.selected = False
                                self.showCursor = False
                                self.escape = True
                                self.repeatKey = None
                                self.keyDown = None
                                self.firstRepeat = True
                                self.reset_select()

                        elif not self.maxLengthReached:
                            symbol = event.unicode
                            if len(symbol) > 0:
                                if not (0 <= ord(symbol) <= 31):
                                    if self.selected_text:
                                        self.erase_text()
                                    self.text.insert(self.cursorPosition, symbol)
                                    self.cursorPosition += 1
                                    self.onTextChanged(*self.onTextChangedParams)
                                else:
                                    self.listen_specific_symbol(event)

                    elif event.type == pygame.KEYUP:
                        self.repeatKey = None
                        self.keyDown = None
                        self.firstRepeat = True
                        self.escape = False

    def listen_specific_symbol(self, event: pygame.event.Event):
        symbol_ord = ord(event.unicode)
        if symbol_ord == 1:  # Ctrl + A
            self.cursorPosition = len(self.text)
            self.select_start_index = 0
            self.select_end_index = len(self.text)
            self.select_text()

        elif symbol_ord == 3:  # Ctrl + C
            if self.selected_text:
                self.buffer = self.selected_text

        elif symbol_ord == 22:  # Ctrl + V
            self.keyDown = True
            self.repeatKey = event
            self.repeatTime = time.time()

            self.text = self.text[:self.cursorPosition] + self.buffer + self.text[len(self.buffer):]
            self.cursorPosition += len(self.buffer)
            self.onTextChanged(*self.onTextChangedParams)

        elif symbol_ord == 24:  # Ctrl + X
            if self.selected_text:
                self.keyDown = True
                self.repeatKey = event
                self.repeatTime = time.time()
                self.buffer = self.selected_text
                self.erase_text()

    def draw(self):
        """ Display to surface """
        if not self._hidden:
            if self.selected:
                self.updateCursor()

            borderRects = [
                (self._x + self.radius, self._y, self._width - self.radius * 2, self._height),
                (self._x, self._y + self.radius, self._width, self._height - self.radius * 2),
            ]

            borderCircles = [
                (self._x + self.radius, self._y + self.radius),
                (self._x + self.radius, self._y + self._height - self.radius),
                (self._x + self._width - self.radius, self._y + self.radius),
                (self._x + self._width - self.radius, self._y + self._height - self.radius)
            ]

            backgroundRects = [
                (
                    self._x + self.borderThickness + self.radius,
                    self._y + self.borderThickness,
                    self._width - 2 * (self.borderThickness + self.radius),
                    self._height - 2 * self.borderThickness
                ),
                (
                    self._x + self.borderThickness,
                    self._y + self.borderThickness + self.radius,
                    self._width - 2 * self.borderThickness,
                    self._height - 2 * (self.borderThickness + self.radius)
                )
            ]

            backgroundCircles = [
                (self._x + self.radius + self.borderThickness,
                 self._y + self.radius + self.borderThickness),
                (self._x + self.radius + self.borderThickness,
                 self._y + self._height - self.radius - self.borderThickness),
                (self._x + self._width - self.radius - self.borderThickness,
                 self._y + self.radius + self.borderThickness),
                (self._x + self._width - self.radius - self.borderThickness,
                 self._y + self._height - self.radius - self.borderThickness)
            ]

            selectedRects = []
            x = [self._x + self.textOffsetLeft]
            for symbol_index, symbol in enumerate(self.text):
                text = self.font.render(symbol, True, self.textColour)
                start_index, end_index = self.get_valid_select_indexes()
                if start_index <= symbol_index < end_index:
                    selectedRects.append(
                        (x[-1], self._y + self.cursorOffsetTop,
                         text.get_width(), self._height - self.borderThickness * 2 - self.textOffsetBottom)
                    )
                x.append(x[-1] + text.get_width())

            for rect in borderRects:
                pygame.draw.rect(self.win, self.borderColour, rect)

            for circle in borderCircles:
                pygame.draw.circle(self.win, self.borderColour, circle, self.radius)

            for rect in backgroundRects:
                pygame.draw.rect(self.win, self.colour, rect)

            for circle in backgroundCircles:
                pygame.draw.circle(self.win, self.colour, circle, self.radius)

            for rect in selectedRects:
                pygame.draw.rect(self.win, self.selected_text_colour, rect)

            # Display text or placeholder text
            x = [self._x + self.textOffsetLeft]
            for i, c in enumerate(self.text if len(self.text) > 0 else self.placeholderText):
                text = self.font.render(c, True,
                                        (self.textColour if len(self.text) > 0 else self.placeholderTextColour))
                textRect = text.get_rect(bottomleft=(x[-1], self._y + self._height - self.textOffsetBottom))
                self.win.blit(text, textRect)
                x.append(x[-1] + text.get_width())

            if self.showCursor:
                try:
                    pygame.draw.line(
                        self.win, self.cursorColour,
                        (x[self.cursorPosition], self._y + self.cursorOffsetTop),
                        (x[self.cursorPosition], self._y + self._height - self.cursorOffsetTop)
                    )
                except IndexError:
                    self.cursorPosition -= 1

            if x[-1] > self._x + self._width - self.textOffsetRight:
                self.maxLengthReached = True

    def erase_text(self):
        start_index, end_index = self.get_valid_select_indexes()
        self.text = self.text[:start_index] + self.text[end_index:]
        self.cursorPosition = start_index
        self.reset_select()

    def select_text(self):
        start_index, end_index = self.get_valid_select_indexes()
        self.selected_text = self.text[start_index: end_index]

    def set_cursor_position(self, x: int):
        coord = [self._x + self.textOffsetLeft]
        for symbol_index in range(len(self.text) - 1):
            symbol_render1 = self.font.render(self.text[symbol_index], True, self.textColour)
            symbol_render2 = self.font.render(self.text[symbol_index + 1], True, self.textColour)
            x1 = symbol_render1.get_width() + coord[-1]
            x2 = symbol_render2.get_width() + x1
            coord.append(x1)
            if x1 - symbol_render1.get_width() / 2 <= x <= x2 + symbol_render2.get_width() / 2:
                self.cursorPosition = symbol_index + 1

        if self.text:
            if x < coord[0] + self.font.render(self.text[0], True, self.textColour).get_width() / 2:
                self.cursorPosition = 0
            elif x > coord[-1] + self.font.render(self.text[-1], True, self.textColour).get_width() / 2:
                self.cursorPosition = len(self.text)

    def reset_select(self):
        self.select_start_index = self.select_end_index = 0
        self.selected_text = []

    def get_valid_select_indexes(self):
        start_index = min(self.select_start_index, self.select_end_index)
        end_index = max(self.select_start_index, self.select_end_index)
        return start_index, end_index


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
