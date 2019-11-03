from cmu_112_graphics import *
from texttospeech import *
from tkinter import *
import random, math
from PIL import Image
import string

'''
Goal: make educational app for children with dyslexia
Features:
- generate random words with confusing vowels and playback separate phonetic sounds
    - highlight; lots of colors
- play audio of words that are hard to spell, and then they enter it, and we spell check
- playback audio with slower pronounciation of a word
- keyPressed for each keyboard key that plays the sound whenever we press it
- words describing tactile things you also display the image (e.g. tree)
'''


class SplashScreenMode(Mode):
    def redrawAll(self, canvas):
        self.font = "Arial 26 bold"
        canvas.create_rectangle(450, 200, 750, 300, fill="green")
        canvas.create_rectangle(450, 350, 750, 450, fill="blue")
        canvas.create_rectangle(450, 500, 750, 600, fill="red")
        canvas.create_rectangle(450, 650, 750, 750, fill="orange")
        canvas.create_text(600, 50, text="Welcome to Read112!", font=self.font)
        canvas.create_text(600, 100, text="Click on an activity to get started!", font=self.font)
        canvas.create_text(600, 250, text="Spelling", font=self.font, fill="white")
        canvas.create_text(600, 400, text="Typing", font=self.font, fill="white")
        canvas.create_text(600, 550, text="Images", font=self.font, fill="white")
        canvas.create_text(600, 700, text="Picture Match", font=self.font, fill="white")

    def mousePressed(self, event):
        if (event.x >= 450) and (event.x <= 750):
            if (event.y >= 200) and (event.y <= 300): #Spelling
                self.app.setActiveMode(self.app.spellingMode)
            elif (event.y >= 350) and (event.y <= 450): #Typing
                self.app.setActiveMode(self.app.typingMode)
            elif (event.y >= 500) and (event.y <= 600): #Images
                self.app.setActiveMode(self.app.imageMode)
            elif (event.y >= 650) and (event.y <= 750): #Picture Match
                self.app.setActiveMode(self.app.pictureMatchMode)

class SpellingMode(Mode):
    def appStarted(self):
        self.tts = TextToSpeech()
        self.words = ["cat", "start", "stare"]
        urlSpeaker = "https://tinyurl.com/yyv3eflw"
        self.imageSpeaker = self.scaleImage(self.loadImage(urlSpeaker), 1/8)
        self.cacheSpeaker = ImageTk.PhotoImage(self.imageSpeaker)
        self.inputtedString = ''
        self.wordIndex = 0
        self.currentWord = self.words[self.wordIndex]
        self.isDone = False
        self.message = ''
    
    def initWord(self):
        self.inputtedString = ''
        self.wordIndex += 1
        if self.wordIndex < len(self.words):
            self.currentWord = self.words[self.wordIndex]
        else:
            self.isDone = True

    def keyPressed(self, event):
        if event.key == "Enter":
            self.checkSpelling()
        elif event.key == "Delete":
            self.inputtedString = self.inputtedString[:-1]
        else:
            self.inputtedString = self.inputtedString + event.key

    def checkSpelling(self):
        if self.inputtedString == self.currentWord:
            self.message = "Yay!"
        else:
            self.message = f'The correct spelling is: {self.currentWord}'
        self.initWord()

    def redrawAll(self, canvas):
        canvas.create_rectangle(0, 0, self.width, self.height, fill=self.app.offwhite)
        canvas.create_oval(5, 5, 100, 50, fill=self.app.maroon)
        canvas.create_text(52, 27, text="Back", font=self.app.font, fill=self.app.offwhite)
        canvas.create_text(600, 100, text="Click on the speaker icon and type the word you hear.", font=self.app.font)
        canvas.create_image(600, 200, image=self.cacheSpeaker)
        canvas.create_rectangle(500, 300, 700, 325, fill="gray", width=2)
        canvas.create_text(600, 315, text=self.inputtedString, fill=self.app.offwhite)
        canvas.create_text(600, 500, text=self.message, font=self.app.font)

    def mousePressed(self, event):
        if (event.x > 5) and (event.x < 100) and (event.y > 5) and (event.y < 50):
            self.app.setActiveMode(self.app.splashMode)
        elif (event.x > 550) and (event.x < 650) and (event.y > 150) and (event.y < 250):
            self.tts.get_pronunciation(self.currentWord)


