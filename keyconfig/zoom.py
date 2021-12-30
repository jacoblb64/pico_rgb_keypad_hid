import time
from constants import *
from adafruit_hid.keycode import Keycode

class ZoomKeypad():
    #--- OPTIONAL METHODS ---
    def zoomIntro(self, frameIndex):
        global image
        frameArray = [0, 1, 2, 3, 6, 9, 12, 13, 14, 15, 4, 5, 7, 8, 10, 11]
        if frameIndex >= len(frameArray):
            return
        index = frameArray[frameIndex]
        self.setKeyColour(index, self.IMAGE[index])

    #------------------------
    #--- REQUIRED METHODS ---
    IMAGE = [
        COLOUR_WHITE, COLOUR_WHITE, COLOUR_WHITE, COLOUR_WHITE,
        COLOUR_BLUE, COLOUR_BLUE, COLOUR_WHITE, COLOUR_BLUE,
        COLOUR_BLUE, COLOUR_WHITE, COLOUR_BLUE, COLOUR_BLUE,
        COLOUR_WHITE, COLOUR_WHITE, COLOUR_WHITE, COLOUR_WHITE
    ]

    def loop(self):
        if self.startAnimationTime > 0:
            estimatedFrame = int((timeInMillis() - self.startAnimationTime) / (ANIMATION_FRAME_MILLIS * 2))
            if estimatedFrame > self.currentFrame:
                # render new animation frame
                self.zoomIntro(self.frameIndex)
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
        print("switched to zoom keypad")

    def resetColours(self, colours):
        for key in range(BUTTON_COUNT):
            if isinstance(colours, int):
                self.setKeyColour(key, colours)
            elif len(colours) == BUTTON_COUNT:
                self.setKeyColour(key, colours[key][0])

    def handleEvent(self, keyIndex, event):
        if event & EVENT_SINGLE_PRESS:
            print("  ~~> [", keyIndex, "] single press")
            self.introduce()
            self.resetColours(self.getKeyColours())
        elif event & EVENT_DOUBLE_PRESS:
            print("  ~~> [", keyIndex, "] double press")
        elif event & EVENT_LONG_PRESS:
            print("  ~~> [", keyIndex, "] long press")
        elif event & EVENT_EXTRA_LONG_PRESS:
            print("  ~~> [", keyIndex, "] extra long press")
        if event & EVENT_KEY_UP:
            print("    ~~> [", keyIndex, "] key up")
        if event & EVENT_KEY_DOWN:
            print("    ~~> [", keyIndex, "] key down")
    #------------------------
