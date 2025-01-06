import time
import pygame

import pygame_widgets
from pygame_widgets.textbox import TextBox
from pygame_widgets.mouse import Mouse, MouseState


# TODO need to add scrolling through the text


class MyTextBox(TextBox):
    def __init__(self, win: pygame.Surface, x: int, y: int, width: int, height: int, isSubWidget=False, **kwargs):
        super().__init__(win, x, y, width, height, isSubWidget, **kwargs)
        self.text = [[]]
        self.selected_line = 0
        self.text_in_selected_line = self.text[self.selected_line]
        self.gap_btw_lines = self.fontSize / 3

        self.highlighted_text = []
        self.highlight_in_line_start = 0
        self.highlight_in_line_end = 0

        # TODO The text is highlighted only in the row, but not in the column.
        self.buffer = []

        # self.highlighted_text_colour = kwargs.get('highlightedTextColour', (33, 66, 131))  # dark theme
        self.highlighted_text_colour = kwargs.get('highlightedTextColour', (166, 210, 255))  # light theme

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
                    self.set_cursor_position_after_mouse_event(x)
                    self.highlight_in_line_start = self.highlight_in_line_end = self.cursorPosition

                else:
                    self.selected = False
                    self.showCursor = False
                    self.cursorTime = time.time()

            elif mouseState == MouseState.DRAG:
                if self.contains(x, y):
                    self.set_cursor_position_after_mouse_event(x)
                    self.highlight_in_line_end = self.cursorPosition
                    self.highlight_text()

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
                            if self.highlighted_text:
                                self.erase_text()
                            elif self.cursorPosition != 0:
                                self.highlight_in_line_start = self.cursorPosition - 1
                                self.highlight_in_line_end = self.cursorPosition
                                self.highlight_text()
                                self.erase_text()
                                self.cursorPosition += 1
                                self.cursorPosition = max(self.cursorPosition - 1, 0)

                        elif event.key == pygame.K_DELETE:
                            if self.highlighted_text:
                                self.erase_text()
                            elif not self.cursorPosition >= len(self.text_in_selected_line):
                                self.maxLengthReached = False
                                self.highlight_in_line_start = self.cursorPosition
                                self.highlight_in_line_end = self.cursorPosition + 1
                                self.highlight_text()
                                self.erase_text()

                        elif event.key == pygame.K_RETURN:
                            self.onSubmit(*self.onSubmitParams)

                        elif event.key == pygame.K_RIGHT:
                            self.cursorPosition = min(self.cursorPosition + 1, len(self.text_in_selected_line))
                            self.reset_highlight()

                        elif event.key == pygame.K_LEFT:
                            self.cursorPosition = max(self.cursorPosition - 1, 0)
                            self.reset_highlight()

                        elif event.key == pygame.K_HOME:
                            self.cursorPosition = 0
                            self.reset_highlight()

                        elif event.key == pygame.K_END:
                            self.cursorPosition = len(self.text_in_selected_line)
                            self.reset_highlight()

                        elif event.key == pygame.K_ESCAPE:
                            if not self.escape:
                                self.selected = False
                                self.showCursor = False
                                self.escape = True
                                self.repeatKey = None
                                self.keyDown = None
                                self.firstRepeat = True
                                self.reset_highlight()

                        # elif not self.maxLengthReached:
                        symbol = event.unicode
                        if len(symbol) > 0:
                            if not (0 <= ord(symbol) <= 31 or ord(symbol) == 127):  # NOT Spec symbols
                                if self.highlighted_text:
                                    self.erase_text()
                                self.add_text(symbol)
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
            self.cursorPosition = len(self.text_in_selected_line)
            self.highlight_in_line_start = 0
            self.highlight_in_line_end = len(self.text_in_selected_line)
            self.highlight_text()
            # TODO highlight text in all lines

        elif symbol_ord == 3:  # Ctrl + C
            if self.highlighted_text:
                self.buffer = self.highlighted_text

        elif symbol_ord == 22:  # Ctrl + V
            self.keyDown = True
            self.repeatKey = event
            self.repeatTime = time.time()
            if self.buffer:
                if self.highlighted_text:
                    self.erase_text()
                self.add_text(self.buffer)

        elif symbol_ord == 24:  # Ctrl + X
            if self.highlighted_text:
                self.keyDown = True
                self.repeatKey = event
                self.repeatTime = time.time()
                self.buffer = self.highlighted_text
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

            highlightedRects = []
            x = [self._x + self.textOffsetLeft]
            for symbol_index, symbol in enumerate(self.text_in_selected_line):
                text = self.font.render(symbol, True, self.textColour)
                start_index, end_index = self.get_valid_highlight_indexes()
                if start_index <= symbol_index < end_index:
                    highlightedRects.append(
                        (x[-1], self._y + self.textOffsetBottom + self.fontSize * self.selected_line,
                         text.get_width(), self.fontSize)
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

            for rect in highlightedRects:
                pygame.draw.rect(self.win, self.highlighted_text_colour, rect)

            # Display text or placeholder text
            if any(line for line in self.text):
                for line_number, line in enumerate(self.text):
                    self.draw_text(line, self.textColour, line_number)
            else:
                self.draw_text(self.placeholderText, self.placeholderTextColour, self.selected_line)

            if self.showCursor:
                try:
                    pygame.draw.line(
                        self.win, self.cursorColour,
                        (x[self.cursorPosition], self._y + self.textOffsetBottom + self.fontSize * self.selected_line),
                        (x[self.cursorPosition],
                         self._y + self.textOffsetBottom + self.fontSize + self.fontSize * self.selected_line),
                        width=2
                    )
                except IndexError:
                    self.cursorPosition -= 1

            if x[-1] > self._x + self._width - self.textOffsetRight:
                self.maxLengthReached = True

    def draw_text(self, string: str | list, color: tuple[int, int, int] | str, line_number: int):
        x = [self._x + self.textOffsetLeft]
        for symbol in string:
            text = self.font.render(symbol, True, color)
            textRect = text.get_rect(bottomleft=(
                x[-1], self._y + self.textOffsetBottom + self.fontSize + self.fontSize * line_number))
            self.win.blit(text, textRect)
            x.append(x[-1] + text.get_width())

    def max_length_reached(self, text):
        x = [self._x + self.textOffsetLeft]
        for symbol in text:
            text = self.font.render(symbol, True, self.textColour)
            x.append(x[-1] + text.get_width())
            if x[-1] > self._x + self._width - self.textOffsetRight:
                return True
        return False

    def add_text(self, sequence: list[str]):
        text = self.text_in_selected_line[:]
        if self.highlighted_text:
            self.erase_text()
        max_length_reached = False
        for symbol in sequence:
            text.insert(self.cursorPosition, symbol)
            if not max_length_reached and self.max_length_reached(text):
                max_length_reached = True
                self.selected_line += 1
                try:
                    self.text_in_selected_line = self.text[self.selected_line]
                except IndexError:
                    self.text.append([])
                    self.text_in_selected_line = self.text[self.selected_line]
            self.text_in_selected_line.insert(self.cursorPosition, symbol)
            self.cursorPosition += 1
            self.onTextChanged(*self.onTextChangedParams)

    def erase_text(self):
        start_index, end_index = self.get_valid_highlight_indexes()
        for _ in self.highlighted_text:
            self.text_in_selected_line.pop(start_index)
            self.onTextChanged(*self.onTextChangedParams)
        if start_index == 0 and self.selected_line >= 1:
            self.selected_line -= 1
            self.text_in_selected_line = self.text[self.selected_line]
            self.cursorPosition = len(self.text_in_selected_line)
        else:
            self.cursorPosition = start_index
        self.reset_highlight()

    def highlight_text(self):
        start_index, end_index = self.get_valid_highlight_indexes()
        self.highlighted_text = self.text_in_selected_line[start_index: end_index]

    def set_cursor_position_after_mouse_event(self, x: int):
        coord = [self._x + self.textOffsetLeft]
        for symbol_index in range(len(self.text_in_selected_line) - 1):
            symbol_render1 = self.font.render(self.text_in_selected_line[symbol_index], True, self.textColour)
            symbol_render2 = self.font.render(self.text_in_selected_line[symbol_index + 1], True, self.textColour)
            x1 = symbol_render1.get_width() + coord[-1]
            x2 = symbol_render2.get_width() + x1
            coord.append(x1)
            if x1 - symbol_render1.get_width() / 2 <= x <= x2 + symbol_render2.get_width() / 2:
                self.cursorPosition = symbol_index + 1

        if self.text_in_selected_line:
            if x < coord[0] + self.font.render(self.text_in_selected_line[0], True, self.textColour).get_width() / 2:
                self.cursorPosition = 0
            elif x > coord[-1] + self.font.render(self.text_in_selected_line[-1], True,
                                                  self.textColour).get_width() / 2:
                self.cursorPosition = len(self.text_in_selected_line)
                self.cursorPosition = len(self.text_in_selected_line)

    def reset_highlight(self):
        self.highlight_in_line_start = self.highlight_in_line_end = 0
        self.highlighted_text = []

    def get_valid_highlight_indexes(self):
        start_index = min(self.highlight_in_line_start, self.highlight_in_line_end)
        end_index = max(self.highlight_in_line_start, self.highlight_in_line_end)
        return start_index, end_index


if __name__ == '__main__':
    def output():
        print(len(textbox.getText()))
        textbox.setText('')


    pygame.init()
    win = pygame.display.set_mode((1000, 600))

    textbox = MyTextBox(win, 100, 100, 800, 400, fontSize=50, borderColour=(255, 0, 0),
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
