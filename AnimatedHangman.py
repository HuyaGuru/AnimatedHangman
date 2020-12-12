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

# pygame_textinput variables
textInput = ti.TextInput(font_size=30)
inputOftext = str()

# gamespeed variables
fps = 30
clock = pg.time.Clock()

# colors
White = [225, 225, 225]
Black = [0, 0, 0]

# font variable
font = pg.font.Font('freesansbold.ttf', 18)

# animation sprite list
images = list()
for i in range(1, 8):
    text = './data/images/' + str(i) + '.png'
    image = pg.image.load(text)
    images.append(image)


# custom func for text rendering on main surface
def render(renderText, rectTopLeft):
    textSurface = font.render(renderText, True, Black)
    textRect = textSurface.get_rect()
    textRect.topleft = rectTopLeft
    Screen.blit(textSurface, textRect)


# gameloop on
while True:

    events = pg.event.get()

    # exit condition
    for event in events:
        if event.type == pg.QUIT:
            pg.quit()
            quit()

    # background
    Screen.fill(White)

    text = '--Hangman--'
    render(text, [10, 10])

    text = 'You get ' + str(chances) + ' chances to guess the word, with each wrong guess hangman gets closer to'
    render(text, [10, 40])

    text = 'his demise.'
    render(text, [10, 70])

    text = 'Chances : ' + str(chances)
    render(text, [10, 100])

    text = 'Used words : '
    render(text, [10, 130])

    textX = 130
    for i in usedWords:
        text = i
        render(text, [textX, 130])
        textX += 15

    text = "Your word : "
    render(text, [10, 160])

    # cheatmode on condition
    if inputOftext == 'cheatmode':
        textX = 10
        for i in word[0]:
            text = i
            render(text, [textX, 190])
            textX += 15

    textX = 10
    for i in blankDataframe[0]:
        text = i
        render(text, [textX, 210])
        textX += 15

    text = 'Enter Letter : '
    render(text, [10, 240])

    # losing condition
    if chances == 0:
        text = 'You Lost!'
        render(text, [10, 270])
        fps = 0

    # winning condition
    if blankDataframe[0].equals(word[0]):
        text = 'You Saved Him!'
        render(text, [10, 270])
        fps = 0

    # text input
    Screen.blit(textInput.get_surface(), [140, 240])

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
                    text = 'This letter doesnt exist in the word'

        # clearing the user text for another cycle
        textInput.clear_text()

    # for animation, number of lives remaining decide the image frame displayed
    if 7 - chances != 0:
        Screen.blit(images[7 - chances - 1], [300, 100])

    # clipping the earlier text to the surface
    if text == 'This letter doesnt exist in the word':
        render(text, [10, 260])

    # refreshing all the respectives rects
    pg.display.update()

    # gameframe clock
    clock.tick(fps)
