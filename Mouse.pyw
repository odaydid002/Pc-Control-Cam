import win32api,cv2
import handdetectfunc as htm
import numpy as np

#---#########-----##########---#
wCam, hCam = 640, 480
wDisplay, hDisplay = 1366, 768
#---#########-----##########---#

cap = cv2.VideoCapture(0)
detector = htm.handDetector(detectionCon=int(0.7))

while True:
    success, img = cap.read()
    img = detector.findHands(img,False)
    lnList = detector.findPosition(img,draw=False)
    
    if len(lnList) !=0:
        x,y = lnList[8][1], lnList[8][2]
        
        x1 = np.interp(x,[0,640],[0, wDisplay])
        y1 = np.interp(y,[0,480],[0, hDisplay])
        
        win32api.SetCursorPos((int(x1),int(y1)))
    
    cv2.imshow("Image", img)
    cv2.waitKey(1)