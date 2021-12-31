import time
from lib.constants import *
from lib.adafruit_hid.keycode import Keycode

class NumpadKeypad():
    #--- OPTIONAL METHODS ---
    def numpadIntro(self, frame):
        if frame >= 4:
            return
        for row in range(4):
            index = (frame * 4) + row
            self.setKeyColour(index, self.IMAGE[index])

    #------------------------
    #--- REQUIRED METHODS ---
    IMAGE = [
        COLOUR_RED, COLOUR_ORANGE, COLOUR_YELLOW, COLOUR_GREEN,
        COLOUR_RED, COLOUR_ORANGE, COLOUR_YELLOW, COLOUR_VIOLET,
        COLOUR_RED, COLOUR_ORANGE, COLOUR_YELLOW, COLOUR_VIOLET,
        COLOUR_BLUE, COLOUR_BLUE, COLOUR_GREEN, COLOUR_WHITE
    ]

    def loop(self):
        if self.startAnimationTime > 0:
            estimatedFrame = int((timeInMillis() - self.startAnimationTime) / (ANIMATION_FRAME_MILLIS * 2))
            if estimatedFrame > self.currentFrame:
                # render new animation frame
                self.numpadIntro(self.frameIndex)
                self.frameIndex += 1
                # print("  ~~> Animation frame: ", estimatedFrame)
                self.currentFrame = estimatedFrame
                if self.frameIndex > self.maxFrame:
                    self.startAnimationTime = -1

    def getKeyColours(self):
        return (
            (darkVersion(self.IMAGE[0]),  COLOUR_CLEAR),
            (darkVersion(self.IMAGE[1]),  COLOUR_CLEAR),
            (darkVersion(self.IMAGE[2]),  COLOUR_CLEAR),
            (darkVersion(self.IMAGE[3]),  COLOUR_CLEAR),
            (darkVersion(self.IMAGE[4]),  COLOUR_CLEAR),
            (darkVersion(self.IMAGE[5]),  COLOUR_CLEAR),
            (darkVersion(self.IMAGE[6]),  COLOUR_CLEAR),
            (darkVersion(self.IMAGE[7]),  COLOUR_CLEAR),
            (darkVersion(self.IMAGE[8]),  COLOUR_CLEAR),
            (darkVersion(self.IMAGE[9]),  COLOUR_CLEAR),
            (darkVersion(self.IMAGE[10]), COLOUR_CLEAR),
            (darkVersion(self.IMAGE[11]), COLOUR_CLEAR),
            (darkVersion(self.IMAGE[12]), COLOUR_CLEAR),
            (darkVersion(self.IMAGE[13]), COLOUR_CLEAR),
            (darkVersion(self.IMAGE[14]), COLOUR_CLEAR),
            (darkVersion(self.IMAGE[15]), COLOUR_YELLOW)
        )

    def __init__(self, keyboard, keyboardLayout, setKeyColour):
        self.setKeyColour = setKeyColour
        self.keyboard = keyboard
        self.keyboardLayout= keyboardLayout

    def introduce(self):
        self.resetColours(COLOUR_OFF)
        self.startAnimationTime = timeInMillis()
        self.currentFrame = -1
        self.maxFrame = 16
        self.frameIndex = 0

    def resetColours(self, colours):
        for key in range(BUTTON_COUNT):
            if isinstance(colours, int):
                self.setKeyColour(key, colours)
            elif len(colours) == BUTTON_COUNT:
                self.setKeyColour(key, colours[key][0])

    def handleEvent(self, keyIndex, event):
        button_map = {
            0: Keycode.KEYPAD_SEVEN,
            1: Keycode.KEYPAD_EIGHT,
            2: Keycode.KEYPAD_NINE,
            4: Keycode.KEYPAD_FOUR,
            5: Keycode.KEYPAD_FIVE,
            6: Keycode.KEYPAD_SIX,
            8: Keycode.KEYPAD_ONE,
            9: Keycode.KEYPAD_TWO,
            10: Keycode.KEYPAD_THREE,
            12: Keycode.KEYPAD_ZERO,
            13: Keycode.KEYPAD_ZERO,

            3: Keycode.KEYPAD_PLUS,
            
            7: Keycode.KEYPAD_ENTER,
            11: Keycode.KEYPAD_ENTER,
        }

        if event & EVENT_SINGLE_PRESS:
            print("  ~~> [", keyIndex, "] single press")

            if keyIndex == 14:
                self.introduce()
                self.resetColours(self.getKeyColours())

        elif event & EVENT_DOUBLE_PRESS:
            print("  ~~> [", keyIndex, "] double press")
        elif event & EVENT_LONG_PRESS:
            print("  ~~> [", keyIndex, "] long press")
        elif event & EVENT_EXTRA_LONG_PRESS:
            print("  ~~> [", keyIndex, "] extra long press")
        
        if event & EVENT_KEY_DOWN:
            print("    ~~> [", keyIndex, "] key down")

            if keyIndex in button_map:
                self.keyboard.press(button_map[keyIndex])

        if event & EVENT_KEY_UP:
            print("    ~~> [", keyIndex, "] key up")
            if keyIndex in button_map:
                self.keyboard.release(button_map[keyIndex])

    #------------------------
