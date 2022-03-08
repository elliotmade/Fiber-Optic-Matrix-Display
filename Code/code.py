# function to shift a pixel in the grid (or the whole grid?) left right up down diagonal and by distance




import time
import board
# from analogio import AnalogIn
import neopixel
from digitalio import DigitalInOut, Direction, Pull
import random
import gc



debug = False

pixel_pin = board.GP15

num_pixels = 256
globalBrightness = 0.1

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1, auto_write=False)





#Predefined colors
OFF = [0, 0, 0]
RED = [255, 0, 0]
ORANGE = [255,128,0]
YELLOW = [255, 255, 0]
CHARTREUSE = [128,255,0]
GREEN = [0, 255, 0]
SPRINGGREEN = [0,255,128]
CYAN = [0,255,255]
BLUE = [0, 0, 255]
PURPLE = [128,0,255]
VIOLET = [255,0,255]
MAGENTA = [255,0,128]
WHITE = [255,255,255]

colorList = [RED,ORANGE,YELLOW,CHARTREUSE,GREEN,SPRINGGREEN,CYAN,BLUE,PURPLE,VIOLET,MAGENTA,WHITE]
colorCount = len(colorList)

globalColor = RED
globalColorIndex = 0

def constrain0to1(val):
            if val < 0: val = 0
            if val > 1: val = 1
            return val

def constrain(val, min, max, wrap = False):
    if val < min and wrap == True: val = max
    if val < min: val = min
    if val > max and wrap == True: val = min
    if val > max: val = max
    if debug == True: print(val)
    return val

