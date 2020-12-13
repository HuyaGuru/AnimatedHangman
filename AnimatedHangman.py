# standard modules
import pygame as pg
import pandas as pd
import random

# local module
from data import pygame_textinput as ti

# wordlist
words = pd.read_csv('./data/words.csv', header=None)

# lives
chances = 7

# word to be guessed
word = random.choice(words[0])
word = word.lower()
word = list(word)
word = pd.DataFrame(data=word)

# variable for blanks
blank = list()
for i in range(len(word)):
    blank.append("_")
blankDataframe = pd.DataFrame(data=blank)
del blank

# list for failed words
usedWords = list()

# game-module on
pg.init()

# grid co-ordinates
x = 800
y = 600

# surface
Screen = pg.display.set_mode([x, y])
pg.display.set_caption('AnimatedHangman')

# pygame_textinput variables
textInput = ti.TextInput(font_size=30, font_family='./data/JetBrainsMOno-Light.ttf')
inputOftext = str()
enablecheatmode = 0
textlastline = str()

# gamespeed variables
fps = 30
clock = pg.time.Clock()

# colors
white = [225, 225, 225]
black = [0, 0, 0]
grey = [169, 169, 169]

# font35 variable
font18 = pg.font.Font('./data/JetBrainsMono-Light.ttf', 18)
font35 = pg.font.Font('./data/JetBrainsMono-Light.ttf', 35)
title60 = pg.font.Font('./data/JetBrainsMono-Light.ttf', 60)

# animation sprite list
images = list()
for i in range(1, 8):
    text = './data/images/' + str(i) + '.png'
    image = pg.image.load(text)
    images.append(image)


# custom func for text rendering on main surface
def render(renderText, rectTopLeft, color, fontObject):
    textSurface = fontObject.render(renderText, True, color)
    textRect = textSurface.get_rect()
    textRect.topleft = rectTopLeft
    Screen.blit(textSurface, textRect)


class Button:
    def __init__(self, x, y, width, height, darkColor, lightColor, surface, text, textColor, fontObject):
        self.x = x
        self.y = y
        self.color = darkColor
        self.darkColor = darkColor
        self.lightColor = lightColor
        self.width = width
        self.height = height
        self.surface = surface
        self.text = text
        self.textColor = textColor
        self.fontObject = fontObject

    def createbutton(self):
        mouse = pg.mouse.get_pos()
        if self.x <= mouse[0] <= self.x + self.width and self.y <= mouse[1] <= self.y + self.height:
            self.color = self.lightColor
        else:
            self.color = self.darkColor
        button = pg.Rect(self.x, self.y, self.width, self.height)
        pg.draw.rect(self.surface, self.color, button)
        render(self.text, [self.x + 2, self.y], self.textColor, self.fontObject)


startButton = Button(345, 390, 110, 50, black, grey, Screen, None, white, font35)

stage = 1

# gameloop on
while True:
    # background
    Screen.fill(white)

    mouse = pg.mouse.get_pos()

    events = pg.event.get()

    # exit condition
    for event in events:
        if event.type == pg.QUIT:
            pg.quit()
            quit()
        if stage == 1:
            if event.type == pg.MOUSEBUTTONDOWN:
                if startButton.x <= mouse[0] <= startButton.x + startButton.width and startButton.y <= mouse[
                    1] <= startButton.y + startButton.height:
                    stage = 2
                else:
                    pass

    if stage == 1:
        text = 'Hangman'
        render(text, [x // 2 - 115, y // 2 - 160], black, title60)
        startButton.text = 'start'
        startButton.createbutton()

    if stage == 2:

        text = 'You get ' + str(chances) + ' chances to guess the word, with each wrong guess hangman gets'
        render(text, [10, 40], black, font18)

        text = 'closer to his demise.'
        render(text, [10, 70], black, font18)

        text = 'Chances : ' + str(chances)
        render(text, [10, 100], black, font18)

        text = 'Used words : '
        render(text, [10, 130], black, font18)

        textX = 130
        for i in usedWords:
            text = i
            render(text, [textX, 130], black, font18)
            textX += 15

        text = "Your word : "
        render(text, [10, 160], black, font18)

        # cheatmode on condition
        if enablecheatmode == 1:
            textX = 10
            for i in word[0]:
                text = i
                render(text, [textX, 190], black, font18)
                textX += 15

        # displaying blanks
        textX = 10
        for i in blankDataframe[0]:
            text = i
            render(text, [textX, 210], black, font18)
            textX += 15

        text = 'Enter Letter : '
        render(text, [10, 240], black, font18)

        # losing condition
        if chances == 0:
            enablecheatmode = 1
            textlastline = 'You Lost!'
            render(textlastline, [10, 270], black, font18)
            fps = 0

        # winning condition
        if blankDataframe[0].equals(word[0]):
            textlastline = 'You Saved Him!'
            render(textlastline, [10, 270], black, font18)
            fps = 0

        # text input
        Screen.blit(textInput.get_surface(), [175, 243])

        # checking Textinput() return condition
        if textInput.update(events):

            # intermediate input holding variable
            inputOftext = str(textInput.get_text()).lower()

            # cheatmode off condition
            if inputOftext != 'cheatmode':

                # user letter input
                guess = inputOftext[0]
                guess = guess.lower()

                # finding boolean filter of user-letter in the chosen word
                check = word[0].str.contains(guess)

                # making index tuple from boolean filter
                workingwordset = word[0][check].index.tolist()

                # if index tuple is a non-empty list
                if workingwordset:
                    textlastline = None
                    for i in workingwordset:
                        # replacing the values via index tuple to the actual guess
                        blankDataframe[0][i] = guess

                # if index-tuple is an empty list
                else:

                    # if the guessed letter isn't already used
                    if guess not in usedWords:
                        # lives -= 1
                        chances -= 1

                        # adding guessed letter to the used-words-list
                        usedWords.append(guess)

                        # deciding text value to be displayed for later use
                        textlastline = 'This letter doesnt exist in the word'

            else:
                enablecheatmode = 1
            # clearing the user text for another cycle
            textInput.clear_text()

        # for animation, number of lives remaining decide the image frame displayed
        if 7 - chances != 0:
            Screen.blit(images[7 - chances - 1], [300, 100])

        # clipping the earlier text to the surface
        if textlastline == 'This letter doesnt exist in the word':
            render(textlastline, [10, 270], black, font18)

    # refreshing all the respectives rects
    pg.display.update()

    # gameframe clock
    clock.tick(fps)
