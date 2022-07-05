from asyncio.windows_events import NULL
from cmath import sqrt
from graphlib import CycleError
from mimetypes import init
from pickle import NONE
from tracemalloc import stop
from turtle import clear, clearscreen
from xml.etree.ElementTree import PI
import cv2
import os
from matplotlib import pyplot as plt
import numpy as np
import time
import math
import requests
import Kamery2
from flask import Flask



def Obraz1(frame):
    frame = cv2.flip(frame , + 1 )
    frame2 = cv2.cvtColor(frame , cv2.COLOR_BGR2HSV)   
    mask = cv2.inRange(frame2 , lb , ub)
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, Kernal)
    res = cv2.bitwise_and(frame, frame, mask = opening)
    contours, hierarchy = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    if len(contours) != 0:
        cnt = contours[0]
        area = cv2.contourArea(cnt)
        M = cv2.moments(cnt)
        Cx = int(M['m10']/M['m00'])
        Cy = int(M['m01'] / M['m00'])
        Cy = 718 - Cy
        Cx = 639 - Cx  
        cv2.drawContours(frame, cnt, -1, (0, 255, 0), 3)
        '''
        S = 'Location of object:' + '(' + str(Cx) + ',' + str(Cy) + ')'    
        cv2.putText(frame, S, (5, 50), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
        C = 'Area Of Object: ' + str(area)
        cv2.putText(frame, C, (5, 100), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
        '''
        
        
        #Cz = ((-10**(-16)*area**3)+(2*10**(-10)*area**2)-(0.0002*area)+74.233)/3
        Cz = 90826*math.pow(area,(-0.557))
        yk =(0.8861*(Cy) - 1.4452)/10-40.816*math.pow(Cz,(-0.29))
        xk =(0.8861*Cx - 1.4452)/-10
        a = math.pow((Cz**2+xk**2),(0.5))
        #A ='Wspl x, y, z:' + ':' + str(round(xk,2)) + "\n" + str(round(yk,2)) + "\n" + str(round(Cz,2))
        cv2.putText(frame, 'Wspl x, y, z:', (1, 25), font, 0.5, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, str(round(xk,2)), (1, 50), font, 0.5, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, str(round(yk,2)), (1, 75), font, 0.5, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, str(round(Cz,2)), (1, 100), font, 0.5, (0, 0, 255), 2, cv2.LINE_AA)
        #cv2.imshow("Mask",mask)
        cv2.imshow("Rama 1", frame)
        return xk,yk,a,1
    else:
        cv2.imshow("Rama 1", frame)
        return 0,0,0,0