class pixelBuffer:
    def __init__(self, pixelCount):

        #make a big buffer of "apixel"s that can be acted on in neat ways.  turn this into a class
        self.buffer = []
        for i in range(pixelCount):
            self.buffer.append(self.apixel())
        
    

    def setColorAll(self, colorIndex):
        #directly set the color, don't use setcolor in case it needs to remain off
        for p in self.buffer:
            p.setColor(colorIndex)
        if debug == True: print("All pixels set to new color: " + str(colorIndex))

    def setBrightnessAll(self, brightness):
        for p in self.buffer:
            p.setBrightness(constrain0to1(brightness))
        if debug == True: print("All pixels set to new brightness: " + str(brightness))

    def fadeByPercentAll(self, percent):
        for p in self.buffer:
            p.fadeBy(percent)
        if debug == True: print("All pixels faded by: " + str(percent))

    def clearAll(self):
        for p in self.buffer:
            p.off()
        if debug == True: print("Clearing all pixels")


    chars = {
    "A":   [[0,0,1,0,0],
            [0,1,0,1,0],
            [1,0,0,0,1],
            [1,0,0,0,1],
            [1,1,1,1,1],
            [1,0,0,0,1],
            [1,0,0,0,1]
            ],
    "B":   [[1,1,1,1,0],
            [0,1,0,0,1],
            [0,1,0,0,1],
            [0,1,1,1,0],
            [0,1,0,0,1],
            [0,1,0,0,1],
            [1,1,1,1,0]
            ],
    "C":   [[0,1,1,1,0],
            [1,0,0,0,1],
            [1,0,0,0,0],
            [1,0,0,0,0],
            [1,0,0,0,0],
            [1,0,0,0,1],
            [0,1,1,1,0]
            ],
    "D":   [[1,1,1,1,0],
            [0,1,0,0,1],
            [0,1,0,0,1],
            [0,1,0,0,1],
            [0,1,0,0,1],
            [0,1,0,0,1],
            [1,1,1,1,0]
            ],
    "E":   [[1,1,1,1,1],
            [1,0,0,0,0],
            [1,0,0,0,0],
            [1,1,1,1,0],
            [1,0,0,0,0],
            [1,0,0,0,0],
            [1,1,1,1,1]
            ],
    "F":   [[1,1,1,1,1],
            [1,0,0,0,0],
            [1,0,0,0,0],
            [1,1,1,1,0],
            [1,0,0,0,0],
            [1,0,0,0,0],
            [1,0,0,0,0]
            ],
    "G":   [[0,1,1,1,0],
            [1,0,0,0,1],
            [1,0,0,0,0],
            [1,0,0,1,1],
            [1,0,0,0,1],
            [1,0,0,0,1],
            [0,1,1,1,1]
            ],
    "H":   [[1,0,0,0,1],
            [1,0,0,0,1],
            [1,0,0,0,1],
            [1,1,1,1,1],
            [1,0,0,0,1],
            [1,0,0,0,1],
            [1,0,0,0,1]
            ],
    "I":   [[1,1,1],
            [0,1,0],
            [0,1,0],
            [0,1,0],
            [0,1,0],
            [0,1,0],
            [1,1,1]
            ],
    "J":   [[0,0,1,1,1],
            [0,0,0,1,0],
            [0,0,0,1,0],
            [0,0,0,1,0],
            [0,0,0,1,0],
            [1,0,0,1,0],
            [0,1,1,0,0]
            ],
    "K":   [[1,0,0,0,1],
            [1,0,0,1,0],
            [1,0,1,0,0],
            [1,1,0,0,0],
            [1,0,1,0,0],
            [1,0,0,1,0],
            [1,0,0,0,1]
            ],
    "L":   [[1,0,0,0,0],
            [1,0,0,0,0],
            [1,0,0,0,0],
            [1,0,0,0,0],
            [1,0,0,0,0],
            [1,0,0,0,0],
            [1,1,1,1,1]
            ],
    "M":   [[1,0,0,0,1],
            [1,1,0,1,1],
            [1,0,1,0,1],
            [1,0,1,0,1],
            [1,0,0,0,1],
            [1,0,0,0,1],
            [1,0,0,0,1]
            ],
    "N":   [[1,0,0,0,1],
            [1,0,0,0,1],
            [1,1,0,0,1],
            [1,0,1,0,1],
            [1,0,0,1,1],
            [1,0,0,0,1],
            [1,0,0,0,1]
            ],
    "O":   [[0,1,1,1,0],
            [1,0,0,0,1],
            [1,0,0,0,1],
            [1,0,0,0,1],
            [1,0,0,0,1],
            [1,0,0,0,1],
            [0,1,1,1,0]
            ],
    "P":   [[1,1,1,1,0],
            [1,0,0,0,1],
            [1,0,0,0,1],
            [1,1,1,1,0],
            [1,0,0,0,0],
            [1,0,0,0,0],
            [1,0,0,0,0]
            ],
    "Q":   [[0,1,1,1,0],
            [1,0,0,0,1],
            [1,0,0,0,1],
            [1,0,0,0,1],
            [1,0,1,0,1],
            [1,0,0,1,0],
            [0,1,1,0,1]
            ],
    "R":   [[1,1,1,1,0],
            [1,0,0,0,1],
            [1,0,0,0,1],
            [1,1,1,1,0],
            [1,0,1,0,0],
            [1,0,0,1,0],
            [1,0,0,0,1]
            ],
    "S":   [[0,1,1,1,0],
            [1,0,0,0,1],
            [1,0,0,0,0],
            [0,1,1,1,0],
            [0,0,0,0,1],
            [1,0,0,0,1],
            [0,1,1,1,0]
            ],
    "T":   [[1,1,1,1,1],
            [0,0,1,0,0],
            [0,0,1,0,0],
            [0,0,1,0,0],
            [0,0,1,0,0],
            [0,0,1,0,0],
            [0,0,1,0,0]
            ],
    "U":   [[1,0,0,0,1],
            [1,0,0,0,1],
            [1,0,0,0,1],
            [1,0,0,0,1],
            [1,0,0,0,1],
            [1,0,0,0,1],
            [0,1,1,1,0]
            ],
    "V":  [[1,0,0,0,1],
            [1,0,0,0,1],
            [1,0,0,0,1],
            [1,0,0,0,1],
            [1,0,0,0,1],
            [0,1,0,1,0],
            [0,0,1,0,0]
            ],
    "W":   [[1,0,0,0,1],
            [1,0,0,0,1],
            [1,0,0,0,1],
            [1,0,0,0,1],
            [1,0,1,0,1],
            [1,0,1,0,1],
            [0,1,0,1,0]
            ],
    "X":   [[1,0,0,0,1],
            [1,0,0,0,1],
            [0,1,0,1,0],
            [0,0,1,0,0],
            [0,1,0,1,0],
            [1,0,0,0,1],
            [1,0,0,0,1]
            ],
    "Y":   [[1,0,0,0,1],
            [1,0,0,0,1],
            [1,0,0,0,1],
            [0,1,0,1,0],
            [0,0,1,0,0],
            [0,0,1,0,0],
            [0,0,1,0,0]
            ],
    "Z":   [[1,1,1,1,1],
            [0,0,0,0,1],
            [0,0,0,1,0],
            [0,0,1,0,0],
            [0,1,0,0,0],
            [1,0,0,0,0],
            [1,1,1,1,1]
            ],
    " ":        [[0],
                [0],
                [0],
                [0],
                [0],
                [0],
                [0]
                ],
    "0":   [[0,1,1,1,0],
            [1,0,0,0,1],
            [1,0,0,0,1],
            [1,0,0,0,1],
            [1,0,0,0,1],
            [1,0,0,0,1],
            [0,1,1,1,0]
            ],
    "1":   [[0,1,0], #add padding to 5 columns?
            [1,1,0],
            [0,1,0],
            [0,1,0],
            [0,1,0],
            [0,1,0],
            [1,1,1]
            ],
    "2":   [[0,1,1,1,0], 
            [1,0,0,0,1],
            [0,0,0,0,1],
            [0,0,1,1,0],
            [0,1,0,0,0],
            [1,0,0,0,0],
            [1,1,1,1,1]
            ],
    "3":   [[0,1,1,1,0],
            [1,0,0,0,1],
            [0,0,0,0,1],
            [0,0,1,1,0],
            [0,0,0,0,1],
            [1,0,0,0,1],
            [0,1,1,1,0]
            ],
    "4":   [[0,0,0,1,0],
            [0,0,1,1,0],
            [0,1,0,1,0],
            [1,0,0,1,0],
            [1,1,1,1,1],
            [0,0,0,1,0],
            [0,0,0,1,0]
            ],
    "5":   [[1,1,1,1,1],
            [1,0,0,0,0],
            [1,1,1,1,0],
            [0,0,0,0,1],
            [0,0,0,0,1],
            [1,0,0,0,1],
            [0,1,1,1,0]
            ], 
    "6":   [[0,0,1,1,0],
            [0,1,0,0,0],
            [1,0,0,0,0],
            [1,1,1,1,0],
            [1,0,0,0,1],
            [1,0,0,0,1],
            [0,1,1,1,0]
            ], 
    "7":   [[1,1,1,1,1],
            [0,0,0,0,1],
            [0,0,0,1,0],
            [0,0,1,0,0],
            [0,1,0,0,0],
            [0,1,0,0,0],
            [0,1,0,0,0]
            ], 
    "8":   [[0,1,1,1,0],
            [1,0,0,0,1],
            [1,0,0,0,1],
            [0,1,1,1,0],
            [1,0,0,0,1],
            [1,0,0,0,1],
            [0,1,1,1,0]
            ], 
    "9":   [[0,1,1,1,0],
            [1,0,0,0,1],
            [1,0,0,0,1],
            [0,1,1,1,1],
            [0,0,0,0,1],
            [0,0,0,1,0],
            [0,1,1,0,0]
            ], 
    "!":   [[1],
            [1],
            [1],
            [1],
            [1],
            [0],
            [1]
            ],
    "?":   [[0,1,1,1,0],
            [1,0,0,0,1],
            [0,0,0,0,1],
            [0,0,0,1,0],
            [0,0,1,0,0],
            [0,0,0,0,0],
            [0,0,1,0,0]
            ],
    ":":   [[0],
            [0],
            [1],
            [0],
            [1],
            [0],
            [0]
            ],          
    "temp": [[],
            [],
            [],
            [],
            [],
            [],
            []
            ],           
    #instead of on-off, there is special logic in the chartobuffer for colors in this case.  2 = white, 3 = red, 4 = blue, 5 = orange, 6 = cyan, 7 = pink          
    "fheart":  [[0,2,2,0,2,2,0],
                [2,3,3,2,3,3,2],
                [2,3,3,3,3,3,2],
                [2,3,3,3,3,3,2],
                [0,2,3,3,3,2,0],
                [0,0,2,3,2,0,0],
                [0,0,0,2,0,0,0]
                ],
    "hheart":  [[0,2,2,0,2,2,0],
                [2,3,3,2,0,0,2],
                [2,3,3,3,0,0,2],
                [2,3,3,3,0,0,2],
                [0,2,3,3,0,2,0],
                [0,0,2,3,2,0,0],
                [0,0,0,2,0,0,0]
                ],
    "eheart":  [[0,2,2,0,2,2,0],
                [2,0,0,2,0,0,2],
                [2,0,0,0,0,0,2],
                [2,0,0,0,0,0,2],
                [0,2,0,0,0,2,0],
                [0,0,2,0,2,0,0],
                [0,0,0,2,0,0,0]
                ],
    "ghostred":[[0,0,3,3,3,0,0],
                [0,3,3,3,3,3,0],
                [3,2,2,3,2,2,3],
                [3,4,2,3,4,2,3],
                [3,3,3,3,3,3,3],
                [3,3,3,3,3,3,3],
                [3,0,3,0,3,0,3]
                ],
    "ghostorange":[[0,0,5,5,5,0,0],
                [0,5,5,5,5,5,0],
                [5,2,2,5,2,2,5],
                [5,4,2,5,4,2,5],
                [5,5,5,5,5,5,5],
                [5,5,5,5,5,5,5],
                [5,0,5,0,5,0,5]
                ],
    "ghostcyan":[[0,0,6,6,6,0,0],
                [0,6,6,6,6,6,0],
                [6,2,2,6,2,2,6],
                [6,4,2,6,4,2,6],
                [6,6,6,6,6,6,6],
                [6,6,6,6,6,6,6],
                [6,0,6,0,6,0,6]
                ],
    "ghostpink":[[0,0,7,7,7,0,0],
                [0,7,7,7,7,7,0],
                [7,2,2,7,2,2,7],
                [7,4,2,7,4,2,7],
                [7,7,7,7,7,7,7],
                [7,7,7,7,7,7,7],
                [7,0,7,0,7,0,7]
                ],
    "ghostblue":[[0,0,4,4,4,0,0],
                [0,4,4,4,4,4,0],
                [4,2,2,4,2,2,4],
                [4,4,2,4,4,2,4],
                [4,4,4,4,4,4,4],
                [4,4,4,4,4,4,4],
                [4,0,4,0,4,0,4]
                ],
    
    }
    
    def charToBuffer(self, char, col):
        #put a character on to the grid, overwriting whatever was there, starting at an X position "col"
        #loop through each row of the char array, add an initial offset for each row. - each row is +35 from the previous.  So insert at col for the width of the character on row 1, add 35 and insert row 2, etc
        #need to handle a character partly off of the left side of the array?  Also right side?  Or do we care do do that with this function?  Leave it for one that can scroll a string?
        #5 = orange, 6 = cyan, 7 = pink
        for row in range(len(self.chars[char])):
            for column in range(len(self.chars[char][0])):
                currentPixel = column + col + row * 35
                if self.chars[char][row][column] == 0:
                    self.buffer[currentPixel].off()
                elif self.chars[char][row][column] == 2:
                    self.buffer[currentPixel].setColor(11, True)
                elif self.chars[char][row][column] == 3:
                    self.buffer[currentPixel].setColor(0, True)
                elif self.chars[char][row][column] == 4:
                    self.buffer[currentPixel].setColor(7, True)
                elif self.chars[char][row][column] == 5:
                    self.buffer[currentPixel].setColor(1, True)
                elif self.chars[char][row][column] == 6:
                    self.buffer[currentPixel].setColor(6, True)
                elif self.chars[char][row][column] == 7:
                    self.buffer[currentPixel].setColor(10, True)
                else:
                    self.buffer[currentPixel].on()
        if debug == True: print("Added " + char + "to buffer")

    def stringToTempBuffer(self, string, spacing = 1):
        #make a list of lists (7 rows, any number of columns)
        global globalColorIndex
        
        tempBuffer = [] 
        
        for letter in string:

            for row in range(len(self.chars[letter])):
                #print("Row")
                tempBuffer.append([])
                #make a row and populate it one column at a time
                for column in range(len(self.chars[letter][0])):
                    #print("Column")
                    if self.chars[letter][row][column] == 0:
                        tempBuffer[row].append(self.apixel()) #add an off pixel
                    elif self.chars[letter][row][column] == 1:
                        tempBuffer[row].append(self.apixel(colorIndex = globalColorIndex, active = True)) #add an on pixel in the global color (automatically inherited)
                    elif self.chars[letter][row][column] == 2:
                        tempBuffer[row].append(self.apixel(11, True))
                    elif self.chars[letter][row][column] == 3:
                        tempBuffer[row].append(self.apixel(0, True)) #red
                    elif self.chars[letter][row][column] == 4:
                        tempBuffer[row].append(self.apixel(7, True))
                    elif self.chars[letter][row][column] == 5:
                        tempBuffer[row].append(self.apixel(1, True))
                    elif self.chars[letter][row][column] == 6:
                        tempBuffer[row].append(self.apixel(6, True))
                    elif self.chars[letter][row][column] == 7:
                        tempBuffer[row].append(self.apixel(10, True))
                #print("Tempbuffer[0] len: " + str(len(tempBuffer[0])))
            if spacing > 0:
                for i in range(len(tempBuffer)):
                    #print("Space")
                    for j in range(spacing):
                        tempBuffer[i].append(self.apixel()) #add an off pixel to every row then go to next letter
                
            if debug == True: print("Added " + letter + "to temp buffer")

            #print("Tempbuffer len: " + str(len(tempBuffer)))
            #print("Tempbuffer[0] len: " + str(len(tempBuffer[0])))
            #print("Tempbuffer[1] len: " + str(len(tempBuffer[1])))
        return tempBuffer

    def scrollStringLeft(self, inputBuffer, extraColumns = 0): 
        #Scroll the contents of a 7 row high buffer from the right to left, for a certain number of columns
        #length of the buffer will leave the last column on the right edge of the thing.  Add 35 to scroll it all the way off again
        #this could be smoother if the input buffer was created on the fly one character at a time instead of all at once
        numColumns = len(inputBuffer[0]) + extraColumns
        #print("Numcolumns: " + str(numColumns))

        #just pop off the next pixel in each row of the temp buffer every iteration, until their len is 0?

        for i in range(numColumns):
            #print(str(i) + " out of " + str(numColumns))
            for col in range(35): #number of iterations for a single frame
                for row in range(7):
                    currentPixel = col + row * 35
                    if col < 34:
                        #copy the pixel to the right 
                        rightPixel =  currentPixel + 1
                        #print("Column: " + str(col) + " Current Pixel: " + str(currentPixel) + " Right Pixel: " + str(rightPixel))
                        self.copyPixel(rightPixel, currentPixel)
                    else:
                        #this is the right edge, so copy from tempbuffer or add a blank
                        if len(inputBuffer[row]) > 0:
                            #print("Copying a pixel out of the buffer")
                            self.copyPixel2(inputBuffer[row].pop(0), currentPixel)
                            
                        else:
                            #print("No pixel left in the buffer to copy")
                            self.buffer[currentPixel].off()
            bufferToGrid()
            refreshDisplay()

    def stringToBuffer(self, string, col = 0, spacing = 1):
        #add each character from the string to the buffer, moving over one blank column between, until the last character won't fit
        if debug == True: print("Sending string to buffer: " + string)
        curCol = col
        for letter in string:
            #send the letter
            self.charToBuffer(letter, curCol)
            #then offset for the next character column start
            curCol += len(self.chars[letter][0]) + spacing

    def copyPixel(self, source, dest):
        self.buffer[dest].active = self.buffer[source].active
        self.buffer[dest].curBrightness = self.buffer[source].curBrightness
        self.buffer[dest].colorIndex = self.buffer[source].colorIndex
        self.buffer[dest].color = self.buffer[source].color
        self.buffer[dest].rgb = self.buffer[source].rgb
        #this only works within the buffer, not between two different pixel objects
        
    def copyPixel2(self, source, dest):
        #this time source is a pixel object, dest is still the ID in the buffer of where to copy to
        self.buffer[dest].active = source.active
        self.buffer[dest].curBrightness = source.curBrightness
        self.buffer[dest].colorIndex = source.colorIndex
        self.buffer[dest].color = source.color
        self.buffer[dest].rgb = source.rgb

        if debug == True: print("Copied pixel " + str(source) + " to " + str(dest))

    def scrollDown(self, startCol = 0, numCols = 35, delay = .001):
        #scrolls whatever contents in the buffer columns down, turning off anything above it
        if debug == True: print("Starting scroll")
        for i in range(7): #number of iterations
            row = 6 #(should be 7 rows, work backwards)
            while row >= 0:
                for column in range(numCols): #(should be 5 columns)
                    currentPixel = column + startCol + row * 35
                    abovePixel = column + startCol + (row - 1) * 35
                    
                    if abovePixel >= 0:
                        self.copyPixel(abovePixel, currentPixel) #copy the pixel above to the current one
                        if debug == True: print("Iteration: " + str(i) + " Row: " + str(row) + " Column: " + str(column) + " Current Pixel: " + str(currentPixel) + " Above Pixel: " + str(abovePixel) + " Copied Pixel Down")
                    else:
                        self.buffer[currentPixel].off()
                        if debug == True: print("Iteration: " + str(i) + " Row: " + str(row) + " Column: " + str(column) + " Current Pixel: " + str(currentPixel) + " Above Pixel: " + str(abovePixel) + " Turned Pixel Off")
                bufferToGrid()
                refreshDisplay()
                
                row -= 1
            time.sleep(delay)
                
    def dissolve(self):
        #turn off a random pixel until they are all off
        #put all the on pixels into a list
        activeList = []
        for i in range(len(self.buffer)):
            if self.buffer[i].active == True:
                activeList.append(i)
        #randomList = random.sample(range(len(activeList),len(activeList)))
        for j in range(len(activeList)):
            thisPixel = random.choice(range(len(activeList)))
            self.buffer[activeList[thisPixel]].off()
            activeList.pop(thisPixel)
            

            #self.buffer[curPixel].off()
            bufferToGrid()
            refreshDisplay()

    def fadeOut(self, steps = 20):
        activeList = []
        maxBrightness = 0
        #get the pixels that need to fade, and the highest brightness
        for i in range(len(self.buffer)):
            if self.buffer[i].active == True:
                activeList.append(i)
                if self.buffer[i].curBrightness > maxBrightness: maxBrightness = self.buffer[i].curBrightness

        inc = -maxBrightness / steps

        #then fade them out
        for j in range(steps):
            for k in range (len(activeList)):
                if j == steps - 1:
                    self.buffer[activeList[k]].off()
                else:
                    self.buffer[activeList[k]].fadeByIncrement(inc)
            bufferToGrid()
            refreshDisplay()

    def fadeIn(self, steps = 20):
        #let's assume the buffer has already been updated to the desired thing at the desired color and we will use the global brightness
        activeList = []
        inc = globalBrightness / steps
        #get the pixels that need to fade
        for i in range(len(self.buffer)):
            if self.buffer[i].active == True:
                activeList.append(i)
                self.buffer[i].setBrightness(0)
        for j in range(steps):
            for k in range (len(activeList)):
                if j == steps - 1:
                    self.buffer[activeList[k]].setBrightness(globalBrightness)
                else:
                    self.buffer[activeList[k]].fadeByIncrement(inc)
            bufferToGrid()
            refreshDisplay()

 
    #inner class of the pixelbuffer class
    class apixel:
        def __init__(self, colorIndex = globalColorIndex, active = False):
            self.active = active
            self.curBrightness = globalBrightness #inherit the global brightness when initialized
            self.colorIndex = colorIndex #inherit the global color when initialized
            self.color = colorList[self.colorIndex]
            if active == False:
                self.rgb = OFF #rgb is the color value after brightness modification, the final output     
            else:
                self.rgb = [num * self.curBrightness for num in self.color]  
            if debug == True: print("A new pixel was initialized")

        
        #negative should decrease brightness, positive increases it
        def fadeByPercent(self, percent):
            self.curBrightness = constrain0to1(self.curBrightness * (1 + percent))
            self.rgb = [num * self.curBrightness for num in self.color]
            if debug == True: print("New brightness for this pixel is: " + str(self.curBrightness))

        def fadeByIncrement(self, increment):
            self.curBrightness = constrain0to1(self.curBrightness + increment)
            self.rgb = [num * self.curBrightness for num in self.color]
            if self.curBrightness == 0: self.off()
            if debug == True: print("New brightness for this pixel is: " + str(self.curBrightness))

        def randomColor(self):
            self.setColor(random.randrange(colorCount))
            if debug == True: print("New random color for this pixel")

        def nextColor(self):
            self.colorIndex = constrain(self.colorIndex + 1, 0, len(colorList) - 1, True)
            self.setColor(self.colorIndex)
            if debug == True: print("Next color")

        def prevColor(self):
            self.colorIndex = constrain(self.colorIndex - 1, 0, len(colorList) - 1, True)
            self.setColor(self.colorIndex)
            if debug == True: print("Previous Color")

        def setColor(self, colorIndex, activate = False):
            self.colorIndex = colorIndex
            self.color = colorList[self.colorIndex]
            if activate == True: self.active = True
            if self.active == True: self.rgb = [num * self.curBrightness for num in self.color]
            if debug == True: print("New color for this pixel is: " + str(self.colorIndex))

        def setBrightness(self, brightness, activate = False):
            self.curBrightness = brightness
            if activate == True: self.active = True
            if self.active == True: self.rgb = [num * self.curBrightness for num in self.color]
            if debug == True: print("New color for this pixel is: " + str(self.curBrightness))

        def on(self):
            self.active = True
            self.rgb = [num * self.curBrightness for num in self.color]
            if debug == True: print("Pixel activated")

        def off(self):
            self.active = False
            self.rgb = OFF
            if debug == True: print("Pixel deactivated")

        def toggle(self):
            if self.active == True:
                self.off()
            else:
                self.on()
            if debug == True: print("Pixel toggled")