class TypingMode(Mode):
    def appStarted(self):
        self.tts = TextToSpeech()
        self.wordDict = dict()
        self.initWordsDict()
        self.initNewWord()

    def initWordsDict(self):
        self.words = ["tree", "cat", "cut", "dog", "bog", "start", "stare", "glass", "gas"]
        for word in self.words:
            self.wordDict[word] = list(word)
        
    def initNewWord(self):
        self.currentWord = self.words[random.randint(0, len(self.words) - 1)]
        self.letterVals = [False] * len(self.currentWord)
        self.index = 0

    def keyPressed(self, event):
        for letter in string.ascii_lowercase:
            if event.key == letter:
                self.tts.get_pronunciation(letter)
        self.checkLetter(event.key)

    def checkLetter(self, userLetter):
        letters = self.wordDict[self.currentWord]
        if userLetter == letters[self.index]:
            self.letterVals[self.index] = True
        self.index += 1
        if self.index == len(self.currentWord):
            self.initNewWord()

    def drawLetters(self, word, canvas):
        font = "Arial 120 bold"
        letterMargin = self.width // (len(self.currentWord) + 2)
        for i in range(len(self.currentWord)):
            if self.letterVals[i] == False: 
                fill = "blue"
            else: fill = "green"
            canvas.create_text(letterMargin * (i + 1), self.height // 2, 
                               text=self.wordDict[self.currentWord][i],
                               fill=fill, font=font)

    def redrawAll(self, canvas):
        canvas.create_rectangle(0, 0, self.width, self.height, fill=self.app.offwhite)
        canvas.create_oval(5, 5, 100, 50, fill=self.app.maroon)
        canvas.create_text(52, 27, text="Back", font=self.app.font, fill=self.app.offwhite)
        canvas.create_text(self.width // 2, 40, font=self.app.font, text='''
        Type each letter you see on the screen and follow along with the pronunciation!
        ''')
        self.drawLetters(self.currentWord, canvas)

    def mousePressed(self, event):
        if (event.x > 5) and (event.x < 100) and (event.y > 5) and (event.y < 50):
            self.app.setActiveMode(self.app.splashMode)


class ImageMode(Mode):
    def appStarted(mode):
        mode.message = 'Click on the mouse to enter a kind of animal'
        mode.image=mode.app.loadImage('https://tinyurl.com/y44ge5bv')
    
    def mousePressed(mode, event):
        if (event.x > 5) and (event.x < 100) and (event.y > 5) and (event.y < 50):
            mode.app.setActiveMode(mode.app.splashMode)
        animal = mode.getUserInput('What is an animal \
            you would like to know more about')
        if (animal == None):
            mode.message = 'You canceled!'
        else:
            mode.message = f'Here is a {animal}!'
            if (animal=="tiger"):
                mode.image=mode.app.loadImage('https://tinyurl.com/y4d33q9r')
            if (animal=="cat"):
                mode.image=mode.app.loadImage('https://tinyurl.com/y4cjpxxp')
            if (animal=="chicken"):
                mode.image=mode.app.loadImage('https://tinyurl.com/yxzd7qky')
            if (animal=="dog"):
                mode.image=mode.app.loadImage('https://tinyurl.com/y7dghhz3')
            if (animal=="duck"):
                mode.image=mode.app.loadImage('https://tinyurl.com/yxwfjqwp') 
            if (animal=="fish"):
                mode.image=mode.app.loadImage('https://tinyurl.com/y4x5lqch')
            if (animal=="frog"):
                mode.image=mode.app.loadImage('https://tinyurl.com/y2atcte5')
            if animal=="cow":
                mode.image=mode.app.loadImage('https://tinyurl.com/y2pumuau')
            if animal=="horse":
                mode.image=mode.app.loadImage('https://tinyurl.com/y5yndcdz')
            if animal=="mouse":
                mode.image=mode.app.loadImage
            if animal=="pig":
                mode.image=mode.app.loadImage
            if animal=="rabbit":
                mode.image=mode.app.loadImage('https://tinyurl.com/yyq284k8')
            if animal=="elephant":
                mode.image=mode.app.loadImage('https://tinyurl.com/y2az3r6j')
            else:
                mode.message="Sorry, we don't have this animal"
                
    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill=mode.app.offwhite)
        canvas.create_oval(5, 5, 100, 50, fill=mode.app.maroon)
        canvas.create_text(52, 27, text="Back", font=mode.app.font, fill=mode.app.offwhite)
        font = 'Arial 26 bold'
        canvas.create_text(mode.width/2, 20, text=mode.message, font=font)
        canvas.create_image(400, 400, image=ImageTk.PhotoImage(mode.image))
        

def rgb(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)

class Letter(object):
    def __init__(mode, x, y):
        mode.x = x
        mode.y = y

class PictureMatchMode(Mode):
    def appStarted(mode):
        url1 = 'http://www.pngmart.com/files/3/Singing-PNG-HD.png'
        sing = mode.loadImage(url1)
        mode.sing = mode.scaleImage(sing, .35)
        mode.blank1 = '_'
        mode.blank2 = '_'
        mode.startG()
        mode.startN()
        mode.isDraggingG = False
        mode.isDraggingN = False
    
    def startG(mode):
        mode.G = Letter(.4*mode.width, .8*mode.height)
    
    def startN(mode):
        mode.N = Letter(.6*mode.width, .8*mode.height)
    
    def mousePressed(mode, event):
        if ((mode.G.x-20) <= event.x <= (mode.G.x+20)) and ((mode.G.y-20) <= event.y <= (mode.G.y+20)):
            mode.isDraggingG = True
        if ((mode.N.x-20) <= event.x <= (mode.N.x+20)) and ((mode.N.y-20) <= event.y <= (mode.N.y+20)):
            mode.isDraggingN = True
        if (event.x > 5) and (event.x < 100) and (event.y > 5) and (event.y < 50):
            mode.app.setActiveMode(mode.app.splashMode)

    def mouseDragged(mode, event):
        if mode.isDraggingG == True:
            mode.G.x = event.x
            mode.G.y = event.y
        if mode.isDraggingN == True:
            mode.N.x = event.x
            mode.N.y = event.y
    
    def mouseReleased(mode, event):
        if (690 <= event.x == mode.G.x <= 770) and ((.5*mode.height-50) <= event.y == mode.G.y <= (.5*mode.height+80)) \
            or (mode.G.x == mode.width + 100 or mode.G.y == mode.height + 100):
            mode.isDraggingG = False
            mode.G.x = mode.width + 100
            mode.G.y = mode.height + 100
            mode.blank2 = 'g'
        else:
            mode.startG()
        if (600 <= event.x == mode.N.x <= 660) and ((.5*mode.height-30) <= event.y == mode.N.y <= (.5*mode.height+50)) \
            or (mode.N.x == mode.width + 100 or mode.N.y == mode.height + 100):
            mode.isDraggingN = False
            mode.N.x = mode.width + 100
            mode.N.y = mode.height + 100
            mode.blank1 = 'n'
        else:
            mode.startN()

    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill=mode.app.offwhite)
        canvas.create_rectangle(0,0,mode.width,mode.height,fill=rgb(230,230,250))
        canvas.create_oval(5, 5, 100, 50, fill=mode.app.maroon)
        canvas.create_text(52, 27, text="Back", font=mode.app.font, fill=mode.app.offwhite)
        canvas.create_image(mode.width/2, mode.height/5, image=ImageTk.PhotoImage(mode.sing))
        canvas.create_text(mode.width/2, .5*mode.height, text=f's i {mode.blank1} {mode.blank2}', \
                           font='Arial 80 bold', fill=rgb(139,0,139))
        canvas.create_text(mode.G.x, mode.G.y, text='g', font='Arial 80 bold', fill=rgb(139,0,139))
        canvas.create_text(mode.N.x, mode.N.y, text='n', font='Arial 80 bold', fill=rgb(139,0,139))
    

class MyModalApp(ModalApp):
    def appStarted(self):
        self.splashMode = SplashScreenMode()
        self.spellingMode = SpellingMode()
        self.typingMode = TypingMode()
        self.imageMode = ImageMode()
        self.pictureMatchMode = PictureMatchMode()
        self.setActiveMode(self.splashMode)
        self.styleInit()

    def styleInit(self):
        self.font = "Arial 26 bold"
        self.offwhite = "#%02x%02x%02x" % (255, 250, 241)
        self.maroon = "#%02x%02x%02x" % (176, 48, 96)

MyModalApp(width=1200, height=800)
