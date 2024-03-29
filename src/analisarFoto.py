#coding: utf-8
import cv2
import pytesseract
import sys
import numpy as np
from PIL import Image
from HELPERS import Functions


def analisarImagemBruto():
    possibleChars = []

    listOfGroups = []

    newGroup = []

    errorChance = 20

    colors = [(0,255,0),(0,0, 255),(255,0,0)]
    img = cv2.imread("imagem.jpg")

    maxRight = img.shape[1]
    maxBottom = img.shape[0]

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img_gray = cv2.GaussianBlur(img_gray,(3,3),0)

    ret, thresh = cv2.threshold(img_gray, 120, 255, cv2.THRESH_BINARY)

    _,contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        possibleChar = Functions.possibleChar(contour)

        if(Functions.checkIfChar(possibleChar)):
            possibleChars.append(possibleChar)


    color = 0
    for possibleChar in possibleChars:
        x = possibleChar.boundingRectX
        y = possibleChar.boundingRectY
        h = possibleChar.boundingRectH
        w = possibleChar.boundingRectW

        if(color == 2):
            color = 0
        else:
            color = color + 1

    counter = 0

    for possibleChar in possibleChars:

        if(len(possibleChars) == counter):
            break


        if(counter == 0):
            distanceNext = Functions.distanceBetween(possibleChar, possibleChars[counter+1])
            if(distanceNext <= possibleChar.boundingRectH):
                newGroup.append(possibleChar)


        if(counter > 1):
            possibleCharPrevious = possibleChars[counter-1]

            distancePrevious = Functions.distanceBetween(possibleCharPrevious, possibleChar)

            greaterH = possibleCharPrevious.boundingRectH
            if(possibleCharPrevious.boundingRectH < possibleChar.boundingRectH ):
                greaterH = possibleChar.boundingRectH

            if(distancePrevious <= greaterH*1.5):
                newGroup.append(possibleChar)
            else:
                listOfGroups.append(newGroup)
                newGroup = []
                newGroup.append(possibleChar)

        counter = counter + 1

    color = 0

    for group in listOfGroups:
        for possibleChar in group:
            x = possibleChar.boundingRectX
            y = possibleChar.boundingRectY
            h = possibleChar.boundingRectH
            w = possibleChar.boundingRectW

        if(color == 2):
            color = 0
        else:
            color = color + 1


    newListOfGroups = []
    for group in listOfGroups:
        if(len(group) > 1):
            newListOfGroups.append(group)


    listOfGroups = newListOfGroups

    color = 0
    for group in listOfGroups:
        for possibleChar in group:
            x = possibleChar.boundingRectX
            y = possibleChar.boundingRectY
            h = possibleChar.boundingRectH
            w = possibleChar.boundingRectW

        if(color == 2):
            color = 0
        else:
            color = color + 1

    newListGroups = []
    for group in listOfGroups:
        top = 10000
        left = 10000
        right = 0
        bottom = 0

        for item in group:
            x = item.boundingRectX
            y = item.boundingRectY
            h = item.boundingRectH
            w = item.boundingRectW
            if(y < top):
                top = y
            if(x < left):
                left = x
            if(x+w > right):
                right = x+w
            if(y+h > bottom):
                bottom = y+h

        if(top-errorChance < 0):
            top = 0
        else:
            top = top-errorChance

        if(left-errorChance < 0):
            left = 0
        else:
            left = left-errorChance

        if(right+errorChance > maxRight):
            right = maxRight
        else:
            right = right+errorChance
        
        if(bottom+errorChance > maxBottom):
            bottom = maxBottom
        else:
            bottom = bottom+errorChance

        groupObject = Functions.group(top, left, right, bottom)

        newListGroups.append(groupObject)


    listOfGroups = newListGroups



    joined = True

    aux = [ 0, 2 ]

    while joined == True:
        joined = False
        counter = 0
        newJoinGroup = []
        listOfJoinGroups = []

        for group in listOfGroups:
            
            if(counter == 0):
                newJoinGroup.append(group)
                if(len(listOfGroups) == 1):
                    listOfJoinGroups.append(newJoinGroup)
                    break
            else:
                groupPrevious = listOfGroups[counter-1]

                if( Functions.inGroups(groupPrevious, group)):
                    newJoinGroup.append(group)
                    joined = True
                elif(Functions.inGroups(group , groupPrevious)):
                    newJoinGroup.append(group)
                    joined = True
                else:
                    listOfJoinGroups.append(newJoinGroup)
                    newJoinGroup = []
                    newJoinGroup.append(group)

            counter = counter + 1

            if(len(listOfGroups) == counter):
                listOfJoinGroups.append(newJoinGroup)
                break




        newListGroups = []

        for joinedGroups in listOfJoinGroups:
            top = 10000
            left = 10000
            right = 0
            bottom = 0

            for group in joinedGroups:
                _top = group.top
                _left = group.left
                _right = group.right
                _bottom = group.bottom

                if(_top < top):
                    top = _top
                if(_left < left):
                    left = _left
                if(_right > right):
                    right = _right
                if(_bottom > bottom):
                    bottom = _bottom

            groupObject = Functions.group(top, left, right, bottom)

            newListGroups.append(groupObject)


        listOfGroups = newListGroups

    newListOfGroups = []

    for group in listOfGroups:

        roi = thresh[group.top:group.bottom, group.left:group.right]

        text = pytesseract.image_to_string(roi, config='-l eng')
        if(len(text) > 0):
            newListOfGroups.append(group)

    listOfGroups = newListOfGroups


    newListOfGroups = []

    for group in listOfGroups:
        if(Functions.checkPossiblePlate(group)):
            newListOfGroups.append(group)

    listOfGroups = newListOfGroups

    for group in listOfGroups:
        cv2.rectangle(img, (group.left,group.top), (group.right,group.bottom), (255,0,255), 2)
        roi = thresh[group.top:group.bottom, group.left:group.right]


        _, contours, hierarchy = cv2.findContours(roi, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    possibleChars = []

    for contour in contours:
        possibleChar = Functions.possibleChar(contour)

        if(Functions.checkIfChar(possibleChar)):
            possibleChars.append(possibleChar)

    color = 0
    counter = -1

    plateHeight = 160
    plateWidth = 390

    plate = False

    possibleChars = Functions.filterByGreater(possibleChars, 0.8)
    possibleChars = Functions.orderByX(possibleChars)

    margin = 1
    margin_offset = 5


    default_x_offset = 40
    x_offset = default_x_offset
    y_offset = 40

    expectedHeight = 60
    heightGap = 5

    plate_found = False
    plate_text = "cannotBeIdentified"

    while (plate_found == False and expectedHeight >= 20):

        x_offset = default_x_offset
        plate = Image.new('RGB', (plateWidth, plateHeight))

        for possibleChar in possibleChars:
            counter += 1
            x = possibleChar.boundingRectX + listOfGroups[0].left
            y = possibleChar.boundingRectY + listOfGroups[0].top
            h = possibleChar.boundingRectH
            w = possibleChar.boundingRectW

            roi = thresh[y-margin:y+h+margin, x-margin:x+w+margin]
            roi = Functions.applyBitwise_not(roi, w+margin*2, h+margin*2, 0.7)
            roi = Functions.resizeChar(Image.fromarray(roi), expectedHeight)

            area = (x_offset,y_offset)

            plate.paste(roi, area)
            x_offset += roi.size[0]+margin_offset

            if(color == 2):
                color = 0
            else:
                color = color + 1

        text = pytesseract.image_to_string(plate, config='-l eng')

        if(Functions.checkPlateText(text)):
            plate_found = True
            plate_text = text
        else:
            expectedHeight -= heightGap
    return Functions.formatPlate(plate_text)

def analisarImagem():
    try:
        return analisarImagemBruto()
    except:
        return False