#this is a 35x7 array, the index corresponds to the position in the 35x7, the number in that position is the neopixel in the 16x16 physical matrix
pixelAddressGrid = [15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 47, 46, 45, 
                    74, 75, 76, 77, 78, 79, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 
                    73, 72, 71, 70, 69, 68, 67, 66, 65, 64, 95, 94, 93, 92, 91, 90, 89, 88, 87, 86, 85, 84, 83, 82, 81, 80, 111, 110, 109, 108, 107, 106, 105, 104, 103, 
                    131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 96, 97, 98, 99, 100, 102, 
                    130, 129, 128, 159, 158, 157, 156, 155, 154, 153, 152, 151, 150, 148, 147, 146, 145, 144, 175, 174, 173, 172, 171, 170, 169, 168, 167, 166, 165, 164, 163, 162, 161, 160, 191, 
                    220, 221, 222, 223, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 
                    219, 218, 217, 216, 215, 214, 213, 212, 211, 210, 209, 208, 239, 238, 237, 236, 235, 234, 233, 232, 231, 230, 229, 228, 227, 226, 225, 224, 255, 254, 253, 252, 251, 250, 249]


p = pixelBuffer(len(pixelAddressGrid))

class animationTwinkle:
    #pick a pixel at random, set to max brightness, then look at all the other pixels thare are currently on and fade them by some percent
    #when one fades to off, turn on a new one

    def __init__(self, num = 10, randCol = False, fadeInc = -.1, interval = 10000000):
        self.randColor = randCol
        self.number = num
        self.frameInterval = interval
        self.fadeIncrement = fadeInc


    nextFrame = 0
    activePixelCount = 0
    
    def tick(self):
        now = time.monotonic_ns()

        if now > self.nextFrame:
            #do stuff
            self.nextFrame = now + self.frameInterval
            #Fade the active pixels
            for pixel in p.buffer:
                if pixel.active == True:
                    pixel.fadeByIncrement(self.fadeIncrement)
            #count the pixels
            for pixel2 in p.buffer:
                if pixel2.active == True: self.activePixelCount += 1
            #activate a pixel at random if less than the full amount are active
            if self.activePixelCount < self.number:
                thisPixel = random.randrange(len(p.buffer))
                p.buffer[thisPixel].setBrightness(1, True)
                if self.randColor == True:
                    p.buffer[thisPixel].randomColor()
            self.activePixelCount = 0
            bufferToGrid()
            refreshDisplay()

