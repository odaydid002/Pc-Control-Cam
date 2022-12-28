import cv2, math
import numpy as np
import handdetectfunc as htm
import screen_brightness_control as sbc


#---#########-----##########---#
wCam, hCam = 640, 480
wCam, hCam = 640, 480
wDisplay, hDisplay = 1366, 768
cap = cv2.VideoCapture(0)  
cap.set(3, wCam)
cap.set(4, hCam)
#---#########-----##########---#

detector = htm.handDetector(detectionCon=int(0.7))


while True:
    success, img = cap.read()
    img = detector.findHands(img,False)
    lnList = detector.findPosition(img,draw=False)
    if len(lnList)!=0:
    
        x1,y1 = lnList[4][1], lnList[4][2]                      
        x2,y2 = lnList[8][1], lnList[8][2]
        cx,cy = (x1+x2)//2, (y1+y2)//2

        # cv2.circle(img, (x1, y1), 10, (255,0,0), cv2.FILLED)
        # cv2.circle(img, (x2, y2), 10, (255,0,0), cv2.FILLED)
        # cv2.line(img, (x1,y1),(x2,y2),(255,0,0),3)
                   
        length = math.hypot(x2 -x1, y2 - y1)
        
        bright = np.interp(length,[50,200],[0, 100])  
        sbc.set_brightness(bright)


    cv2.imshow("image", img)
    cv2.waitKey(1)