def Obraz2(frame1):
    frame1 = cv2.flip(frame1 , + 1 )
    frame2 = cv2.cvtColor(frame1 , cv2.COLOR_BGR2HSV)          ##BGR do HSV 
    mask = cv2.inRange(frame2 , lb , ub)
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, Kernal)
    res = cv2.bitwise_and(frame1, frame1, mask = opening)
    contours, hierarchy = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    if len(contours) != 0:
        cnt = contours[0]
        area = cv2.contourArea(cnt)
        M = cv2.moments(cnt)
        Cx = int(M['m10']/M['m00'])
        Cy = int(M['m01'] / M['m00'])
        Cy = 718 - Cy
        Cx = 639 - Cx  
        cv2.drawContours(frame1, cnt, -1, (0, 255, 0), 3)
        
        #Cz = ((-10**(-16)*area**3)+(2*10**(-10)*area**2)-(0.0002*area)+74.233)/3
        Cz = 90826*math.pow(area,(-0.557))
        yk =(0.8861*(Cy) - 1.4452)/10-40.816*math.pow(Cz,(-0.29))
        xk =(0.8861*Cx - 1.4452)/-10
        a = math.pow((Cz**2+xk**2),(0.5))
        #A ='Wspl x, y, z:' + ':' + str(round(xk,2)) + "\n" + str(round(yk,2)) + "\n" + str(round(Cz,2))
        cv2.putText(frame1, 'Wspl x, y, z:', (1, 25), font, 0.5, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(frame1, str(round(xk,2)), (1, 50), font, 0.5, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(frame1, str(round(yk,2)), (1, 75), font, 0.5, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(frame1, str(round(Cz,2)), (1, 100), font, 0.5, (0, 0, 255), 2, cv2.LINE_AA)
        #cv2.imshow("Mask 2",mask)
        cv2.imshow("Rama 2",frame1)
        return xk,yk,a,1
    else:
        cv2.imshow("Rama 1", frame1)
        return 0,0,0,0

os.system("cls")
cap = cv2.VideoCapture(2)
cap2 = cv2.VideoCapture(0)
Kernal = np.ones((3, 3), np.uint8)
font = cv2.FONT_HERSHEY_COMPLEX 

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)        ##Set camera resolution
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)        ##Set camera resolution
cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
c=2*230
xk = 0
yk = 0
a = 0
cnt = 0
while 1:
    print("Czy chcesz kalibrowac odczytywane kolory kamery?\nWybierz t jesli tak lub n jesli nie")
    i = input()
    if i == 't':
        zmienna = Kamery2.funkcja()
        os.system("cls")
        break
    if i == 'n':
        zmienna = [0,165,12,255,255,255]
        os.system("cls")
        break
    else:
        print('Podaj poprawna odpowiedz')
        time.sleep(2)
        os.system("cls")
        
#print(zmienna)
#print(zmienna[0],zmienna[1],zmienna[2],zmienna[3],zmienna[4],zmienna[5])
lb = np.array([ zmienna[0], zmienna[1] , zmienna[2] ])
ub = np.array([ zmienna[3] , zmienna[4] , zmienna[5] ])
t1 = time.time()
t2 = t1

while(1):
    
    ret , frame = cap.read()
    ret2, frame2 = cap2.read()
    frame = cv2.rotate(frame, cv2.ROTATE_180)
    frame2 = cv2.rotate(frame2, cv2.ROTATE_180)
    #cv2.imshow("1",frame)
    #cv2.imshow("2",frame2)
    temp1 = 0
    temp2 = 0
    xR1, yR1, a, temp1 = Obraz1(frame)
    #print("xk, yk, a, wart")
    #print(xR1, yR1, a, temp1)
    xR2, yR2, b, temp2 = Obraz2(frame2)
    #print("xk2, yk2, a2, wart2")
    #print(xR2, yR2, b, temp2)
    
    
    if temp1 == 1 and temp2 == 1:
        R_cos=(4*(a**2)*(b**2)-(((a**2)+(b**2)-(230**2))**2))
        #print(R_cos)
        if R_cos > 0:
            zR = math.pow(R_cos,(0.5))/c
            yR = (yR1+yR2)/2
            #print(yR, zR,a)
            x1 = math.pow((a**2-zR**2),0.5)
            x2 = math.pow((b**2-zR**2),0.5)
            xR1 = c/2 - x1
            xR2 = x2 - c/2
            xR = (xR1+xR2)/2
            xR = round(xR,0)
            yR = round(yR,0)
            zR = round(zR,0)
            if zR < 2000:
                print(xR, yR, zR)
                #time.sleep(5)
                t1 = time.time()
                t = t1 - t2
                if t >= 10:
                    wyslij= {"marker_x": xR,"marker_y": yR,"marker_z": zR}
                    response = requests.post('http://ipzkamery.pythonanywhere.com/pomiarky',json=wyslij)
                    #response2 = requests.get('http://ipzkamery.pythonanywhere.com/pomiary')
                    #if i==0 or i==6 or i==9:print(response2.json())
                    #print(t)
                    t1 = time.time()
                    t2 = t1

   

    if cv2.waitKey(1) == ord('s'):
        break
    
    
cap.release()
cv2.destroyAllWindows()