class animationCascade:
    def __init__(self, randCol = False, cycleCol = False, tail = 10, stagger = 1, interval = .001, onlyTurnOff = False):
        self.randColor = randCol
        self.tailLength = tail
        self.stagger = stagger
        self.frameInterval = interval
        self.cycleColor = cycleCol
        self.tempColorIndexValue = 0
        self.turnOff = onlyTurnOff
        
    def setup(self):
        #list for the current position of the head and tail
        self.head = []
        self.tail = []
        self.colorIndex = []
        self.nextFrame = 0
        
        

        for i in range (7):

            self.head.append(0 - i * self.stagger)
            self.tail.append(0 - i * self.stagger - self.tailLength)
            if self.randColor == True:
                self.colorIndex.append(random.randrange(len(colorList)))
            elif self.cycleColor == True:
                self.tempColorIndexValue = constrain(self.tempColorIndexValue + 1, 0, len(colorList) - 1, True)
                print(self.tempColorIndexValue)
                self.colorIndex.append(self.tempColorIndexValue)
            else:
                self.colorIndex.append(globalColorIndex)

    #length of the chunk:
    # stagger * rows + (tail - stagger)



    def tick(self):
        

        #every frame, add 1 to the head and light it up, and add one to the tail and turn it off
        for row in range(7):
            
            if self.head[row] >= 0 and self.head[row] < 35:
                p.buffer[row * 35 + self.head[row]].setColor(self.colorIndex[row], True)
            self.tail[row] += 1
            if self.tail[row] >= 0 and self.tail[row] < 35:
                p.buffer[row * 35 + self.tail[row]].off()
            self.head[row] += 1
        bufferToGrid()
        refreshDisplay()


    def run(self):
        self.setup()
        #run the animation for the right number of frames
        for i in range((self.stagger * 7 + self.tailLength - self.stagger) + 35): #the math here is bad
            self.tick()
            time.sleep(self.frameInterval)

        


    


