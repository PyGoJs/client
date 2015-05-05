import pygame, math
import urllib
#import file_reader_xml
import file_reader_json
from constants import *
import time
from datetime import datetime
import idreader

# Call this function so the Pygame library can initialize itself
pygame.init()

font = pygame.font.SysFont(None, 25)

# Create an 800x600 sized screen
screen = pygame.display.set_mode([screen_width, screen_height],pygame.FULLSCREEN)

# Set the title of the window
pygame.display.set_caption('Test')

file_reader_json.init()
pixelsBetweenRows = 20
pixelsBetweenCollums = 150
studentRow = 0
studentColumn = 0
studentStartingX = (screen_width / 2) - pixelsBetweenCollums#+ (screen_width / 4) - pixelsBetweenCollums
studentStartingY = screen_height / 4 - pixelsBetweenRows
counter = 0
idsScanned = []
last_id = get_last_id()
new_class_start_id = last_id
try:
    minTillStart = file_reader_json.getMinTillStart()
except:
    minTillStart = 999999
currentTime = datetime.now().hour * 60 + datetime.now().minute

def text_object(text, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_to_screen(msg, color, x, y):
    textSurface, textRect = text_object(msg, color)
    textRect.center = x, y
    screen.blit(textSurface, (x,y))#textRect)


clock = pygame.time.Clock()

loop = 1


done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
            if event.key == pygame.K_r:
                urllib.urlopen("http://pygojs.remi.im/checkin?clientid=PEvUGU6yL&rfid=%s&save=true" % idsScanned[0]).read()

    screen.fill(white)
    loop += 1
    
    
    if loop >= 5:
        idreader.get_id_file()

        with open("ids.txt", "r") as ins:
            arrayTest = []
	    n = 0
	    
	    
            for line in ins:
		if n < last_id:
		    n += 1
		    continue
                new = True
                for rfid in file_reader_json.rfids:
		    
                    if rfid == line[14:-1]:
                        for scanned in idsScanned[last_id:]:
                            if rfid == scanned:
                                new = False
                        if new == True:
                            idsScanned.append(rfid)

        for ids in idsScanned[last_id:]:
            urllib.urlopen("http://pygojs.remi.im/checkin?clientid=%s&rfid=%s" % (dezeClid, ids)).read()
            file_reader_json.studentsPresent[file_reader_json.rfids.index(ids)] = "Aanwezig"
            print file_reader_json.studentsPresent[file_reader_json.rfids.index(ids)]
            last_id += 1
        set_last_id(last_id)
        loop = 1
    amountPresent = 0
    studentRow = -1
    studentColumn = 1
    counter = -1
    h = 0
    m = 0
    if minTillStart > 60:
        h = minTillStart / 60
    if minTillStart > 0:
        m = minTillStart % 60
    if h * 60 + m > 0:
        message_to_screen("De Les begint in %s uur en %s minuten" % (str(h), str(m)), green, screen_width / 6, screen_height / 6)
    else:
        message_to_screen("De les is begonnen", green, screen_width / 6, screen_height / 6)
    for student in file_reader_json.students:
        counter += 1
        studentRow += 1
        # if there are more than x number of students move to the next column
        if studentRow >= 10:
            studentRow = 0
            studentColumn += 1
            # Change color if the student is present
        if file_reader_json.studentsPresent[counter] == 'Aanwezig':
            amountPresent += 1
            color = green
        else:
            color = black

        message_to_screen(student, color, studentStartingX + (studentColumn * pixelsBetweenCollums), studentStartingY + (studentRow * pixelsBetweenRows))

    message_to_screen("%d van de %d aanwezig." % (amountPresent, len(file_reader_json.studentsPresent)),green, screen_width / 1.5-100, screen_height / 1.2)

    # Drawing a uitline for error square
    #pygame.draw.rect(screen, black, (screen_width / 10, screen_height / 5 * 3, 400, 150), 0)
    #pygame.draw.rect(screen, white, (screen_width / 10 +5, screen_height / 5 * 3 +5, 400-10, 150-10), 0)
    #error drawing
    # TODO TODO TODO

    pygame.display.flip()

    t = datetime.now().hour * 60 + datetime.now().minute - currentTime
    if t != 0:
        minTillStart -= t
    currentTime = datetime.now().hour * 60 + datetime.now().minute

    clock.tick(5)

pygame.quit()
