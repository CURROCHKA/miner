import time
import pygame
import pyperclip
from typing import Iterable

import pygame_widgets
from pygame_widgets.textbox import TextBox
from pygame_widgets.mouse import Mouse, MouseState


# TODO need to add scrolling through the text


class MyTextBox(TextBox):
    def __init__(self, win: pygame.Surface, x: int, y: int, width: int, height: int, isSubWidget=False, **kwargs):
        super().__init__(win, x, y, width, height, isSubWidget, **kwargs)
        self.font = kwargs.get('font', pygame.font.SysFont('Consolas', self.fontSize))  # Using monospaced fonts

        # self.highlightedTextColour = kwargs.get('highlightedTextColour', (33, 66, 131))  # dark theme
        self.highlightedTextColour = kwargs.get('highlightedTextColour', (166, 210, 255))  # light theme

        self.textOffsetTop = self.textOffsetBottom
        self.text = [[]]

        # Need to maintain cursor position
        self.oldCursorPosition = self.cursorPosition

        # The line in which user is currently typing
        self.selectedLine = 0

        self.highlightedText = []

        # Edges of highlighting the text
        self.highlightInLineStart = 0
        self.highlightInLineEnd = 0

        self.highlightLineStart = 0
        self.highlightLineEnd = 0

    def listen(self, events: list[pygame.event.Event]) -> None:
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

                    # Setting start of highlighting
                    self.setCursorPositionAfterMouseEvent(x)
                    self.highlightInLineStart = self.highlightInLineEnd = self.cursorPosition

                    self.setSelectedLineAfterMouseEvent(y)
                    self.highlightLineStart = self.highlightLineEnd = self.selectedLine
                else:
                    self.selected = False
                    self.showCursor = False
                    self.cursorTime = time.time()

            elif mouseState == MouseState.DRAG:
                if self.contains(x, y):
                    # Setting end of highlighting
                    self.setCursorPositionAfterMouseEvent(x)
                    self.highlightInLineEnd = self.cursorPosition

                    self.setSelectedLineAfterMouseEvent(y)
                    self.highlightLineEnd = self.selectedLine

                    self.highlightText()

            if self.selected:
                for event in events:
                    # Keyboard Input
                    if event.type == pygame.KEYDOWN:
                        self.showCursor = True
                        self.keyDown = True
                        self.repeatKey = event
                        self.repeatTime = time.time()

                        if event.key == pygame.K_BACKSPACE:
                            if not self.isEmpty2DSequence(self.highlightedText):
                                self.eraseHighlightedText()
                                self.cursorPosition += 1

                            elif self.cursorPosition != 0:
                                del self.text[self.selectedLine][self.cursorPosition - 1]
                                self.shiftLines()
                                self.onTextChanged(*self.onTextChangedParams)

                            elif self.cursorPosition == 0 and self.selectedLine != 0:
                                if len(self.text[self.selectedLine]) == 0:
                                    del self.text[self.selectedLine]

                                self.selectedLine -= 1
                                self.cursorPosition = len(self.text[self.selectedLine])

                                self.eraseSpecialChar()
                                self.shiftLines()
                                self.cursorPosition += 1

                                self.onTextChanged(*self.onTextChangedParams)

                            self.cursorPosition = max(0, self.cursorPosition - 1)

                        elif event.key == pygame.K_DELETE:
                            if not self.isEmpty2DSequence(self.highlightedText):
                                self.eraseHighlightedText()

                            elif self.cursorPosition < len(self.text[self.selectedLine]):
                                del self.text[self.selectedLine][self.cursorPosition]
                                self.shiftLines()
                                self.onTextChanged(*self.onTextChangedParams)

                            elif self.cursorPosition >= len(self.text[self.selectedLine]) != 0 and \
                                    not self.isSpecialChar(self.text[self.selectedLine][self.cursorPosition - 1]):
                                self.shiftLines()

                        elif event.key == pygame.K_RETURN:
                            keys = pygame.key.get_mods()

                            if keys & pygame.KMOD_SHIFT:
                                self.text[self.selectedLine].insert(self.cursorPosition, '\n')
                                self.selectedLine += 1
                                self.text.insert(self.selectedLine,
                                                 self.text[self.selectedLine - 1][self.cursorPosition + 1:])
                                self.text[self.selectedLine - 1] = self.text[self.selectedLine - 1][
                                                                   :self.cursorPosition + 1]
                                self.cursorPosition = self.oldCursorPosition = 0
                            else:
                                self.onSubmit(*self.onSubmitParams)

                            self.resetHighlight()

                        elif event.key == pygame.K_RIGHT:
                            self.cursorPosition = min(self.cursorPosition + 1,
                                                      len(self.text[self.selectedLine]))
                            self.skipSpecialChar()
                            self.oldCursorPosition = self.cursorPosition
                            self.resetHighlight()

                        elif event.key == pygame.K_LEFT:
                            self.cursorPosition = max(self.cursorPosition - 1, 0)
                            self.skipSpecialChar()
                            self.oldCursorPosition = self.cursorPosition
                            self.resetHighlight()

                        elif event.key == pygame.K_UP:
                            self.selectedLine = max(0, self.selectedLine - 1)
                            self.cursorPosition = self.oldCursorPosition
                            if self.cursorPosition >= len(self.text[self.selectedLine]):
                                self.cursorPosition = len(self.text[self.selectedLine])
                            self.skipSpecialChar()
                            self.resetHighlight()

                        elif event.key == pygame.K_DOWN:
                            self.selectedLine = min(len(self.text) - 1, self.selectedLine + 1)
                            self.cursorPosition = self.oldCursorPosition
                            if self.cursorPosition >= len(self.text[self.selectedLine]):
                                self.cursorPosition = len(self.text[self.selectedLine])
                            self.skipSpecialChar()
                            self.resetHighlight()

                        elif event.key == pygame.K_HOME:
                            self.cursorPosition = self.oldCursorPosition = 0
                            self.resetHighlight()

                        elif event.key == pygame.K_END:
                            self.cursorPosition = self.oldCursorPosition = len(self.text[self.selectedLine])
                            self.skipSpecialChar()
                            self.resetHighlight()

                        elif event.key == pygame.K_ESCAPE:
                            if not self.escape:
                                self.selected = False
                                self.showCursor = False
                                self.escape = True
                                self.repeatKey = None
                                self.keyDown = None
                                self.firstRepeat = True
                                self.resetHighlight()

                        char = event.unicode
                        if len(char) > 0:
                            if not self.isSpecialChar(char):  # NOT Spec chars
                                if not self.isEmpty2DSequence(self.highlightedText):
                                    self.eraseHighlightedText()
                                self.addText(char)
                            else:
                                self.listenSpecialChar(event)

                    elif event.type == pygame.KEYUP:
                        self.repeatKey = None
                        self.keyDown = None
                        self.firstRepeat = True
                        self.escape = False

    def listenSpecialChar(self, event: pygame.event.Event) -> None:
        charOrd = ord(event.unicode)
        if charOrd == 1:  # Ctrl + A
            self.selectedLine = len(self.text) - 1
            self.cursorPosition = len(self.text[self.selectedLine])

            self.highlightInLineStart = 0
            self.highlightInLineEnd = len(self.text[self.selectedLine])

            self.highlightLineStart = 0
            self.highlightLineEnd = len(self.text) - 1

            self.highlightText()

        elif charOrd == 3:  # Ctrl + C
            if not self.isEmpty2DSequence(self.highlightedText):
                self.copyHighlightedText()

        elif charOrd == 22:  # Ctrl + V
            self.keyDown = True
            self.repeatKey = event
            self.repeatTime = time.time()
            text = pyperclip.paste()
            if not self.isEmpty2DSequence(self.highlightedText):
                self.eraseHighlightedText()
            self.addText(text)

        elif charOrd == 24:  # Ctrl + X
            if not self.isEmpty2DSequence(self.highlightedText):
                self.keyDown = True
                self.repeatKey = event
                self.repeatTime = time.time()
                self.copyHighlightedText()
                self.eraseHighlightedText()

    def draw(self) -> None:
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

            lineStart, lineEnd = self.getValidHighlightLineIndexes()
            inLineStart, inLineEnd = self.getValidHighlightInLineIndexes()

            if lineStart == lineEnd:
                highlightedRects = self.getHighlightedRect(lineStart, inLineStart, inLineEnd)
            else:
                if lineStart != self.highlightLineStart:
                    inLineStart = self.highlightInLineEnd
                    inLineEnd = self.highlightInLineStart

                highlightedRects = \
                    self.getHighlightedRect(lineStart, inLineStart, len(self.text[lineStart]))
                for line in range(lineStart + 1, lineEnd):
                    highlightedRects += self.getHighlightedRect(line, 0, len(self.text[line]))
                highlightedRects += self.getHighlightedRect(lineEnd, 0, inLineEnd)

            for rect in borderRects:
                pygame.draw.rect(self.win, self.borderColour, rect)

            for circle in borderCircles:
                pygame.draw.circle(self.win, self.borderColour, circle, self.radius)

            for rect in backgroundRects:
                pygame.draw.rect(self.win, self.colour, rect)

            for circle in backgroundCircles:
                pygame.draw.circle(self.win, self.colour, circle, self.radius)

            for rect in highlightedRects:
                pygame.draw.rect(self.win, self.highlightedTextColour, rect)

            # Display text or placeholder text
            if self.text != [[]]:
                visibleText = self.text[:]

                while len(visibleText) * self.fontSize >= self._height - self.textOffsetTop - self.textOffsetBottom:
                    del visibleText[0]

                for lineIndex, line in enumerate(visibleText):
                    self.drawText(line, self.textColour, lineIndex)
            else:
                self.drawText(self.placeholderText, self.placeholderTextColour, self.selectedLine)

            x = self.getLineX(self.text[self.selectedLine])
            if self.showCursor:
                try:
                    pygame.draw.line(
                        self.win, self.cursorColour,
                        (x[self.cursorPosition],
                         self._y + self.textOffsetTop + self.fontSize * self.selectedLine),
                        (x[self.cursorPosition],
                         self._y + self.textOffsetTop + self.fontSize + self.fontSize * self.selectedLine),
                        width=2
                    )
                except IndexError:
                    self.cursorPosition -= 1

    def drawText(self, string: str | list, color: tuple[int, int, int] | str, lineIndex: int) -> None:
        x = self.getLineX(string)

        for charIndex in range(len(string)):
            char = string[charIndex]

            if self.isSpecialChar(char):
                continue

            text = self.font.render(char, True, color)
            textRect = text.get_rect(bottomleft=(
                x[charIndex], self._y + self.textOffsetTop + self.fontSize + self.fontSize * lineIndex))
            self.win.blit(text, textRect)

    def setText(self, text: str) -> None:
        self.text = [[]]
        self.selectedLine = 0
        self.cursorPosition = self.oldCursorPosition = 0
        self.addText(text)

    def getText(self) -> str:
        text = ''
        for line in self.text:
            text += ''.join(line)
        return text

    def addText(self, text: str):
        if not self.isEmpty2DSequence(self.highlightedText):
            self.eraseHighlightedText()

        text = text.replace('\t', ' ' * 4)

        for char in text:
            if ord(char) != 10 and self.isSpecialChar(char):
                continue

            self.insertCharInText(self.selectedLine, self.cursorPosition, char)

            if ord(char) == 10:  # \n
                self.selectedLine += 1
                self.cursorPosition = 0
                self.text.append([])

            for lineIndex in range(self.selectedLine, len(self.text)):
                if self.maxWidthReached(self.text[lineIndex][:-1]):
                    lastChar = self.text[lineIndex][-1]
                    del self.text[lineIndex][-1]

                    if ord(lastChar) == 10:
                        self.selectedLine += 1
                        self.cursorPosition = 0
                        self.text.insert(self.selectedLine, [])
                        self.insertCharInText(lineIndex + 1, 0, lastChar)
                        lastChar = self.text[lineIndex][-2]

                    self.insertCharInText(lineIndex + 1, 0, lastChar)

                    if self.cursorPosition >= len(self.text[lineIndex]) - 1:
                        self.selectedLine += 1
                        self.cursorPosition = 0

            if not self.isSpecialChar(char):
                self.cursorPosition += 1
                self.onTextChanged(*self.onTextChangedParams)

        self.oldCursorPosition = self.cursorPosition

    def eraseHighlightedText(self):
        lineStart, lineEnd = self.getValidHighlightLineIndexes()
        inLineStart, inLineEnd = self.getValidHighlightInLineIndexes()

        if lineStart == lineEnd:  # Simple erase in line
            del self.text[self.selectedLine][inLineStart:inLineEnd]
        else:
            if lineStart == self.highlightLineStart:
                inLineStart, inLineEnd = self.highlightInLineStart, self.highlightInLineEnd
            else:
                inLineStart, inLineEnd = self.highlightInLineEnd, self.highlightInLineStart

            del self.text[lineStart][inLineStart:]
            del self.text[lineEnd][:inLineEnd]
            del self.text[lineStart + 1: lineEnd]

            try:
                if not self.text[lineStart]:
                    del self.text[lineStart]
            except IndexError:
                pass

            try:
                if not self.text[lineEnd]:
                    del self.text[lineEnd]
            except IndexError:
                pass

        self.selectedLine = lineStart
        self.cursorPosition = inLineStart

        self.resetHighlight()

    def highlightText(self):
        lineStart, lineEnd = self.getValidHighlightLineIndexes()
        inLineStart, inLineEnd = self.getValidHighlightInLineIndexes()

        if lineStart == lineEnd:
            self.highlightedText = [self.text[lineStart][inLineStart:inLineEnd]]
        else:
            if lineStart == self.highlightLineStart:
                inLineStart, inLineEnd = self.highlightInLineStart, self.highlightInLineEnd
            else:
                inLineStart, inLineEnd = self.highlightInLineEnd, self.highlightInLineStart

            self.highlightedText = [self.text[lineStart][inLineStart:]]
            self.highlightedText += self.text[lineStart + 1: lineEnd]
            self.highlightedText += [self.text[lineEnd][:inLineEnd]]

    def resetHighlight(self) -> None:
        self.highlightInLineStart = self.highlightInLineEnd = 0
        self.highlightLineStart = self.highlightLineEnd = 0
        self.highlightedText = []

    def shiftLines(self) -> None:
        if len(self.text[self.selectedLine]) > 0 and ord(self.text[self.selectedLine][-1]) == 10:
            return

        flag = False
        for lineIndex in range(self.selectedLine, len(self.text) - 1):
            while not self.maxWidthReached(self.text[lineIndex]):
                if not self.isEmpty2DSequence(self.text[lineIndex + 1]):
                    char = self.text[lineIndex + 1][0]

                    self.insertCharInText(lineIndex, len(self.text[lineIndex]), char)

                    del self.text[lineIndex + 1][0]

                else:
                    del self.text[lineIndex + 1]
                    flag = True
                    break
                if flag:
                    break

    def insertCharInText(self, lineIndex: int, inLineIndex: int, char: str) -> None:
        try:
            self.text[lineIndex].insert(inLineIndex, char)
        except IndexError:
            self.text.append([char])

    def eraseSpecialChar(self):
        if self.text[self.selectedLine]:
            while self.cursorPosition > 0 \
                    and self.isSpecialChar(self.text[self.selectedLine][self.cursorPosition - 1]):
                del self.text[self.selectedLine][self.cursorPosition - 1]
                self.cursorPosition -= 1

    def skipSpecialChar(self):
        if self.text[self.selectedLine]:
            while self.cursorPosition > 0 \
                    and self.isSpecialChar(self.text[self.selectedLine][self.cursorPosition - 1]):
                self.cursorPosition = max(0, self.cursorPosition - 1)

    def getLineX(self, line: list[str]) -> list[float]:
        x = [self._x + self.textOffsetLeft]

        for charIndex in range(len(line)):
            char = line[charIndex]

            if self.isSpecialChar(char):
                continue

            textWidth = self.font.size(line[charIndex])[0]
            x.append(x[-1] + textWidth)
        return x

    def getHighlightedRect(self, lineIndex: int, inLineStart: int, inLineEnd: int) -> \
            list[tuple[float, float, float, float]]:
        x = self.getLineX(self.text[lineIndex])

        highlightedRects = []
        for charIndex in range(len(self.text[lineIndex])):
            char = self.text[lineIndex][charIndex]

            if self.isSpecialChar(char):
                continue

            textWidth = self.font.size(char)[0]

            if inLineStart <= charIndex < inLineEnd:
                highlightedRects.append(
                    (x[charIndex], self._y + self.textOffsetTop + self.fontSize * lineIndex,
                     textWidth, self.fontSize)
                )

        return highlightedRects

    def maxWidthReached(self, line: list[str]) -> bool:
        x = self.getLineX(line)
        return x[-1] > self._x + self._width - self.textOffsetRight - self.textOffsetLeft

    def setCursorPositionAfterMouseEvent(self, x: int) -> None:
        coord = self.getLineX(self.text[self.selectedLine])

        for charIndex in range(len(self.text[self.selectedLine]) - 1):
            char1 = self.text[self.selectedLine][charIndex]
            char2 = self.text[self.selectedLine][charIndex + 1]

            if any(char for char in (char1, char2) if self.isSpecialChar(char)):
                continue

            charWidth1 = self.font.size(char1)[0]
            charWidth2 = self.font.size(char2)[0]

            x1 = charWidth1 + coord[charIndex]
            x2 = charWidth2 + x1

            if x1 - charWidth1 / 2 <= x <= x2 + charWidth2 / 2:
                self.cursorPosition = charIndex + 1

        if self.text[self.selectedLine]:
            if x < coord[0] + self.font.size(self.text[self.selectedLine][0])[0] / 2:
                self.cursorPosition = 0
            elif x > coord[-1] - self.font.size(self.text[self.selectedLine][-1])[0] / 2:
                self.cursorPosition = len(self.text[self.selectedLine])

    def setSelectedLineAfterMouseEvent(self, y: int) -> None:
        coord = [self._y + self.textOffsetTop]

        for lineIndex in range(len(self.text)):
            if coord[-1] <= y <= coord[-1] + self.fontSize:
                self.selectedLine = lineIndex
            coord.append(coord[-1] + self.fontSize)

        if y < coord[0] + self.fontSize / 2:
            self.selectedLine = 0
        elif y > coord[-1] + self.fontSize / 2:
            self.selectedLine = len(self.text) - 1

    def getValidHighlightLineIndexes(self) -> tuple[int, int]:
        startIndex = min(self.highlightLineStart, self.highlightLineEnd)
        endIndex = max(self.highlightLineStart, self.highlightLineEnd)
        return startIndex, endIndex

    def getValidHighlightInLineIndexes(self) -> tuple[int, int]:
        startIndex = min(self.highlightInLineStart, self.highlightInLineEnd)
        endIndex = max(self.highlightInLineStart, self.highlightInLineEnd)
        return startIndex, endIndex

    def copyHighlightedText(self) -> None:
        text = ''
        for line in self.highlightedText:
            text += ''.join(line)
        pyperclip.copy(text)

    @staticmethod
    def isSpecialChar(char: str) -> bool:
        return 0 <= ord(char) <= 31 or ord(char) == 127

    @staticmethod
    def isEmpty2DSequence(sequence: Iterable[Iterable]) -> bool:  # It's not a good name for a function.
        return not any(element for element in sequence)


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