#grab the color from the buffer, apply it to the pixels using the mapping table
def bufferToGrid():
    for i in range(len(p.buffer)):
        pixels[pixelAddressGrid[i]] = p.buffer[i].rgb
    if debug == True: print("Buffer copied to grid")

#refresh the actual display
def refreshDisplay():
    pixels.show()
    if debug == True: print("Display updated")

def nextColor():
    global globalColorIndex
    global globalColor
    globalColorIndex += 1
    if globalColorIndex >= colorCount:
        globalColorIndex = 0
    globalColor = colorList[globalColorIndex]
    p.setColorAll(globalColorIndex)
    if debug == True: print("Global color index is now: " + str(globalColorIndex))



p.clearAll()
bufferToGrid()
refreshDisplay()

def testScrollText():
    temp = p.stringToTempBuffer("ELLIOTMADE")
    p.scrollStringLeft(temp, 34)
    time.sleep(1)
    temp2 = p.stringToTempBuffer(["ghostred", "ghostpink", "ghostorange", "ghostcyan"])
    p.scrollStringLeft(temp2, 36)

def testGhosts():
    temp2 = p.stringToTempBuffer(["ghostred", "ghostpink", "ghostorange", "ghostcyan"])
    p.scrollStringLeft(temp2, 36)

def testAllChars():
    temp = None
    gc.collect()
    temp = p.stringToTempBuffer("ABCDEFGHIJKL")
    p.scrollStringLeft(temp)
    temp = None
    gc.collect()
    temp = p.stringToTempBuffer("MNOPQRSTUVWX")
    p.scrollStringLeft(temp)
    temp = None
    gc.collect()
    temp = p.stringToTempBuffer("YZ0123456789")
    p.scrollStringLeft(temp)
    temp = None
    gc.collect()
    temp = p.stringToTempBuffer("!?: ")
    p.scrollStringLeft(temp)
    
