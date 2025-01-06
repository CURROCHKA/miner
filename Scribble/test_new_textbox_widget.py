import time
import pygame
import pyperclip

import pygame_widgets
from pygame_widgets.textbox import TextBox
from pygame_widgets.mouse import Mouse, MouseState


# TODO need to add scrolling through the text


class MyTextBox(TextBox):
    def __init__(self, win: pygame.Surface, x: int, y: int, width: int, height: int, isSubWidget=False, **kwargs):
        super().__init__(win, x, y, width, height, isSubWidget, **kwargs)
        self.textOffsetTop = self.textOffsetBottom
        self.text = [[]]
        self.selected_line = 0

        self.highlighted_text = []

        self.highlight_in_line_start = 0
        self.highlight_in_line_end = 0

        self.highlight_line_start = 0
        self.highlight_line_end = 0

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

                    self.set_selected_line_after_mouse_event(y)
                    self.highlight_line_start = self.highlight_line_end = self.selected_line
                else:
                    self.selected = False
                    self.showCursor = False
                    self.cursorTime = time.time()

            elif mouseState == MouseState.DRAG:
                if self.contains(x, y):
                    self.set_cursor_position_after_mouse_event(x)
                    self.highlight_in_line_end = self.cursorPosition

                    self.set_selected_line_after_mouse_event(y)
                    self.highlight_line_end = self.selected_line

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

                                self.highlight_line_start = self.highlight_line_end = self.selected_line

                                self.highlight_text()
                                self.erase_text()

                                self.cursorPosition += 1
                                self.cursorPosition = max(self.cursorPosition - 1, 0)

                        elif event.key == pygame.K_DELETE:
                            if self.highlighted_text:
                                self.erase_text()
                            elif not self.cursorPosition >= len(self.text[self.selected_line]):
                                self.maxLengthReached = False
                                self.highlight_in_line_start = self.cursorPosition
                                self.highlight_in_line_end = self.cursorPosition + 1

                                self.highlight_line_start = self.highlight_line_end = self.selected_line

                                self.highlight_text()
                                self.erase_text()

                        elif event.key == pygame.K_RETURN:
                            self.onSubmit(*self.onSubmitParams)

                        elif event.key == pygame.K_RIGHT:
                            self.cursorPosition = min(self.cursorPosition + 1, len(self.text[self.selected_line]))
                            self.reset_highlight()

                        elif event.key == pygame.K_LEFT:
                            self.cursorPosition = max(self.cursorPosition - 1, 0)
                            self.reset_highlight()

                        elif event.key == pygame.K_HOME:
                            self.cursorPosition = 0
                            self.reset_highlight()

                        elif event.key == pygame.K_END:
                            self.cursorPosition = len(self.text[self.selected_line])
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
            self.selected_line = len(self.text) - 1
            self.cursorPosition = len(self.text[self.selected_line])

            self.highlight_in_line_start = 0
            self.highlight_in_line_end = len(self.text[self.selected_line])

            self.highlight_line_start = 0
            self.highlight_line_end = len(self.text) - 1

            self.highlight_text()

        elif symbol_ord == 3:  # Ctrl + C
            if self.highlighted_text:
                self.copy_highlighted_text()

        elif symbol_ord == 22:  # Ctrl + V
            self.keyDown = True
            self.repeatKey = event
            self.repeatTime = time.time()
            text = pyperclip.paste()
            if len(text) > 0:
                if self.highlighted_text:
                    self.erase_text()
                self.add_text(text)

        elif symbol_ord == 24:  # Ctrl + X
            if self.highlighted_text:
                self.keyDown = True
                self.repeatKey = event
                self.repeatTime = time.time()
                self.copy_highlighted_text()
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

            line_start, line_end = self.get_valid_highlight_line_indexes()
            if line_start == line_end:
                in_line_start, in_line_end = self.get_valid_highlight_in_line_indexes()
                highlightedRects = self.get_selected_rect(line_start, in_line_start, in_line_end)
            else:
                in_line_start = self.highlight_in_line_start
                in_line_end = self.highlight_in_line_end

                if line_start != self.highlight_line_start:
                    in_line_start = self.highlight_in_line_end
                    in_line_end = self.highlight_in_line_start

                highlightedRects =\
                    self.get_selected_rect(line_start, in_line_start, len(self.text[line_start]))
                for line in range(line_start + 1, line_end):
                    highlightedRects += self.get_selected_rect(line, 0, len(self.text[line]))
                highlightedRects += self.get_selected_rect(line_end, 0, in_line_end)

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

            x = [self._x + self.textOffsetLeft]
            for symbol in self.text[self.selected_line]:
                if not symbol.isprintable():
                    continue
                text = self.font.render(symbol, True, self.textColour)
                x.append(x[-1] + text.get_width())
            if self.showCursor:
                try:
                    pygame.draw.line(
                        self.win, self.cursorColour,
                        (x[self.cursorPosition],
                         self._y + self.textOffsetTop + self.fontSize * self.selected_line),
                        (x[self.cursorPosition],
                         self._y + self.textOffsetTop + self.fontSize + self.fontSize * self.selected_line),
                        width=2
                    )
                except IndexError:
                    self.cursorPosition -= 1

            if x[-1] > self._x + self._width - self.textOffsetRight:
                self.maxLengthReached = True

    def draw_text(self, string: str | list, color: tuple[int, int, int] | str, line_number: int):
        x = [self._x + self.textOffsetLeft]
        for symbol in string:
            if not symbol.isprintable():
                continue
            text = self.font.render(symbol, True, color)
            textRect = text.get_rect(bottomleft=(
                x[-1], self._y + self.textOffsetTop + self.fontSize + self.fontSize * line_number))
            self.win.blit(text, textRect)
            x.append(x[-1] + text.get_width())

    def get_selected_rect(self, line: int, in_line_start: int, in_line_end: int):
        x = [self._x + self.textOffsetLeft]
        highlightedRects = []
        for symbol_index, symbol in enumerate(self.text[line]):
            if not symbol.isprintable():
                continue
            text = self.font.render(symbol, True, self.textColour)
            if in_line_start <= symbol_index < in_line_end:
                highlightedRects.append(
                    (x[-1], self._y + self.textOffsetTop + self.fontSize * line,
                     text.get_width(), self.fontSize)
                )
            x.append(x[-1] + text.get_width())
        return highlightedRects

    def setText(self, text):
        text = []
        max_length_reached = False
        for symbol in text:
            text.append(symbol)
            if not max_length_reached and self.max_length_reached(text):
                text = []

    def getText(self):
        text = ''
        for line in self.text:
            text += ''.join(line)
        return text

    def copy_highlighted_text(self):
        text = []
        for line in self.highlighted_text:
            text.append(''.join(line))
        pyperclip.copy('\n'.join(text))

    def max_length_reached(self, text):
        x = [self._x + self.textOffsetLeft]
        for symbol in text:
            if not symbol.isprintable():
                continue
            text = self.font.render(symbol, True, self.textColour)
            x.append(x[-1] + text.get_width())
            if x[-1] >= self._x + self._width - self.textOffsetRight:
                return True
        return False

    def add_text(self, sequence: list[str]):
        text = self.text[self.selected_line][:]
        if self.highlighted_text:
            self.erase_text()
        for symbol in sequence:
            if not symbol.isprintable():
                continue
            text.insert(self.cursorPosition, symbol)
            if self.max_length_reached(text):
                text = []
                self.selected_line += 1
            try:
                self.text[self.selected_line].insert(self.cursorPosition, symbol)
            except IndexError:
                self.text.append([symbol])
            self.cursorPosition += 1
            self.onTextChanged(*self.onTextChangedParams)

    def erase_text(self):
        line_start, line_end = self.get_valid_highlight_line_indexes()
        in_line_start, in_line_end = self.get_valid_highlight_in_line_indexes()

        if line_start == self.highlight_line_start:
            self.text[self.selected_line] = self.text[self.selected_line][:in_line_start] + self.text[self.selected_line][in_line_end:]
        else:
            in_line_start = self.highlight_line_end
            in_line_end = self.highlight_line_start

            self.text[line_start] = self.text[line_start][:in_line_start]
            for line in self.text[line_start + 1: line_end]:
                self.text.remove(line)
            length_of_removed_lines = line_end - line_start + 1
            self.text[line_end - length_of_removed_lines] = self.text[line_end - length_of_removed_lines][in_line_end:]

        self.cursorPosition = in_line_start
        self.selected_line = line_start

        self.reset_highlight()

    def highlight_text(self):
        line_start, line_end = self.get_valid_highlight_line_indexes()
        if line_start == line_end:
            in_line_start, in_line_end = self.get_valid_highlight_in_line_indexes()
            self.highlighted_text = [self.text[line_start][in_line_start:in_line_end]]
        else:
            self.highlighted_text = [self.text[line_start][self.highlight_in_line_start:]]
            for line_number in range(line_start + 1, line_end):
                self.highlighted_text.append([self.text[line_number]])
            self.highlighted_text += [self.text[line_end][:self.highlight_in_line_end]]

    def set_selected_line_after_mouse_event(self, y: int):
        coord = [self._y + self.textOffsetTop + self.fontSize]
        for line_number in range(len(self.text)):
            if coord[-1] - self.fontSize / 2 <= y <= coord[-1] + self.fontSize / 2:
                self.selected_line = line_number
            coord.append(coord[-1] + self.fontSize)

        if y < coord[0] + self.fontSize / 2:
            self.selected_line = 0
        elif y > coord[-1] + self.fontSize / 2:
            self.selected_line = len(self.text) - 1

    def set_cursor_position_after_mouse_event(self, x: int):
        coord = [self._x + self.textOffsetLeft]
        for symbol_index in range(len(self.text[self.selected_line]) - 1):
            symbol1 = self.text[self.selected_line][symbol_index]
            symbol2 = self.text[self.selected_line][symbol_index + 1]

            symbol_render1 = self.font.render(symbol1, True, self.textColour)
            symbol_render2 = self.font.render(symbol2, True, self.textColour)

            x1 = symbol_render1.get_width() + coord[-1]
            x2 = symbol_render2.get_width() + x1

            coord.append(x1)

            if x1 - symbol_render1.get_width() / 2 <= x <= x2 + symbol_render2.get_width() / 2:
                self.cursorPosition = symbol_index + 1

        if self.text[self.selected_line]:
            if x < coord[0] + self.font.render(self.text[self.selected_line][0], True, self.textColour).get_width() / 2:
                self.cursorPosition = 0
            elif x > coord[-1] + self.font.render(self.text[self.selected_line][-1], True,
                                                  self.textColour).get_width() / 2:
                self.cursorPosition = len(self.text[self.selected_line])

    def reset_highlight(self):
        self.highlight_in_line_start = self.highlight_in_line_end = 0
        self.highlight_line_start = self.highlight_line_end = 0
        self.highlighted_text = []

    def get_valid_highlight_in_line_indexes(self):
        start_index = min(self.highlight_in_line_start, self.highlight_in_line_end)
        end_index = max(self.highlight_in_line_start, self.highlight_in_line_end)
        return start_index, end_index

    def get_valid_highlight_line_indexes(self):
        start_index = min(self.highlight_line_start, self.highlight_line_end)
        end_index = max(self.highlight_line_start, self.highlight_line_end)
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