def testScrollDownText():
    p.setColorAll(6)
    p.stringToBuffer("ELLIOT", 1)
    bufferToGrid()
    refreshDisplay()
    time.sleep(1)
    p.scrollDown()

def testDissolve():
    #this is 2 and a half hearts
    p.charToBuffer("fheart", 2)
    p.charToBuffer("fheart", 10)
    p.charToBuffer("hheart", 18)
    p.charToBuffer("eheart", 26)
    p.setBrightnessAll(.1)
    bufferToGrid()
    refreshDisplay()

    time.sleep(1)

    p.dissolve()

def testFadeOut():
    p.charToBuffer("fheart", 2)
    p.charToBuffer("fheart", 10)
    p.charToBuffer("hheart", 18)
    p.charToBuffer("eheart", 26)
    bufferToGrid()
    time.sleep(.5)
    p.fadeOut()

def testFadeIn():
    p.charToBuffer("ghostred", 2)
    p.charToBuffer("ghostorange", 10)
    p.charToBuffer("ghostcyan", 18)
    p.charToBuffer("ghostpink", 26)
    bufferToGrid()

    p.fadeIn()



def demoSequence():
    #hello world
    p.setColorAll(4)
    p.stringToBuffer("HELLO", 3)
    bufferToGrid()
    p.fadeIn(40)
    time.sleep(1)
    p.scrollStringLeft(p.stringToTempBuffer("WORLD"), 2)
    time.sleep(1)
    p.fadeOut(40)
    
    #ghosts
    p.scrollStringLeft(p.stringToTempBuffer(["ghostred", "ghostpink", "ghostorange", "ghostcyan"]), 35)
    time.sleep(.5)
    
    #fake clock
    p.setColorAll(2)
    p.stringToBuffer("12 : 35 : 56",0,0)
    p.fadeIn()
    p.stringToBuffer("12 : 35 : 57",0,0)
    bufferToGrid()
    refreshDisplay()
    time.sleep(1)
    p.stringToBuffer("12 : 35 : 58",0,0)
    bufferToGrid()
    refreshDisplay()
    time.sleep(1)
    p.stringToBuffer("12 : 35 : 59",0,0)
    bufferToGrid()
    refreshDisplay()
    time.sleep(1)
    p.stringToBuffer("12 : 36 : 00",0,0)
    bufferToGrid()
    refreshDisplay()
    time.sleep(1)
    p.clearAll()
    p.stringToBuffer("12 : 36 : 0 1",0,0)
    bufferToGrid()
    refreshDisplay()
    time.sleep(1)
    p.stringToBuffer("12 : 36 : 02",0,0)
    bufferToGrid()
    refreshDisplay()
    time.sleep(1)
    p.scrollDown()

    #hearts
    p.charToBuffer("fheart", 2)
    bufferToGrid()
    refreshDisplay()
    time.sleep(.25)
    p.charToBuffer("fheart", 10)
    bufferToGrid()
    refreshDisplay()
    time.sleep(.25)
    p.charToBuffer("hheart", 18)
    bufferToGrid()
    refreshDisplay()
    time.sleep(.25)
    p.charToBuffer("eheart", 26)
    bufferToGrid()
    refreshDisplay()
    time.sleep(1)
    p.dissolve()

    p.setColorAll(11)
    endTime = time.monotonic() + 10
    twinkle = animationTwinkle(40, False, -0.025) 
    while time.monotonic() < endTime:
        twinkle.tick()


    endTime = time.monotonic() + 10
    twinkle = animationTwinkle(40, True, -0.025) 
    while time.monotonic() < endTime:
        twinkle.tick()

    p.setBrightnessAll(globalBrightness)

    cascade = animationCascade(False, False, 10, 1)
    cascade.run()

    cascade = animationCascade(True, False, 10, 0, 0.01)
    cascade.run()

    cascade = animationCascade(False, True, 25, 10)
    while 1 == 1:
        cascade.run()




def makingOf():
    global globalColorIndex
    globalColorIndex = 6
    temp = None
    gc.collect()
    temp = p.stringToTempBuffer("MAKING ")
    p.scrollStringLeft(temp)
    temp = None
    gc.collect()
    temp = p.stringToTempBuffer("OF ")
    p.scrollStringLeft(temp)
    temp = None
    gc.collect()
    temp = p.stringToTempBuffer("THIS ")
    p.scrollStringLeft(temp)
    temp = None
    gc.collect()
    temp = p.stringToTempBuffer("THING:")
    p.scrollStringLeft(temp, 35)


def fillHearts():
    delay = 0.1
    p.setBrightnessAll(.1)
    p.charToBuffer("eheart", 2)
    bufferToGrid()
    refreshDisplay()
    time.sleep(delay)
    p.setBrightnessAll(.1)
    p.charToBuffer("hheart", 2)
    bufferToGrid()
    refreshDisplay()
    time.sleep(delay)
    p.setBrightnessAll(.1)
    p.charToBuffer("fheart", 2)
    bufferToGrid()
    refreshDisplay()
    time.sleep(delay)
    p.setBrightnessAll(.1)
    p.charToBuffer("eheart", 10)
    bufferToGrid()
    refreshDisplay()
    time.sleep(delay)
    p.setBrightnessAll(.1)
    p.charToBuffer("hheart", 10)
    bufferToGrid()
    refreshDisplay()
    time.sleep(delay)
    p.setBrightnessAll(.1)
    p.charToBuffer("fheart", 10)
    bufferToGrid()
    refreshDisplay()
    time.sleep(delay)
    p.charToBuffer("eheart", 18)
    bufferToGrid()
    refreshDisplay()
    time.sleep(delay)
    p.setBrightnessAll(.1)
    p.charToBuffer("hheart", 18)
    bufferToGrid()
    refreshDisplay()
    time.sleep(delay)
    p.setBrightnessAll(.1)
    p.charToBuffer("fheart", 18)
    bufferToGrid()
    refreshDisplay()
    time.sleep(delay)
    p.charToBuffer("eheart", 26)
    bufferToGrid()
    refreshDisplay()
    time.sleep(delay)
    p.setBrightnessAll(.1)
    p.charToBuffer("hheart", 26)
    bufferToGrid()
    refreshDisplay()
    time.sleep(delay)
    p.setBrightnessAll(.1)
    p.charToBuffer("fheart", 26)
    bufferToGrid()
    refreshDisplay()
    print("did it")

    time.sleep(3)
    p.dissolve()
    time.sleep(.5)

    


while True:
    #fillHearts()
    #makingOf()
    #testGhosts()

    #cascade.run()

    demoSequence()

    #modeButton.tick()

    # twinkle.tick()

    #testAllChars()

    # testFadeIn()
    # time.sleep(1)

    # testFadeOut()
    # time.sleep(1)



        